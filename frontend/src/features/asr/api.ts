import { postForm } from "../../lib/http";
import type { ASRResp } from "../../types/asr";
export async function transcribe(file:File, lang="auto"){
  const fd = new FormData(); fd.append("file",file); fd.append("lang",lang);
  return postForm<ASRResp>("/asr", fd);
}
