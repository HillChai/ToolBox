export interface ASRSegment { t0:number; t1:number; text:string }
export interface ASRResp { text:string; segments:ASRSegment[]; time_ms:number }
