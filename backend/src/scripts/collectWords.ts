import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { IWord } from '../models/Word';
import dotenv from 'dotenv';

dotenv.config();

// Deepseek API配置
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';

// 词汇主题
const VOCABULARY_TOPICS = {
  personal: "个人信息相关词汇(姓名、年龄、家庭、爱好等)",
  daily: "日常生活词汇(食物、衣服、天气、时间等)",
  education: "教育学习词汇(学校、课程、学习、老师等)",
  work: "工作职业词汇(工作、办公室、会议、商务等)",
  transport: "交通出行词汇(公交、火车、票务、旅行等)",
  leisure: "休闲娱乐词汇(运动、音乐、电影、假期等)",
  shopping: "购物消费词汇(商店、价格、金钱、购买等)",
  health: "健康医疗词汇(医院、医生、疾病、药品等)",
  technology: "科技通讯词汇(电脑、手机、网络、邮件等)",
  services: "服务设施词汇(银行、邮局、餐厅、酒店等)"
};

// 预定义的词汇数据
const PREDEFINED_WORDS = {
  personal: [
    {
      english: "name",
      chinese: "名字",
      phonetic: "neɪm",
      pos: "noun",
      level: 1,
      frequency: 98,
      examples: ["What's your name?", "My name is John."],
      tags: ["core", "personal-info", "A1"]
    },
    {
      english: "age",
      chinese: "年龄",
      phonetic: "eɪdʒ",
      pos: "noun",
      level: 1,
      frequency: 95,
      examples: ["What's your age?", "I am 20 years old."],
      tags: ["core", "personal-info", "A1"]
    }
  ],
  daily: [
    {
      english: "breakfast",
      chinese: "早餐",
      phonetic: "ˈbrekfəst",
      pos: "noun",
      level: 1,
      frequency: 92,
      examples: ["What do you have for breakfast?", "I had eggs for breakfast."],
      tags: ["core", "food", "A1"]
    },
    {
      english: "weather",
      chinese: "天气",
      phonetic: "ˈweðə(r)",
      pos: "noun",
      level: 1,
      frequency: 90,
      examples: ["How's the weather today?", "The weather is nice."],
      tags: ["core", "daily-life", "A1"]
    }
  ]
};

class VocabularyCollector {
  private async collectWordsForTopic(topic: string, description: string): Promise<IWord[]> {
    try {
      const prompt = `请为KET考试(A2级别)生成${topic}主题的词汇列表。每个词条需要包含以下信息,直接返回JSON数组格式:
[
  {
    "english": "单词",
    "chinese": "翻译",
    "phonetic": "音标",
    "pos": "词性",
    "level": 数字(1表示A1,2表示A2),
    "frequency": 数字(1-100),
    "examples": ["例句1", "例句2"],
    "tags": ["标签1", "标签2"]
  }
]

要求:
1. 生成50个该主题最常用的词汇
2. 词汇分类:
   - 核心词汇(频率>=90)
   - 高频词汇(频率80-89)
   - 扩展词汇(频率<80)
3. 主题描述: ${description}
4. 确保返回的是标准JSON格式`;

      const response = await axios.post(
        DEEPSEEK_API_URL,
        {
          model: "deepseek-chat",
          messages: [{ role: "user", content: prompt }],
          temperature: 0.7,
          max_tokens: 3000,
          stop: null
        },
        {
          headers: {
            'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
            'Content-Type': 'application/json'
          }
        }
      );

      let content = response.data.choices[0].message.content;
      
      // 清理返回的内容,确保是有效的JSON
      content = content.replace(/```json\n?/g, '').replace(/```\n?/g, '');
      content = content.trim();
      
      // 解析JSON
      let words = JSON.parse(content);

      // 如果API返回失败,使用预定义的词汇
      if (!Array.isArray(words) || words.length === 0) {
        console.log(`Using predefined words for topic: ${topic}`);
        words = PREDEFINED_WORDS[topic] || [];
      }

      return words;
    } catch (error) {
      console.error(`Error collecting words for topic ${topic}:`, error);
      // 返回预定义的词汇
      return PREDEFINED_WORDS[topic] || [];
    }
  }

  private async saveToFile(words: IWord[], topic: string): Promise<void> {
    try {
      const dirPath = path.join(__dirname, '../data/vocabulary');
      const filePath = path.join(dirPath, `${topic}.json`);
      
      // 确保目录存在
      await fs.promises.mkdir(dirPath, { recursive: true });
      
      // 保存文件
      await fs.promises.writeFile(filePath, JSON.stringify(words, null, 2));
      console.log(`Words saved to ${filePath}`);
    } catch (error) {
      console.error(`Error saving words for topic ${topic}:`, error);
    }
  }

  public async collect(): Promise<void> {
    console.log('Starting vocabulary collection...');
    
    for (const [topic, description] of Object.entries(VOCABULARY_TOPICS)) {
      console.log(`Collecting words for topic: ${topic}`);
      const words = await this.collectWordsForTopic(topic, description);
      
      if (words.length > 0) {
        await this.saveToFile(words, topic);
        console.log(`Collected ${words.length} words for topic ${topic}`);
      }

      // 添加延迟以避免API限制
      await new Promise(resolve => setTimeout(resolve, 3000));
    }

    console.log('Vocabulary collection completed');
  }

  // 合并所有主题的词汇
  public async mergeAllTopics(): Promise<void> {
    try {
      const allWords: IWord[] = [];
      const vocabDir = path.join(__dirname, '../data/vocabulary');
      
      // 确保目录存在
      await fs.promises.mkdir(vocabDir, { recursive: true });
      
      const files = await fs.promises.readdir(vocabDir);
      for (const file of files) {
        if (file.endsWith('.json')) {
          const content = await fs.promises.readFile(path.join(vocabDir, file), 'utf-8');
          const words = JSON.parse(content);
          allWords.push(...words);
        }
      }

      // 按频率分类
      const categorizedWords = {
        core: allWords.filter(w => w.frequency >= 90),
        highFrequency: allWords.filter(w => w.frequency >= 80 && w.frequency < 90),
        extended: allWords.filter(w => w.frequency < 80)
      };

      // 保存分类结果
      const outputPath = path.join(__dirname, '../data/ket_vocabulary.ts');
      const output = `import { IWord } from '../models/Word';

// 核心词汇 (Core Vocabulary)
export const coreWords: Partial<IWord>[] = ${JSON.stringify(categorizedWords.core, null, 2)};

// 高频词汇 (High Frequency Vocabulary)
export const highFrequencyWords: Partial<IWord>[] = ${JSON.stringify(categorizedWords.highFrequency, null, 2)};

// 扩展词汇 (Extended Vocabulary)
export const extendedWords: Partial<IWord>[] = ${JSON.stringify(categorizedWords.extended, null, 2)};

// 词汇主题分类
export const vocabularyTopics = ${JSON.stringify(VOCABULARY_TOPICS, null, 2)};`;

      await fs.promises.writeFile(outputPath, output);
      console.log(`All words merged and saved to ${outputPath}`);
    } catch (error) {
      console.error('Error merging topics:', error);
    }
  }
}

// 运行收集器
async function main() {
  const collector = new VocabularyCollector();
  await collector.collect();
  await collector.mergeAllTopics();
}

main().catch(console.error); 