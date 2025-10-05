import { useState } from "react";
import Card from "../../components/Card";
import UploadBox from "../../components/UploadBox";
import Button from "../../components/Button";
import { Spinner } from "../../components/Spinner";
import JSONBlock from "../../components/JSONBlock";
import { transcribe } from "./api";

export default function ASRPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [lang, setLang] = useState("auto");
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<any>(null);
  async function go() {
    if (!file) return;
    setLoading(true);
    try {
      setRes(await transcribe(file, lang));
    } catch (e: any) {
      setRes({ error: String(e) });
    } finally {
      setLoading(false);
    }
  }
  return (
    <>
      <Card
        title="上传音频"
        extra={
          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            className="text-sm border rounded-lg px-2 py-1"
          >
            <option value="auto">自动识别</option>
            <option value="zh">中文</option>
            <option value="en">English</option>
          </select>
        }
      >
        <UploadBox
          accept="audio/*"
          onFile={setFile}
          hint="16kHz 单声道，≤ 5 分钟"
        />
        {file && (
          <div className="mt-3 flex justify-between text-sm">
            <span className="truncate">{file.name}</span>
            <Button onClick={go} disabled={loading}>
              开始转写
            </Button>
          </div>
        )}
      </Card>
      <Card title="结果">
        {loading ? (
          <Spinner label="正在转写…" />
        ) : res ? (
          res.error ? (
            <div className="text-rose-700">{res.error}</div>
          ) : (
            <div className="space-y-3">
              <div className="text-sm whitespace-pre-wrap bg-slate-100 rounded-xl p-3 max-h-72 overflow-auto">
                {res.text}
              </div>
              <JSONBlock
                data={{ segments: res.segments, time_ms: res.time_ms }}
              />
            </div>
          )
        ) : (
          <div className="text-sm text-slate-400">暂无</div>
        )}
      </Card>
    </>
  );
}
