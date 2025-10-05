import { useRef } from "react";
export default function UploadBox({
  accept,
  onFile,
  hint,
}: {
  accept: string;
  onFile: (f: File) => void;
  hint?: string;
}) {
  const ref = useRef<HTMLInputElement | null>(null);
  return (
    <div
      className="rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 hover:bg-slate-100 h-44 grid place-content-center cursor-pointer"
      onClick={() => ref.current?.click()}
    >
      <input
        ref={ref}
        type="file"
        accept={accept}
        className="hidden"
        onChange={(e) => {
          const f = e.target.files?.[0];
          if (f) onFile(f);
        }}
      />
      <div className="text-center text-sm text-slate-600">
        <div className="font-medium">点击选择文件 / 拖拽到此处</div>
        <div className="text-xs mt-1 text-slate-500">{hint || accept}</div>
      </div>
    </div>
  );
}
