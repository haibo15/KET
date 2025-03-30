from typing import Optional, Dict, List, Set
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    progress: Dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class Word(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    word: str
    translation: str
    phonetic: Optional[str] = None  # 音标
    part_of_speech: str  # 词性 (n, v, adj等)
    frequency: int = 0  # 使用频率(1-100)
    examples: List[Dict[str, str]] = Field(default_factory=list)  # [{en: "example", zh: "翻译"}]
    difficulty_level: str = "A"  # A, B, C级
    topics: List[str] = Field(default_factory=list)  # 主题标签
    usage_count: int = 0
    last_review_time: Optional[datetime] = None
    next_review_time: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class LearningRecord(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    type: str  # "vocab", "sentence", "reading"
    content_id: PyObjectId
    score: float
    time_spent: int  # 以秒为单位
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class LearningProgress(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    word_id: PyObjectId
    mastery_level: int = 0  # 0-5, 0表示未学习, 5表示完全掌握
    review_count: int = 0
    last_review_time: Optional[datetime] = None
    next_review_time: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class TopicCategory(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    word_count: int = 0
    parent_category: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class LearningSession(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    words_studied: List[PyObjectId] = Field(default_factory=list)
    words_reviewed: List[PyObjectId] = Field(default_factory=list)
    session_type: str  # "study" or "review"
    topic_category: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class Topic(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str  # 英文名
    name_zh: str  # 中文名
    description: Optional[str] = None
    word_count: int = 0
    target_count: int = 300  # 目标词汇量
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# 新的主题分类
TOPICS = {
    "Personal Information": "个人信息",
    "Daily Life": "日常生活",
    "Education": "教育学习",
    "Work": "工作职业",
    "Transportation": "交通出行",
    "Entertainment": "休闲娱乐",
    "Shopping": "购物消费",
    "Health": "健康医疗",
    "Technology": "科技通讯",
    "Services": "服务设施"
}
