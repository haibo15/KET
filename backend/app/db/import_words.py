import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict
from models import Word, Topic, TOPICS
from word_parser import WordParser
from translator import MockTranslator  # 暂时使用模拟翻译器

# MongoDB连接配置
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "ket_system"

# 原主题到新主题的映射
TOPIC_MAPPING = {
    # 个人信息
    "Family and Friends": "Personal Information",
    "Personal Feelings, Opinions and Experiences": "Personal Information",
    
    # 日常生活
    "House and Home": "Daily Life",
    "Food and Drink": "Daily Life",
    "Clothes and Accessories": "Daily Life",
    "Weather": "Daily Life",
    "Time": "Daily Life",
    
    # 教育学习
    "Education": "Education",
    "Documents and Texts": "Education",
    
    # 工作职业
    "Work and Jobs": "Work",
    
    # 交通出行
    "Travel and Transport": "Transportation",
    "Places: Town and City": "Transportation",
    "Places: Countryside": "Transportation",
    
    # 休闲娱乐
    "Entertainment and Media": "Entertainment",
    "Hobbies and Leisure": "Entertainment",
    "Sport": "Entertainment",
    
    # 购物消费
    "Shopping": "Shopping",
    
    # 健康医疗
    "Health, Medicine and Exercise": "Health",
    
    # 科技通讯
    "Communication and Technology": "Technology",
    "Appliances": "Technology",
    
    # 服务设施
    "Services": "Services",
    "Places: Buildings": "Services"
}

async def connect_to_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    return db

async def import_topics(db) -> None:
    """导入新的主题分类"""
    collection = db.topics
    for eng_name, zh_name in TOPICS.items():
        topic = {
            "name": eng_name,
            "name_zh": zh_name,
            "word_count": 0,
            "target_count": 300
        }
        await collection.update_one(
            {"name": eng_name},
            {"$set": topic},
            upsert=True
        )
    print("主题分类导入完成")

async def import_words(db, words_data: List[Dict]) -> None:
    """导入单词数据"""
    collection = db.words
    translator = MockTranslator()  # 创建翻译器实例
    
    for word_data in words_data:
        # 获取翻译数据
        trans_data = await translator.translate(word_data["word"])
        
        # 映射主题分类
        old_topics = word_data.get("topic_categories", [])
        new_topics = set()
        for old_topic in old_topics:
            if old_topic in TOPIC_MAPPING:
                new_topics.add(TOPIC_MAPPING[old_topic])
        
        # 准备单词数据
        word_doc = {
            "word": word_data["word"],
            "translation": trans_data["translation"],
            "phonetic": trans_data["phonetic"],
            "part_of_speech": word_data["part_of_speech"],
            "frequency": 0,  # TODO: 需要添加频率数据
            "examples": trans_data["examples"] or [{"en": ex, "zh": ""} for ex in word_data.get("examples", [])],
            "difficulty_level": word_data.get("difficulty_level", "A"),
            "topics": list(new_topics)
        }
        
        # 更新主题的单词计数
        for topic in new_topics:
            await db.topics.update_one(
                {"name": topic},
                {"$inc": {"word_count": 1}}
            )
        
        # 导入单词
        await collection.update_one(
            {"word": word_data["word"]},
            {"$set": word_doc},
            upsert=True
        )
        
        # 打印进度
        print(f"已处理: {word_data['word']}")
    
    print(f"导入了 {len(words_data)} 个单词")

async def main():
    # 读取词汇列表文件
    vocab_file = "../../DOC/ket-schools-vocabulary-list.md"
    if not os.path.exists(vocab_file):
        print(f"找不到词汇列表文件: {vocab_file}")
        return
        
    with open(vocab_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析词汇
    parser = WordParser()
    words_data = parser.parse_file(content)
    
    # 连接数据库并导入数据
    db = await connect_to_db()
    
    # 导入主题分类
    await import_topics(db)
    
    # 导入单词
    await import_words(db, words_data)
    
    print("数据导入完成")

if __name__ == "__main__":
    asyncio.run(main()) 