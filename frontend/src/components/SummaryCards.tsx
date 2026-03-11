type Props = {
  report: any;
};

export function SummaryCards({ report }: Props) {
  const s = report.summary;
  return (
    <div className="summary-grid">
      <div className="card"><strong>Total changes</strong><span>{s.total_changes}</span></div>
      <div className="card"><strong>Added volume</strong><span>{s.added_volume.toFixed(3)} mm³</span></div>
      <div className="card"><strong>Removed volume</strong><span>{s.removed_volume.toFixed(3)} mm³</span></div>
      <div className="card"><strong>Volume delta</strong><span>{s.volume_delta.toFixed(3)} mm³</span></div>
    </div>
  );
}
