import { useState, useEffect } from "react";
import api from "../api";
import { useChat } from "../context/contextProvider";
import { useParams } from "react-router-dom";

type Message = {
  role: "user" | "assistant";
  content: string;
  used_chunks?: string[];
};

export default function ChatPage() {
  const { chatId, setChatId, messages, setMessages } = useChat();
  const [input, setInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [sending, setSending] = useState<boolean>(false);
  const { chatId: urlChatId } = useParams();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadChat = async () => {
      if (urlChatId && urlChatId !== "new") {
        setLoading(true);
        setChatId(urlChatId);
        try {
          const res = await api.get(`/chat/${urlChatId}`);
          const mappedMessages = res.data.messages.flatMap(
            (msg: { user: string; agent: string }) =>
              [
                msg.user ? { role: "user", content: msg.user } : null,
                msg.agent ? { role: "assistant", content: msg.agent } : null,
              ].filter(Boolean),
          );
          setMessages(mappedMessages);
        } catch (err) {
          console.error("Failed to load chat:", err);
        } finally {
          setLoading(false);
        }
      }
    };
    loadChat();
  }, [urlChatId]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setError(null);
    setSending(true);

    let currentChatId = chatId;
    if (!currentChatId || urlChatId === "new") {
      const res = await api.post("/chat/new");
      currentChatId = res.data.chat_id;
      setChatId(currentChatId);
      window.history.pushState({}, "", `/chat/${currentChatId}`);
    }

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    try {
      const res = await api.post("/message", {
        chat_id: currentChatId,
        input,
      });

      const assistantMessage: Message = {
        role: "assistant",
        content: res.data.response,
        used_chunks: res.data.used_chunks,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError("Failed to send message. Please try again.");
      setMessages((prev) => prev.slice(0, -1));
      console.error("Message Send Failed:", err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-4 min-h-screen bg-gray-100">
      {loading ? (
        <div className="text-gray-600 text-lg">Loading chat...</div>
      ) : (
        <>
          <div className="w-full max-w-lg space-y-2 flex-1 overflow-y-auto mb-4">
            {messages.map((msg, idx) => (
              <div key={idx} className="p-3 rounded-lg max-w-xs self-start ">
                {msg.role === "user" ? (
                  <div style={{ color: "blue" }}>
                    <strong>Question:</strong> {msg.content}
                  </div>
                ) : (
                  <div>
                    <strong>Answer:</strong> {msg.content}
                  </div>
                )}
              </div>
            ))}
          </div>
          <div className="flex w-full max-w-lg">
            <input
              className="flex-1 p-3 border rounded-lg"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask your question..."
              disabled={sending}
            />
            <button
              className="ml-2 p-3 bg-blue-600 text-white rounded-lg"
              onClick={sendMessage}
              disabled={!input.trim() || sending}
            >
              {sending ? "Sending..." : "Send"}
            </button>
          </div>
          {sending && (
            <div className="text-gray-600 mt-2 w-full max-w-lg text-center">
              Waiting for response...
            </div>
          )}
          {error && (
            <div style={{ color: "red" }} className="mt-2 w-full max-w-lg">
              {error}
            </div>
          )}
        </>
      )}
    </div>
  );
}
