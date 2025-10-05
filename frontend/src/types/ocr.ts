export interface OCRLine { box:number[][]; text:string; score:number }
export interface OCRResp { text:string; lines:OCRLine[]; time_ms:number }
