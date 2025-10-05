export interface BreedItem { label:string; zh?:string; score:number }
export interface BreedResp { topk:BreedItem[]; unknown:boolean; time_ms:number }
