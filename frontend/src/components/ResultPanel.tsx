import { useState } from "react";
import type { OCRDocument } from "../types";

interface Props {
  doc: OCRDocument;
}

export default function ResultPanel({ doc }: Props) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    await navigator.clipboard.writeText(doc.extracted_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  };

  const download = () => {
    const blob = new Blob([doc.extracted_text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = doc.filename.replace(/\.[^.]+$/, "") + ".txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="result-panel">
      <header className="result-header">
        <div>
          <h2>{doc.filename}</h2>
          <time>{new Date(doc.created_at).toLocaleString()}</time>
        </div>
        <div className="result-actions">
          <button onClick={copy}>{copied ? "Copied" : "Copy text"}</button>
          <button onClick={download}>Download .txt</button>
        </div>
      </header>
      <div className="clipping" dir="rtl" lang="ur">
        {doc.extracted_text || "— no text detected —"}
      </div>
    </section>
  );
}
