import { Suspense, lazy, useState } from "react";
import Card from "../components/Card";

const ASRPanel = lazy(() => import("../features/asr/ASRPanel"));
const OCRPanel = lazy(() => import("../features/ocr/OCRPanel"));
const BreedPanel = lazy(() => import("../features/breed/BreedPanel"));

const TABS = [
  { id: "ocr", name: "图片文字识别" },
  { id: "breed", name: "猫狗品种识别" },
  { id: "asr", name: "语音转文字" },
] as const;

export default function App() {
  const [tab, setTab] = useState<(typeof TABS)[number]["id"]>("asr");
  return (
    <div className=" bg-slate-50 text-slate-900">
      <main className="mx-auto max-w-screen-2xl w-full px-4 pb-24">
        <nav className="mt-6 rounded-2xl p-1 bg-white border border-slate-200 shadow-sm grid grid-cols-3 text-sm">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`px-4 py-2 rounded-xl transition ${"text-slate-700 hover:bg-slate-100"}`}
            >
              {t.name}
            </button>
          ))}
        </nav>

        <div className="mt-6 grid gap-6 lg:grid-cols-3">
          <section className="lg:col-span-2">
            <Suspense
              fallback={
                <Card title="加载中…">
                  <div className="text-sm">正在载入面板…</div>
                </Card>
              }
            >
              {tab === "asr" && <ASRPanel />}
              {tab === "ocr" && <OCRPanel />}
              {tab === "breed" && <BreedPanel />}
            </Suspense>
          </section>
          <section className="lg:col-span-1">
            <Card title="拍摄/上传建议">
              <ul className="list-disc pl-5 space-y-2 text-sm text-slate-600">
                {tab === "asr" && (
                  <>
                    <li>16kHz 单声道，去除长静音。</li>
                    <li>超 5 分钟建议分段。</li>
                  </>
                )}
                {tab === "ocr" && (
                  <>
                    <li>正摄、光线均匀；长图可分段。</li>
                    <li>手写体效果受限。</li>
                  </>
                )}
                {tab === "breed" && (
                  <>
                    <li>正面无遮挡，背景简洁。</li>
                    <li>远景先裁剪主体。</li>
                  </>
                )}
              </ul>
            </Card>
          </section>
        </div>
      </main>
    </div>
  );
}
