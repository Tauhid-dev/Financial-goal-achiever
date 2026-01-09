import React, { useEffect, useState } from 'react';
import { ensureSession } from '../lib/session';
import { listDocuments, uploadDocument } from '../lib/endpoints';
import { Document } from '../lib/types';
import { Scope } from '../lib/types';

export const DocumentsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const fetchDocs = async (scope: Scope) => {
    const docs = await listDocuments(scope);
    setDocuments(docs);
  };

  const handleUpload = async () => {
    if (!file) return;
    // Client‑side PDF validation
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
      setError('Only PDF files are allowed');
      return;
    }
    setUploading(true);
    try {
      const scope = await ensureSession();
      await uploadDocument(scope, file);
      await fetchDocs(scope);
      setFile(null);
    } catch (err: any) {
      // Preserve existing error message; could be auth, validation, or generic
      setError(err.message ?? 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const scope = await ensureSession();
        await fetchDocs(scope);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return (
  <div style={{ color: 'red' }}>
    {error}
    <button onClick={() => window.location.reload()} style={{ marginLeft: '1rem' }}>Reload</button>
  </div>
);

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
        <button onClick={handleUpload} disabled={!file || uploading}>
          {uploading ? 'Uploading…' : 'Upload PDF'}
        </button>
      </div>
    </div>
  );
};

export default DocumentsPage;
