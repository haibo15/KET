import { IWord } from '../models/Word';

export const basicWords: Partial<IWord>[] = [
  {
    english: "hello",
    chinese: "你好",
    phonetic: "həˈləʊ",
    pos: "interjection",
    level: 1,
    frequency: 100,
    examples: ["Hello, how are you?", "She said hello to everyone."],
    tags: ["greeting", "basic"]
  },
  {
    english: "goodbye",
    chinese: "再见",
    phonetic: "ɡʊdˈbaɪ",
    pos: "interjection",
    level: 1,
    frequency: 95,
    examples: ["Goodbye, see you tomorrow!", "He waved goodbye to his friends."],
    tags: ["greeting", "basic"]
  },
  {
    english: "thank",
    chinese: "感谢",
    phonetic: "θæŋk",
    pos: "verb",
    level: 1,
    frequency: 98,
    examples: ["Thank you very much!", "I want to thank you for your help."],
    tags: ["courtesy", "basic"]
  },
  {
    english: "please",
    chinese: "请",
    phonetic: "pliːz",
    pos: "interjection",
    level: 1,
    frequency: 97,
    examples: ["Please help me.", "Can I have some water, please?"],
    tags: ["courtesy", "basic"]
  },
  {
    english: "sorry",
    chinese: "对不起",
    phonetic: "ˈsɒri",
    pos: "adjective",
    level: 1,
    frequency: 96,
    examples: ["I'm sorry I'm late.", "Sorry about that!"],
    tags: ["courtesy", "basic"]
  }
]; 