# 词汇模板使用说明

## 文件结构说明

### 1. metadata部分
- `category`：填写词汇类别的英文名称
- `category_cn`：填写词汇类别的中文名称
- `word_count`：该类别包含的词汇数量
- `difficulty_distribution`：各难度等级词汇的百分比分布

### 2. words部分
将"word_example"替换为实际的单词，每个单词需包含以下信息：
- `word`：英文单词
- `translation`：中文翻译
- `phonetic`：音标
- `part_of_speech`：词性(n/v/adj/adv等，可以是组合如 'n & v')
- `frequency`：使用频率(50-100)
- `examples`：至少2个例句（包含英文和中文翻译）
- `difficulty_level`：难度等级(A/B/C)
- `topics`：相关主题标签
- `category`：所属类别(中文)
- `related_words`：相关词汇
- `phrases`：相关短语（包含短语原文、翻译和难度等级）

## 难度等级说明
- A级：KET考试核心词汇，使用频率最高
- B级：KET考试重要词汇，使用频率中等
- C级：KET考试扩展词汇，使用频率较低

## 使用频率分数说明(50-100)
- 90-100：最常用核心词汇
- 80-89：常用重要词汇
- 70-79：较常用词汇
- 50-69：一般用词

## 示例
```json
{
  "metadata": {
    "category": "Daily Routines",
    "category_cn": "日常事务",
    "word_count": 1,
    "difficulty_distribution": {
      "A": 100,
      "B": 0,
      "C": 0
    }
  },
  "words": {
    "breakfast": {
      "word": "breakfast",
      "translation": "早餐",
      "phonetic": "ˈbrekfəst",
      "part_of_speech": "n",
      "frequency": 95,
      "examples": [
        {
          "en": "What do you usually have for breakfast?",
          "zh": "你早餐通常吃什么？"
        },
        {
          "en": "I always eat breakfast at 7 AM.",
          "zh": "我总是在早上7点吃早餐。"
        }
      ],
      "difficulty_level": "A",
      "topics": ["Daily Life"],
      "category": "日常事务",
      "related_words": ["meal", "food", "morning"],
      "phrases": [
        {
          "phrase": "have breakfast",
          "translation": "吃早餐",
          "difficulty": "A"
        },
        {
          "phrase": "morning meal",
          "translation": "早餐",
          "difficulty": "B"
        }
      ]
    }
  }
}
``` 