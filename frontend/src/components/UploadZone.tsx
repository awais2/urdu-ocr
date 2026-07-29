import { useCallback, useRef, useState } from "react";

interface Props {
  onSelect: (file: File) => void;
  disabled: boolean;
}

const ACCEPTED = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp", "image/tiff"];

export default function UploadZone({ onSelect, disabled }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);

  const pick = useCallback(
    (file: File | undefined) => {
      if (!file || disabled) return;
      if (!ACCEPTED.includes(file.type)) return;
      onSelect(file);
    },
    [onSelect, disabled]
  );

  return (
    <div
      className={`upload-zone ${dragging ? "dragging" : ""} ${disabled ? "disabled" : ""}`}
      role="button"
      tabIndex={0}
      onClick={() => !disabled && inputRef.current?.click()}
      onKeyDown={(e) => e.key === "Enter" && !disabled && inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);
        pick(e.dataTransfer.files[0]);
      }}
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED.join(",")}
        hidden
        onChange={(e) => {
          pick(e.target.files?.[0]);
          e.target.value = "";
        }}
      />
      <span className="upload-glyph" aria-hidden>&#x235F;</span>
      <p className="upload-title">Drop a newspaper scan here</p>
      <p className="upload-hint">or click to browse — JPG, PNG, GIF, WEBP up to 15 MB</p>
    </div>
  );
}
