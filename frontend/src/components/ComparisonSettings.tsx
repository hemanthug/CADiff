type Props = {
  tolerance: number;
  setTolerance: (value: number) => void;
};

export function ComparisonSettings({ tolerance, setTolerance }: Props) {
  return (
    <div className="panel">
      <h3>Comparison Settings</h3>
      <label>
        Tolerance (mm)
        <input
          type="number"
          min={0}
          step={0.001}
          value={tolerance}
          onChange={(e) => setTolerance(Number(e.target.value))}
        />
      </label>
    </div>
  );
}
