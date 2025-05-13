import React, { createContext, useContext, useState } from 'react';

type Message = {
  role: 'user' | 'assistant';
  content: string;
  used_chunks?: string[];
};

type ChatContextType = {
  chatId: string;
  messages: Message[];
  setChatId: (id: string) => void;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
};

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [chatId, setChatId] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);

  return (
    <ChatContext.Provider value={{ chatId, setChatId, messages, setMessages }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (!context) throw new Error('useChat must be used within a ChatProvider');
  return context;
};
