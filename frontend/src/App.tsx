import { useCallback, useEffect, useState } from "react";
import { deleteDocument, extractText, listDocuments } from "./api/client";
import HistoryList from "./components/HistoryList";
import ResultPanel from "./components/ResultPanel";
import UploadZone from "./components/UploadZone";
import type { OCRDocument } from "./types";

export default function App() {
  const [documents, setDocuments] = useState<OCRDocument[]>([]);
  const [current, setCurrent] = useState<OCRDocument | null>(null);
  const [removeMasthead, setRemoveMasthead] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const list = await listDocuments();
      setDocuments(list.documents);
    } catch {
      /* history is non-critical; upload still works */
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const handleFile = async (file: File) => {
    setBusy(true);
    setError(null);
    try {
      const doc = await extractText(file, removeMasthead);
      setCurrent(doc);
      setDocuments((prev) => [doc, ...prev]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Extraction failed");
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async (id: string) => {
    await deleteDocument(id).catch(() => undefined);
    setDocuments((prev) => prev.filter((d) => d.id !== id));
    if (current?.id === id) setCurrent(null);
  };

  return (
    <div className="app">
      <header className="masthead">
        <h1>
          <span className="masthead-urdu" lang="ur">نسخہ</span>
          <span className="masthead-latin">Nuskha · Urdu Newspaper OCR</span>
        </h1>
        <p>Upload a Nastaliq newspaper scan and get clean, copyable Urdu text.</p>
      </header>

      <main className="layout">
        <div className="work-column">
          <UploadZone onSelect={handleFile} disabled={busy} />

          <label className="option-row">
            <input
              type="checkbox"
              checked={removeMasthead}
              onChange={(e) => setRemoveMasthead(e.target.checked)}
              disabled={busy}
            />
            Crop the newspaper banner before reading (top 18%)
          </label>

          {busy && (
            <div className="status reading" role="status">
              Reading the page… this takes 15–40 seconds for dense text.
            </div>
          )}
          {error && (
            <div className="status error" role="alert">
              {error}
            </div>
          )}

          {current && <ResultPanel doc={current} />}
        </div>

        <aside className="history-column">
          <h3>History</h3>
          <HistoryList
            documents={documents}
            activeId={current?.id ?? null}
            onOpen={setCurrent}
            onDelete={handleDelete}
          />
        </aside>
      </main>
    </div>
  );
}
