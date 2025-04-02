from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class VocabularyBase(BaseModel):
    word: str
    translation: str
    phonetic: Optional[str] = None
    part_of_speech: Optional[str] = None
    frequency: Optional[int] = 0
    difficulty_level: Optional[str] = None
    topics: List[str] = []
    related_words: List[str] = []

class VocabularyCreate(VocabularyBase):
    category_id: Optional[str] = None
    source_file: Optional[str] = None

class VocabularyUpdate(BaseModel):
    translation: Optional[str] = None
    phonetic: Optional[str] = None
    part_of_speech: Optional[str] = None
    frequency: Optional[int] = None
    difficulty_level: Optional[str] = None
    topics: Optional[List[str]] = None
    related_words: Optional[List[str]] = None

class VocabularyInDB(VocabularyBase):
    id: str = Field(alias="_id")
    category_id: Optional[str] = None
    source_file: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        } 