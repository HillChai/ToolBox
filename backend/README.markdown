# AI Backend (OCR / ASR / Cat-Dog)

接口清单：

- `GET /api/health` 健康检查
- `POST /api/files/upload` 上传（图片/音频），返回 `path`
- `POST /api/ocr/extract` OCR，入参：`file` 或 `?path=`，可选 `lang=eng|chi_sim|eng+chi_sim`
- `POST /api/asr/transcribe` 语音转文字，入参：`file` 或 `?path=`，可选 `model_size=base`、`language=zh|en|...`
- `POST /api/vision/cat-dog` 猫狗品种/类别识别，入参：`file` 或 `?path=`

## 本地运行

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## 前端对接

// 1) 上传

```js
const form = new FormData();
form.append("file", file);
const info = await fetch("http://localhost:8000/api/files/upload", {
  method: "POST",
  body: form,
}).then((r) => r.json());
```

// 2) OCR

```js
const ocr = await fetch(
  `http://localhost:8000/api/ocr/extract?path=${encodeURIComponent(
    info.path
  )}&lang=eng+chi_sim`,
  { method: "POST" }
).then((r) => r.json());
```

// 3) ASR（先在 .env 设置 ASR_BACKEND=faster_whisper）

```js
const asr = await fetch(
  `http://localhost:8000/api/asr/transcribe?path=${encodeURIComponent(
    info.path
  )}&model_size=base`,
  { method: "POST" }
).then((r) => r.json());
```

// 4) 猫狗识别

```js
const res = await fetch(
  `http://localhost:8000/api/vision/cat-dog?path=${encodeURIComponent(
    info.path
  )}`,
  { method: "POST" }
).then((r) => r.json());
```
