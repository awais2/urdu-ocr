import type { OCRDocument } from "../types";

interface Props {
  documents: OCRDocument[];
  activeId: string | null;
  onOpen: (doc: OCRDocument) => void;
  onDelete: (id: string) => void;
}

export default function HistoryList({ documents, activeId, onOpen, onDelete }: Props) {
  if (documents.length === 0) {
    return <p className="history-empty">Extractions you run will appear here.</p>;
  }
  return (
    <ul className="history-list">
      {documents.map((d) => (
        <li key={d.id} className={d.id === activeId ? "active" : ""}>
          <button className="history-open" onClick={() => onOpen(d)}>
            <span className="history-name">{d.filename}</span>
            <span className="history-date">
              {new Date(d.created_at).toLocaleDateString()}
            </span>
          </button>
          <button
            className="history-delete"
            aria-label={`Delete ${d.filename}`}
            onClick={() => onDelete(d.id)}
          >
            &times;
          </button>
        </li>
      ))}
    </ul>
  );
}
