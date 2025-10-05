import { postForm } from "../../lib/http"; import type { OCRResp } from "../../types/ocr";
export async function ocr(file:File){ const fd=new FormData(); fd.append("file",file); return postForm<OCRResp>("/ocr", fd); }
