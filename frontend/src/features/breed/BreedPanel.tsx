import { useState } from "react";
import Card from "../../components/Card";
import UploadBox from "../../components/UploadBox";
import Button from "../../components/Button";
import { Spinner } from "../../components/Spinner";
import JSONBlock from "../../components/JSONBlock";
import { classify } from "./api";

export default function BreedPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [topk, setTopk] = useState(5);
  const [loading, setLoading] = useState(false);
  const [res, setRes] = useState<any>(null);
  async function go() {
    if (!file) return;
    setLoading(true);
    try {
      setRes(await classify(file, topk));
    } catch (e: any) {
      setRes({ error: String(e) });
    } finally {
      setLoading(false);
    }
  }
  return (
    <>
      <Card
        title="上传宠物照片"
        extra={
          <div className="flex items-center gap-2 text-sm">
            <span className="text-slate-500">Top-k</span>
            <input
              type="number"
              min={1}
              max={10}
              value={topk}
              onChange={(e) => setTopk(parseInt(e.target.value || "5", 10))}
              className="w-16 border rounded-lg px-2 py-1"
            />
          </div>
        }
      >
        <UploadBox
          accept="image/*"
          onFile={setFile}
          hint="正面无遮挡，背景简洁更准"
        />
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
          <Spinner label="正在分类…" />
        ) : res ? (
          res.error ? (
            <div className="text-rose-700">{res.error}</div>
          ) : (
            <div className="space-y-4">
              {res.unknown && (
                <div className="text-amber-700 bg-amber-50 border border-amber-200 rounded-xl p-3 text-sm">
                  置信度较低，建议上传更清晰的正面照片。
                </div>
              )}
              <ul className="space-y-2">
                {(res.topk || []).map((it: any, i: number) => (
                  <li
                    key={i}
                    className="flex items-center justify-between bg-slate-50 rounded-xl p-3 text-sm"
                  >
                    <div>
                      <div className="font-medium">{it.zh || it.label}</div>
                      {it.zh && (
                        <div className="text-xs text-slate-500">{it.label}</div>
                      )}
                    </div>
                    <div className="font-mono">
                      {(it.score * 100).toFixed(1)}%
                    </div>
                  </li>
                ))}
              </ul>
              <JSONBlock data={{ raw: res }} />
            </div>
          )
        ) : (
          <div className="text-sm text-slate-400">暂无</div>
        )}
      </Card>
    </>
  );
}
