export default function JSONBlock({ data }: { data: any }) {
  return (
    <pre className="bg-slate-900 text-slate-50 rounded-xl p-4 text-xs overflow-auto max-h-96">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
