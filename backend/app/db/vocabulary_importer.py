import json
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, List
from models import Word, Topic, TOPICS

# MongoDB连接配置
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "ket_system"

class VocabularyImporter:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """连接到MongoDB"""
        self.client = AsyncIOMotorClient(MONGODB_URL)
        self.db = self.client[DATABASE_NAME]
        
    async def close(self):
        """关闭数据库连接"""
        if self.client:
            self.client.close()
            
    async def import_topics(self):
        """导入主题分类"""
        collection = self.db.topics
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
            
    async def import_vocabulary(self, vocab_data: Dict):
        """导入词汇数据"""
        collection = self.db.words
        imported_count = 0
        
        # 重置主题单词计数
        await self.db.topics.update_many(
            {},
            {"$set": {"word_count": 0}}
        )
        
        # 导入每个主题下的单词
        for topic, words in vocab_data.items():
            for word_key, word_data in words.items():
                # 导入单词
                await collection.update_one(
                    {"word": word_data["word"]},
                    {"$set": word_data},
                    upsert=True
                )
                
                # 更新主题的单词计数
                for topic_name in word_data["topics"]:
                    await self.db.topics.update_one(
                        {"name": topic_name},
                        {"$inc": {"word_count": 1}}
                    )
                    
                imported_count += 1
                if imported_count % 10 == 0:
                    print(f"已导入 {imported_count} 个单词")
                    
        print(f"总共导入了 {imported_count} 个单词")
        
    async def validate_data(self):
        """验证导入的数据"""
        # 检查单词总数
        word_count = await self.db.words.count_documents({})
        print(f"数据库中共有 {word_count} 个单词")
        
        # 检查每个主题的单词数
        async for topic in self.db.topics.find():
            print(f"主题 '{topic['name']}' 包含 {topic['word_count']} 个单词")
            
        # 检查单词完整性
        incomplete_words = []
        async for word in self.db.words.find(
            {
                "$or": [
                    {"translation": {"$exists": False}},
                    {"phonetic": {"$exists": False}},
                    {"examples": {"$size": 0}},
                    {"topics": {"$size": 0}}
                ]
            }
        ):
            incomplete_words.append(word["word"])
            
        if incomplete_words:
            print("以下单词信息不完整：")
            for word in incomplete_words:
                print(f"- {word}")
        else:
            print("所有单词信息完整")

async def main():
    # 读取词汇数据
    with open("../../DOC/vocabulary_data.json", "r", encoding="utf-8") as f:
        vocab_data = json.load(f)
        
    # 创建导入器
    importer = VocabularyImporter()
    await importer.connect()
    
    try:
        # 导入主题
        await importer.import_topics()
        
        # 导入词汇
        await importer.import_vocabulary(vocab_data)
        
        # 验证数据
        await importer.validate_data()
        
    finally:
        await importer.close()

if __name__ == "__main__":
    asyncio.run(main()) 