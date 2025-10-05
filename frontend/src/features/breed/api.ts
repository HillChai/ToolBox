import { postForm } from "../../lib/http"; import type { BreedResp } from "../../types/breed";
export async function classify(file:File, topk=5){
  const fd=new FormData(); fd.append("file",file); return postForm<BreedResp>(`/breed?topk=${topk}`, fd);
}
