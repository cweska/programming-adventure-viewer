export function Torch({ side }: { side: "left" | "right" }) {
  return (
    <div className={`torch torch-${side}`} data-testid={`torch-${side}`} aria-hidden="true">
      <div className="flame" />
      <div className="torch-cup" />
      <div className="torch-stick" />
    </div>
  );
}
