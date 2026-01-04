import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listDocuments, uploadDocument } from '../lib/endpoints';
import { Document } from '../lib/types';

export const DocumentsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [file, setFile] = useState<File | null>(null);

  const fetchDocs = async (familyId: string) => {
    const docs = await listDocuments(familyId);
    setDocuments(docs);
  };

  const handleUpload = async () => {
    if (!file) return;
    try {
      const { scopeId, familyId } = await ensureSession();
const fid = familyId ?? scopeId;
      await uploadDocument(fid, file);
      await fetchDocs(fid);
      setFile(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const { scopeId, familyId } = await ensureSession();
const fid = familyId ?? scopeId;
        await fetchDocs(fid);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Documents</h2>
      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>
            {doc.filename} – {new Date(doc.uploaded_at).toLocaleDateString()}
          </li>
        ))}
      </ul>
      <div>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button onClick={handleUpload} disabled={!file}>
          Upload PDF
        </button>
      </div>
    </div>
  );
};

export default DocumentsPage;
