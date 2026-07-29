export interface OCRDocument {
  id: string;
  filename: string;
  extracted_text: string;
  status: string;
  remove_masthead: boolean;
  created_at: string;
}

export interface OCRDocumentList {
  total: number;
  documents: OCRDocument[];
}
