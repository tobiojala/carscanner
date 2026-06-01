type ProfitBarProps = {
  value: number;
  max: number;
};

export function ProfitBar({ value, max }: ProfitBarProps) {
  const percent = max > 0 ? Math.max(4, Math.min(100, (value / max) * 100)) : 0;
  return (
    <div className="profit-bar" aria-label={`Profit ${Math.round(value)} SEK`}>
      <div className="profit-bar-fill" style={{ width: `${percent}%` }} />
    </div>
  );
}
