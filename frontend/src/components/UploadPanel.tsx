type Props = {
  label: string;
  file: File | null;
  onChange: (file: File | null) => void;
};

export function UploadPanel({ label, file, onChange }: Props) {
  return (
    <div className="panel">
      <h3>{label}</h3>
      <input
        type="file"
        accept=".step,.stp"
        onChange={(e) => onChange(e.target.files?.[0] ?? null)}
      />
      <p className="muted">{file ? file.name : "No file selected"}</p>
    </div>
  );
}
