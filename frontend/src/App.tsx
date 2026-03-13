import { useState } from "react";
import { compareParts } from "./api/client";
import { ChangeList } from "./components/ChangeList";
import { ComparisonSettings } from "./components/ComparisonSettings";
import { DiffViewer } from "./components/DiffViewer";
import { SummaryCards } from "./components/SummaryCards";
import { UploadPanel } from "./components/UploadPanel";

export function App() {
  const [fileA, setFileA] = useState<File | null>(null);
  const [fileB, setFileB] = useState<File | null>(null);
  const [tolerance, setTolerance] = useState(0.01);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [report, setReport] = useState<any | null>(null);

  const runCompare = async () => {
    if (!fileA || !fileB) {
      setError("Please upload both STEP files.");
      return;
    }
    setBusy(true);
    setError(null);
    const result = await compareParts(fileA, fileB, tolerance);
    setBusy(false);

    if (result.status === "error") {
      setError(result.error || "Comparison failed.");
      return;
    }
    setReport(result.report);
  };

  return (
    <div className="app">
      <header>
        <h1>CAD Diff</h1>
        <p>Engineer-friendly geometric revision comparison for STEP parts.</p>
      </header>

      <div className="grid-2">
        <UploadPanel label="CAD File A (baseline)" file={fileA} onChange={setFileA} />
        <UploadPanel label="CAD File B (revision)" file={fileB} onChange={setFileB} />
      </div>

      <ComparisonSettings tolerance={tolerance} setTolerance={setTolerance} />

      <button className="primary" onClick={runCompare} disabled={busy}>
        {busy ? "Comparing…" : "Run Comparison"}
      </button>

      {error && <p className="error">{error}</p>}

      {report && (
        <>
          <SummaryCards report={report} />
          <div className="grid-2">
            <ChangeList changes={report.changes} onSelect={(id) => console.log("zoom to", id)} />
            <DiffViewer />
          </div>
        </>
      )}
    </div>
  );
}
