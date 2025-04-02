from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
import json
from pathlib import Path
import logging
import os
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VocabularyImporter:
    def __init__(self):
        # MongoDB连接配置
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['ket']
        
        # 定义集合
        self.words = self.db['words']
        self.examples = self.db['examples']
        self.phrases = self.db['phrases']
        self.topics = self.db['topics']
        self.categories = self.db['categories']
        
    def setup_database(self):
        """设置数据库索引和约束"""
        # 删除现有集合
        self.categories.drop()
        self.words.drop()
        self.examples.drop()
        self.phrases.drop()
        self.topics.drop()
        
        # 创建索引
        self.words.create_index([("word", 1)], unique=True)
        self.topics.create_index([("name", 1)], unique=True)
        self.categories.create_index([("name", 1)], unique=True)
        
        # 为关联字段创建索引
        self.examples.create_index([("word", 1)])
        self.phrases.create_index([("word", 1)])
        self.words.create_index([("category_id", 1)])
        self.words.create_index([("topic_ids", 1)])
        
        logger.info("数据库初始化完成")
        
    def insert_category(self, category_data):
        """插入或更新类别，返回类别ID"""
        result = self.categories.update_one(
            {"name": category_data["name"]},
            {"$set": category_data},
            upsert=True
        )
        
        if result.upserted_id:
            return result.upserted_id
        else:
            return self.categories.find_one({"name": category_data["name"]})["_id"]
            
    def insert_word(self, word_data, category_id):
        """插入词汇数据"""
        try:
            word = {
                "word": word_data["word"],
                "translation": word_data["translation"],
                "phonetic": word_data["phonetic"],
                "part_of_speech": word_data["part_of_speech"],
                "frequency": word_data["frequency"],
                "difficulty_level": word_data["difficulty_level"],
                "category_id": category_id,
                "related_words": word_data.get("related_words", []),
                "topics": word_data.get("topics", []),
                "source_file": word_data.get("source_file", ""),
                "updated_at": datetime.utcnow()
            }
            result = self.words.insert_one(word)
            return result.inserted_id
        except Exception as e:
            logger.error(f"插入词汇失败 {word_data['word']}: {str(e)}")
            return None
            
    def insert_examples(self, word_id, examples):
        """插入例句数据"""
        try:
            if not examples:
                return
            
            example_docs = [{
                "word_id": word_id,
                "en": example["en"],
                "zh": example["zh"]
            } for example in examples]
            
            self.examples.insert_many(example_docs)
        except Exception as e:
            logger.error(f"插入例句失败: {str(e)}")
            
    def insert_phrases(self, word_id, phrases):
        """插入短语数据"""
        try:
            if not phrases:
                return
                
            phrase_docs = [{
                "word_id": word_id,
                "phrase": phrase["phrase"],
                "translation": phrase["translation"],
                "difficulty": phrase["difficulty"]
            } for phrase in phrases]
            
            self.phrases.insert_many(phrase_docs)
        except Exception as e:
            logger.error(f"插入短语失败: {str(e)}")
            
    def process_topics(self, word, topics):
        """处理主题数据，返回topic_ids"""
        topic_ids = []
        try:
            for topic in topics:
                # 插入或更新主题
                result = self.topics.update_one(
                    {"name": topic},
                    {
                        "$set": {
                            "name": topic,
                            "updated_at": datetime.utcnow()
                        },
                        "$addToSet": {"words": word}  # 添加单词到主题的words数组
                    },
                    upsert=True
                )
                
                # 获取主题ID
                if result.upserted_id:
                    topic_id = result.upserted_id
                else:
                    topic_id = self.topics.find_one({"name": topic})["_id"]
                
                topic_ids.append(topic_id)
                
            return topic_ids
        except Exception as e:
            logger.error(f"处理主题失败: {str(e)}")
            return []
            
    def process_file(self, file_path):
        """处理单个JSON文件"""
        logger.info(f"正在处理文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 获取文件名（不含扩展名）作为类别名
            category_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # 插入或更新类别
            category_id = self.insert_category({
                "name": category_name,
                "name_cn": data.get("metadata", {}).get("category_cn", ""),
                "word_count": data.get("metadata", {}).get("word_count", 0),
                "difficulty_distribution": data.get("metadata", {}).get("difficulty_distribution", {})
            })

            # 处理词汇
            words_data = data.get("words", {})
            operations = []
            for word, word_data in words_data.items():
                # 处理主题并获取topic_ids
                topic_ids = self.process_topics(word, word_data.get("topics", []))
                
                word_doc = {
                    "word": word,
                    "translation": word_data.get("translation", ""),
                    "phonetic": word_data.get("phonetic", ""),
                    "part_of_speech": word_data.get("part_of_speech", ""),
                    "frequency": word_data.get("frequency", 0),
                    "difficulty_level": word_data.get("difficulty_level", ""),
                    "category_id": category_id,
                    "topic_ids": topic_ids,
                    "related_words": word_data.get("related_words", []),
                    "source_file": category_name,
                    "updated_at": datetime.utcnow()
                }
                
                # 创建更新操作
                operations.append(
                    UpdateOne(
                        {"word": word},
                        {"$set": word_doc},
                        upsert=True
                    )
                )

                # 处理例句
                if "examples" in word_data:
                    for example in word_data["examples"]:
                        self.examples.update_one(
                            {"word": word, "en": example.get("en", "")},
                            {"$set": {
                                "word": word,
                                "en": example.get("en", ""),
                                "zh": example.get("zh", ""),
                                "updated_at": datetime.utcnow()
                            }},
                            upsert=True
                        )

                # 处理短语
                if "phrases" in word_data:
                    for phrase in word_data["phrases"]:
                        self.phrases.update_one(
                            {"word": word, "phrase": phrase.get("phrase", "")},
                            {"$set": {
                                "word": word,
                                "phrase": phrase.get("phrase", ""),
                                "translation": phrase.get("translation", ""),
                                "difficulty": phrase.get("difficulty", ""),
                                "updated_at": datetime.utcnow()
                            }},
                            upsert=True
                        )

            # 批量执行单词更新操作
            if operations:
                try:
                    self.words.bulk_write(operations, ordered=False)
                except BulkWriteError as bwe:
                    logger.warning(f"部分单词更新失败: {bwe.details}")

            logger.info(f"文件处理完成: {file_path}")

        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
            
    def import_all_data(self):
        """导入所有数据"""
        try:
            # 设置数据库
            self.setup_database()
            
            # 获取所有JSON文件
            json_dir = Path("../DOC/vocabulary_data/JSON")
            json_files = list(json_dir.glob("*.json"))
            
            logger.info(f"找到 {len(json_files)} 个JSON文件")
            
            # 处理所有文件
            for json_file in json_files:
                self.process_file(json_file)
                
            logger.info("所有数据导入完成")
            
        except Exception as e:
            logger.error(f"导入过程失败: {str(e)}")
            
if __name__ == "__main__":
    importer = VocabularyImporter()
    importer.import_all_data() 