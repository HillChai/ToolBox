export default function Button(
  p: React.ButtonHTMLAttributes<HTMLButtonElement>
) {
  return (
    <button
      {...p}
      className={
        "px-4 py-2 rounded-xl text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50 " +
        (p.className || "")
      }
    />
  );
}
