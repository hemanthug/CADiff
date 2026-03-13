type Props = {
  changes: any[];
  onSelect: (id: string) => void;
};

export function ChangeList({ changes, onSelect }: Props) {
  return (
    <div className="panel">
      <h3>Detected Changes</h3>
      <ul className="change-list">
        {changes.map((change) => (
          <li key={change.change_id}>
            <button onClick={() => onSelect(change.change_id)}>
              <strong>{change.title}</strong>
              <span>{change.description}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
