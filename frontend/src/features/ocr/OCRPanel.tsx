import { useState } from "react";
import Card from "../../components/Card";
import UploadBox from "../../components/UploadBox";
import Button from "../../components/Button";
import { Spinner } from "../../components/Spinner";
import JSONBlock from "../../components/JSONBlock";
import { ocr } from "./api";

export default function OCRPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<any>(null);
  async function go() {
    if (!file) return;
    setLoading(true);
    try {
      setRes(await ocr(file));
    } catch (e: any) {
      setRes({ error: String(e) });
    } finally {
      setLoading(false);
    }
  }
  return (
    <>
      <Card title="上传图片">
        <UploadBox accept="image/*" onFile={setFile} hint="最长边 ≤ 1600px" />
        {file && (
          <div className="mt-3 flex justify-between text-sm">
            <span className="truncate">{file.name}</span>
            <Button onClick={go} disabled={loading}>
              开始识别
            </Button>
          </div>
        )}
      </Card>
      <Card title="结果">
        {loading ? (
          <Spinner label="正在识别…" />
        ) : res ? (
          res.error ? (
            <div className="text-rose-700">{res.error}</div>
          ) : (
            <>
              <div className="text-sm whitespace-pre-wrap bg-slate-100 rounded-xl p-3 max-h-72 overflow-auto">
                {res.text}
              </div>
              <JSONBlock data={{ lines: res.lines, time_ms: res.time_ms }} />
            </>
          )
        ) : (
          <div className="text-sm text-slate-400">暂无</div>
        )}
      </Card>
    </>
  );
}
