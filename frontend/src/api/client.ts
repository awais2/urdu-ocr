import type { OCRDocument, OCRDocumentList } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Request failed (${res.status})`);
  }
  return res.json() as Promise<T>;
}

export async function extractText(
  file: File,
  removeMasthead: boolean
): Promise<OCRDocument> {
  const form = new FormData();
  form.append("file", file);
  form.append("remove_masthead", String(removeMasthead));
  const res = await fetch(`${API_URL}/api/ocr/extract`, {
    method: "POST",
    body: form,
  });
  return handle<OCRDocument>(res);
}

export async function listDocuments(): Promise<OCRDocumentList> {
  const res = await fetch(`${API_URL}/api/documents`);
  return handle<OCRDocumentList>(res);
}

export async function deleteDocument(id: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/documents/${id}`, { method: "DELETE" });
  await handle<{ deleted: boolean }>(res);
}
