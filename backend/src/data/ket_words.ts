import { IWord } from '../models/Word';

// 核心词汇 (Core Vocabulary)
export const coreWords: Partial<IWord>[] = [
  // A1 Level - 基础日常用语
  {
    english: "hello",
    chinese: "你好",
    phonetic: "həˈləʊ",
    pos: "interjection",
    level: 1,
    frequency: 100,
    examples: ["Hello, how are you?", "She said hello to everyone."],
    tags: ["core", "greeting", "A1"]
  },
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
    english: "student",
    chinese: "学生",
    phonetic: "ˈstjuːdnt",
    pos: "noun",
    level: 1,
    frequency: 95,
    examples: ["I am a student.", "There are twenty students in my class."],
    tags: ["core", "education", "A1"]
  }
];

// 高频词汇 (High Frequency Vocabulary)
export const highFrequencyWords: Partial<IWord>[] = [
  {
    english: "computer",
    chinese: "电脑",
    phonetic: "kəmˈpjuːtə(r)",
    pos: "noun",
    level: 2,
    frequency: 92,
    examples: ["I use my computer every day.", "The computer is not working."],
    tags: ["high-frequency", "technology", "A1-A2"]
  },
  {
    english: "weekend",
    chinese: "周末",
    phonetic: "ˌwiːkˈend",
    pos: "noun",
    level: 2,
    frequency: 90,
    examples: ["What do you do at the weekend?", "I like to rest at weekends."],
    tags: ["high-frequency", "time", "A1-A2"]
  }
];

// 扩展词汇 (Extended Vocabulary)
export const extendedWords: Partial<IWord>[] = [
  {
    english: "appointment",
    chinese: "预约",
    phonetic: "əˈpɔɪntmənt",
    pos: "noun",
    level: 4,
    frequency: 75,
    examples: ["I have an appointment with the doctor.", "Would you like to make an appointment?"],
    tags: ["extended", "service", "A2"]
  },
  {
    english: "schedule",
    chinese: "日程表",
    phonetic: "ˈʃedjuːl",
    pos: "noun",
    level: 4,
    frequency: 73,
    examples: ["What's your schedule like today?", "The meeting is not on my schedule."],
    tags: ["extended", "time", "A2"]
  }
];

// 词汇主题分类
export const vocabularyTopics = {
  personal: ["name", "age", "family", "hobby"],
  daily: ["food", "clothes", "weather", "time"],
  education: ["school", "class", "study", "teacher"],
  work: ["job", "office", "meeting", "business"],
  transport: ["bus", "train", "ticket", "travel"],
  leisure: ["sport", "music", "movie", "holiday"],
  shopping: ["shop", "price", "money", "buy"],
  health: ["hospital", "doctor", "sick", "medicine"],
  technology: ["computer", "phone", "internet", "email"],
  services: ["bank", "post office", "restaurant", "hotel"]
}; 