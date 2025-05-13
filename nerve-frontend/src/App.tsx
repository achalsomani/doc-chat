import { useNavigate } from 'react-router-dom';
import { FiUpload, FiMessageSquare, FiClock } from 'react-icons/fi';

export default function App() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-12">Take Home Assessment</h1>
      <div className="flex gap-12">
        <button
          className="w-40 h-40 bg-blue-600 text-white text-lg font-semibold rounded-full shadow-lg hover:bg-blue-700 transition flex flex-col items-center justify-center"
          onClick={() => navigate('/Ingest')}
        >
          <FiUpload size={32} />
          <span className="mt-2">Ingest</span>
        </button>
        <button
          className="w-40 h-40 bg-green-600 text-white text-lg font-semibold rounded-full shadow-lg hover:bg-green-700 transition flex flex-col items-center justify-center"
          onClick={() => navigate('/chat/new')}
        >
          <FiMessageSquare size={32} />
          <span className="mt-2">Chat</span>
        </button>
        <button
          className="w-40 h-40 bg-gray-700 text-white text-lg font-semibold rounded-full shadow-lg hover:bg-gray-800 transition flex flex-col items-center justify-center"
          onClick={() => navigate('/history')}
        >
          <FiClock size={32} />
          <span className="mt-2">History</span>
        </button>
      </div>
    </div>
  );
}
