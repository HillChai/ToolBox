export default function Card({
  title,
  extra,
  children,
}: {
  title: string;
  extra?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 md:p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="font-medium">{title}</h2>
        {extra}
      </div>
      {children}
    </div>
  );
}
