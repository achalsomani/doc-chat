import { useState } from 'react';
import api from '../api';

export default function Ingest() {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return alert('Please select a file first.');
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/ingest', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert(`File Ingested: ${response.data.success}`);
    } catch (error) {
      console.error('Upload Error:', error);
      alert('Failed to upload file.');
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-3xl font-bold mb-8">Ingest File</h1>
      <input type="file" accept=".txt" onChange={(e) => setFile(e.target.files?.[0] || null)} />
      <button
        className="bg-blue-600 text-white px-6 py-3 rounded-full hover:bg-blue-700 transition mt-4"
        onClick={handleUpload}
      >
        Upload
      </button>
    </div>
  );
}
