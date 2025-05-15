import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Ingest from "./pages/ingest_file";
import Chat from "./pages/chat";
import History from "./pages/history";
import "./index.css";
import { ChatProvider } from "./context/contextProvider";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ChatProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/ingest" element={<Ingest />} />
          <Route path="/chat/:chatId" element={<Chat />} />
          <Route path="/chat/new" element={<Chat />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </BrowserRouter>
    </ChatProvider>
  </React.StrictMode>,
);
