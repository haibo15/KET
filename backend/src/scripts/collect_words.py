import os
import json
import time
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.operations import UpdateOne
from datetime import datetime
from openai import OpenAI  # 使用OpenAI SDK调用Deepseek API

# 加载环境变量
load_dotenv()

# MongoDB配置
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'ket_exam')

# Deepseek API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# 初始化OpenAI客户端(用于调用Deepseek API)
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"  # Deepseek API的基础URL
)

# 词汇主题
VOCABULARY_TOPICS = {
    "personal": "个人信息相关词汇(姓名、年龄、家庭、爱好等)",
    "daily": "日常生活词汇(食物、衣服、天气、时间等)",
    "education": "教育学习词汇(学校、课程、学习、老师等)",
    "work": "工作职业词汇(工作、办公室、会议、商务等)",
    "transport": "交通出行词汇(公交、火车、票务、旅行等)",
    "leisure": "休闲娱乐词汇(运动、音乐、电影、假期等)",
    "shopping": "购物消费词汇(商店、价格、金钱、购买等)",
    "health": "健康医疗词汇(医院、医生、疾病、药品等)",
    "technology": "科技通讯词汇(电脑、手机、网络、邮件等)",
    "services": "服务设施词汇(银行、邮局、餐厅、酒店等)"
}

class VocabularyCollector:
    def __init__(self):
        try:
            # 连接MongoDB
            print("正在连接MongoDB数据库...")
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[DB_NAME]
            self.words_collection = self.db.words
            
            # 测试连接
            self.client.server_info()
            print("MongoDB连接成功!")

            # 确保索引
            print("正在创建数据库索引...")
            self.words_collection.create_index([("english", 1)], unique=True)
            self.words_collection.create_index([("frequency", -1)])
            self.words_collection.create_index([("level", 1)])
            self.words_collection.create_index([("tags", 1)])
            print("数据库索引创建完成!")
            
            # 初始化计数器
            self.total_collected = 0
            self.total_saved = 0
            self.start_time = datetime.now()
            
        except Exception as e:
            print(f"数据库连接错误: {str(e)}")
            raise

    def print_progress(self):
        """打印总体进度"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        words_per_second = self.total_collected / elapsed if elapsed > 0 else 0
        
        print("\n当前总进度:")
        print(f"已收集词汇: {self.total_collected} 个")
        print(f"已保存词汇: {self.total_saved} 个")
        print(f"运行时间: {elapsed:.1f}秒")
        print(f"平均速度: {words_per_second:.1f}个/秒")

    def collect_words_for_topic(self, topic: str, description: str) -> list:
        """收集特定主题的词汇"""
        all_words = []
        
        # 分批次收集词汇,每批次更大以提高效率
        categories = [
            ("基础核心词汇", "频率最高的基础词汇,适合初学者", 150),  # 增加每批次的词汇量
            ("进阶词汇", "中等难度的常用词汇", 100),
            ("主题专业词汇", f"与{description}相关的专业词汇", 50)
        ]
        
        total_categories = len(categories)
        for category_index, (category, cat_desc, target_count) in enumerate(categories, 1):
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 正在收集 {topic} - {category} ({category_index}/{total_categories})")
            print(f"目标词汇量: {target_count}个")
            
            prompt = f"""请为KET考试(A2级别)生成{topic}主题的{category}。
要求:
1. 生成{target_count}个该主题最常用的词汇
2. 词汇分类要求:
   - {category}({cat_desc})
   - 确保词汇难度符合KET考试要求(A1-A2)
   - 避免重复词汇
3. 主题描述: {description}

请按以下Python格式返回词汇列表(一次性返回所有词汇,不要分批):

words = [
    {{
        "english": "name",  # 英文单词
        "chinese": "名字",  # 中文翻译
        "phonetic": "/neɪm/",  # 音标
        "pos": "n.",  # 词性
        "level": 1,  # 1=A1, 2=A2
        "frequency": 95,  # 使用频率1-100
        "examples": [
            "What's your name?",
            "My name is John."
        ],
        "tags": ["personal", "basic"]  # 标签
    }},
    # ... 更多词汇 ...
]

直接返回Python代码,不要加任何其他说明。确保一次性返回所有词汇。"""

            try:
                print("正在调用Deepseek API...")
                start_time = time.time()
                
                # 使用OpenAI SDK调用Deepseek API
                response = client.chat.completions.create(
                    model="deepseek-chat",  # 使用最新的DeepSeek-V3模型
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=8000,  # 增加token限制
                    response_format={"type": "text"},  # 确保返回文本格式
                    timeout=30  # 添加超时设置
                )
                
                content = response.choices[0].message.content
                
                # 清理返回的内容
                content = content.strip()
                if content.startswith('```python'):
                    content = content.split('```python')[1]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                # 提取words变量
                try:
                    local_vars = {}
                    exec(content, {}, local_vars)
                    words = local_vars.get('words', [])
                    
                    if not isinstance(words, list):
                        print("API返回格式错误: 预期Python列表")
                        continue
                        
                except Exception as e:
                    print(f"Python代码执行错误: {str(e)}")
                    continue
                
                # 验证每个词条的格式
                valid_words = []
                for word in words:
                    try:
                        # 验证必要字段
                        required_fields = ["english", "chinese", "phonetic", "pos", "level", "frequency", "examples", "tags"]
                        if not all(field in word for field in required_fields):
                            continue
                        
                        # 验证数据类型
                        if not isinstance(word["level"], (int, float)) or word["level"] not in [1, 2]:
                            word["level"] = 1 if word.get("frequency", 0) >= 90 else 2
                        
                        if not isinstance(word["frequency"], (int, float)):
                            word["frequency"] = 90 if word.get("level", 2) == 1 else 70
                        
                        # 标准化格式
                        word["level"] = int(word["level"])
                        word["frequency"] = int(word["frequency"])
                        if not word["phonetic"].startswith("/"):
                            word["phonetic"] = "/" + word["phonetic"]
                        if not word["phonetic"].endswith("/"):
                            word["phonetic"] = word["phonetic"] + "/"
                            
                        valid_words.append(word)
                    except Exception as e:
                        continue
                
                # 添加主题标签和类别标签
                for word in valid_words:
                    if 'tags' not in word:
                        word['tags'] = []
                    word['tags'].extend([topic, category])
                
                all_words.extend(valid_words)
                self.total_collected += len(valid_words)
                
                elapsed_time = time.time() - start_time
                print(f"✓ 成功收集 {len(valid_words)}/{target_count} 个有效词汇 (用时: {elapsed_time:.1f}秒)")
                
                # 显示一些示例词汇
                if valid_words:
                    print("\n示例词汇:")
                    for word in valid_words[:3]:
                        print(f"- {word['english']}: {word['chinese']} [{word['phonetic']}] ({word['pos']})")
                
                # 打印总进度
                self.print_progress()
                
                # 添加较短的延迟
                if category_index < total_categories:
                    print("\n等待1秒后继续...")
                    time.sleep(1)
                
            except Exception as e:
                print(f"发生错误: {str(e)}")
                continue
        
        return all_words

    def save_to_database(self, words: list):
        """保存词汇到数据库"""
        if not words:
            return
            
        try:
            print(f"\n正在保存 {len(words)} 个词汇到数据库...")
            start_time = time.time()
            
            # 批量更新以提高性能
            operations = []
            for word in words:
                operations.append(
                    UpdateOne(
                        {"english": word["english"]},
                        {"$set": word},
                        upsert=True
                    )
                )
            
            if operations:
                result = self.words_collection.bulk_write(operations)
                self.total_saved += result.upserted_count + result.modified_count
                elapsed_time = time.time() - start_time
                print(f"✓ 保存完成! 更新: {result.modified_count}, 新增: {result.upserted_count} (用时: {elapsed_time:.1f}秒)")
                
        except Exception as e:
            print(f"数据库保存错误: {str(e)}")

    def collect(self):
        """收集所有主题的词汇"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 开始收集词汇...")
        print("计划收集词汇:")
        print("- 基础核心词汇: 每主题150个")
        print("- 进阶词汇: 每主题100个")
        print("- 主题专业词汇: 每主题50个")
        print(f"共 {len(VOCABULARY_TOPICS)} 个主题,预计总词汇量: {len(VOCABULARY_TOPICS) * 300}个")
        
        total_topics = len(VOCABULARY_TOPICS)
        for topic_index, (topic, description) in enumerate(VOCABULARY_TOPICS.items(), 1):
            print(f"\n{'='*50}")
            print(f"主题进度: {topic_index}/{total_topics}")
            print(f"当前主题: {topic}")
            print(f"描述: {description}")
            print('='*50)
            
            words = self.collect_words_for_topic(topic, description)
            
            if words:
                self.save_to_database(words)
            
            if topic_index < total_topics:
                print("\n等待1秒后继续下一个主题...")
                time.sleep(1)
        
        # 最终统计
        try:
            total_words = self.words_collection.count_documents({})
            core_words = self.words_collection.count_documents({"tags": "基础核心词汇"})
            advanced_words = self.words_collection.count_documents({"tags": "进阶词汇"})
            special_words = self.words_collection.count_documents({"tags": "主题专业词汇"})
            
            print("\n最终统计:")
            print(f"计划收集: {len(VOCABULARY_TOPICS) * 300}个词汇")
            print(f"实际收集: {self.total_collected}个词汇")
            print(f"成功保存: {self.total_saved}个词汇")
            print(f"数据库中总词汇量: {total_words}个")
            print(f"- 基础核心词汇: {core_words}个")
            print(f"- 进阶词汇: {advanced_words}个")
            print(f"- 主题专业词汇: {special_words}个")
            
            # 按主题统计
            print("\n各主题词汇统计:")
            for topic in VOCABULARY_TOPICS.keys():
                count = self.words_collection.count_documents({"tags": topic})
                print(f"{topic}: {count}个词汇")
            
            # 计算总用时和平均速度
            total_time = (datetime.now() - self.start_time).total_seconds()
            avg_speed = self.total_collected / total_time if total_time > 0 else 0
            print(f"\n总用时: {total_time:.1f}秒")
            print(f"平均速度: {avg_speed:.1f}个/秒")
                
        except Exception as e:
            print(f"统计信息获取失败: {str(e)}")

if __name__ == "__main__":
    try:
        collector = VocabularyCollector()
        collector.collect()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")
    finally:
        print("\n程序结束") 