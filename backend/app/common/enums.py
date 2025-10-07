from enum import Enum

# --- 任务类型表 ---
class TaskKind(str, Enum):
    ocr = "ocr"         # 图片文字识别
    vision = "vision"   # 猫狗品种识别
    asr = "asr"         # 语音转文字
    
    
# --- 媒体类型表 ---
class MediaKind(str, Enum):
    image = "image"
    audio = "audio"
    
    
# --- 任务状态表 ---
class TaskStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    succeeded = "succeeded"
    failed = "failed"