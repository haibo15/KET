from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from ....core.database import get_database
from ....schemas.vocabulary import (
    VocabularyBase,
    VocabularyCreate,
    VocabularyInDB,
    VocabularyUpdate
)

router = APIRouter()

@router.get("/", response_model=List[VocabularyInDB])
async def get_vocabulary_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """
    获取词汇列表，支持分页和过滤。
    """
    query = {}
    if topic:
        query["topics"] = topic
    if difficulty:
        query["difficulty_level"] = difficulty
        
    cursor = db.words.find(query).skip(skip).limit(limit)
    words = await cursor.to_list(length=limit)
    return words

@router.get("/{word}", response_model=VocabularyInDB)
async def get_vocabulary_detail(
    word: str,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """
    获取单个词汇的详细信息。
    """
    word_doc = await db.words.find_one({"word": word})
    if not word_doc:
        raise HTTPException(status_code=404, detail="Word not found")
    return word_doc

@router.get("/search/{query}", response_model=List[VocabularyInDB])
async def search_vocabulary(
    query: str,
    limit: int = Query(10, ge=1, le=100),
    db: AsyncIOMotorClient = Depends(get_database)
):
    """
    搜索词汇。
    """
    # 创建文本索引
    await db.words.create_index([("word", "text"), ("translation", "text")])
    
    # 执行搜索
    cursor = db.words.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(limit)
    
    results = await cursor.to_list(length=limit)
    return results

@router.get("/topic/{topic}", response_model=List[VocabularyInDB])
async def get_vocabulary_by_topic(
    topic: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncIOMotorClient = Depends(get_database)
):
    """
    获取指定主题的词汇列表。
    """
    cursor = db.words.find({"topics": topic}).skip(skip).limit(limit)
    words = await cursor.to_list(length=limit)
    return words 