import { useEffect, useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

type Chat = {
  chat_id: string;
  content: { user?: string; ai?: string }[];
};

export default function HistoryPage() {
  const [chats, setChats] = useState<Chat[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get("/history");
        setChats(res.data.chats);
      } catch (err) {
        console.error("Failed to fetch history:", err);
      }
    };
    fetchHistory();
  }, []);

  const getFirstQuestion = (content: Chat["content"]) => {
    const first = content.find((msg) => msg.user);
    return first ? first.user : "No question yet";
  };

  return (
    <div className="flex flex-col items-center justify-center p-4 min-h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Chat History</h1>
      <div className="w-full max-w-lg space-y-4">
        {chats.map((chat) => (
          <div
            key={chat.chat_id}
            className="w-full border-b pb-4 cursor-pointer"
            onClick={() => navigate(`/chat/${chat.chat_id}`)}
          >
            {getFirstQuestion(chat.content)}
          </div>
        ))}
      </div>
    </div>
  );
}
