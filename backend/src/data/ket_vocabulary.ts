import { IWord } from '../models/Word';

// 核心词汇 (Core Vocabulary) - A1 Level
export const coreWordsA1: Partial<IWord>[] = [
  {
    english: "hello",
    chinese: "你好",
    phonetic: "həˈləʊ",
    pos: "interjection",
    level: 1,
    frequency: 100,
    examples: [
      "Hello, how are you?",
      "She said hello to everyone."
    ],
    tags: ["core", "greeting", "A1"]
  },
  {
    english: "goodbye",
    chinese: "再见",
    phonetic: "ɡʊdˈbaɪ",
    pos: "interjection",
    level: 1,
    frequency: 98,
    examples: [
      "Goodbye, see you tomorrow!",
      "He waved goodbye to his friends."
    ],
    tags: ["core", "greeting", "A1"]
  },
  {
    english: "please",
    chinese: "请",
    phonetic: "pliːz",
    pos: "interjection",
    level: 1,
    frequency: 98,
    examples: [
      "Please help me.",
      "Can I have some water, please?"
    ],
    tags: ["core", "courtesy", "A1"]
  },
  {
    english: "thank",
    chinese: "感谢",
    phonetic: "θæŋk",
    pos: "verb",
    level: 1,
    frequency: 97,
    examples: [
      "Thank you very much!",
      "I want to thank you for your help."
    ],
    tags: ["core", "courtesy", "A1"]
  },
  {
    english: "sorry",
    chinese: "对不起",
    phonetic: "ˈsɒri",
    pos: "adjective",
    level: 1,
    frequency: 97,
    examples: [
      "I'm sorry I'm late.",
      "Sorry about that!"
    ],
    tags: ["core", "courtesy", "A1"]
  }
];

// 核心词汇 (Core Vocabulary) - A2 Level
export const coreWordsA2: Partial<IWord>[] = [
  {
    english: "appointment",
    chinese: "预约",
    phonetic: "əˈpɔɪntmənt",
    pos: "noun",
    level: 2,
    frequency: 85,
    examples: [
      "I have an appointment with the doctor.",
      "Would you like to make an appointment?"
    ],
    tags: ["core", "service", "A2"]
  },
  {
    english: "schedule",
    chinese: "日程表",
    phonetic: "ˈʃedjuːl",
    pos: "noun",
    level: 2,
    frequency: 86,
    examples: [
      "What's your schedule like today?",
      "The meeting is not on my schedule."
    ],
    tags: ["core", "time", "A2"]
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
    frequency: 82,
    examples: [
      "I use my computer every day.",
      "The computer is not working."
    ],
    tags: ["high-frequency", "technology", "A2"]
  },
  {
    english: "weekend",
    chinese: "周末",
    phonetic: "ˌwiːkˈend",
    pos: "noun",
    level: 2,
    frequency: 83,
    examples: [
      "What do you do at the weekend?",
      "I like to rest at weekends."
    ],
    tags: ["high-frequency", "time", "A2"]
  }
];

// 扩展词汇 (Extended Vocabulary)
export const extendedWords: Partial<IWord>[] = [
  {
    english: "adventure",
    chinese: "冒险",
    phonetic: "ədˈventʃə(r)",
    pos: "noun",
    level: 3,
    frequency: 75,
    examples: [
      "We had an exciting adventure in the forest.",
      "He loves reading adventure stories."
    ],
    tags: ["extended", "activity", "A2"]
  },
  {
    english: "celebrate",
    chinese: "庆祝",
    phonetic: "ˈselɪbreɪt",
    pos: "verb",
    level: 3,
    frequency: 76,
    examples: [
      "We celebrate Christmas every year.",
      "They're celebrating their wedding anniversary."
    ],
    tags: ["extended", "activity", "A2"]
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