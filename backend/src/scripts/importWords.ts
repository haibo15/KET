import mongoose from 'mongoose';
import dotenv from 'dotenv';
import Word from '../models/Word';
import { coreWordsA1, coreWordsA2, highFrequencyWords, extendedWords } from '../data/ket_vocabulary';

// 加载环境变量
dotenv.config();

// 连接数据库
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/ket_exam';

async function importWords() {
  try {
    // 连接MongoDB
    await mongoose.connect(MONGODB_URI);
    console.log('Connected to MongoDB');

    // 清空现有数据
    await Word.deleteMany({});
    console.log('Cleared existing words');

    // 导入A1级核心词汇
    const coreA1Result = await Word.insertMany(coreWordsA1);
    console.log(`Imported ${coreA1Result.length} A1 core words`);

    // 导入A2级核心词汇
    const coreA2Result = await Word.insertMany(coreWordsA2);
    console.log(`Imported ${coreA2Result.length} A2 core words`);

    // 导入高频词汇
    const highFreqResult = await Word.insertMany(highFrequencyWords);
    console.log(`Imported ${highFreqResult.length} high frequency words`);

    // 导入扩展词汇
    const extendedResult = await Word.insertMany(extendedWords);
    console.log(`Imported ${extendedResult.length} extended words`);

    const totalWords = 
      coreA1Result.length + 
      coreA2Result.length + 
      highFreqResult.length + 
      extendedResult.length;
    
    console.log(`Total words imported: ${totalWords}`);
    console.log('Word import completed successfully');

  } catch (error) {
    console.error('Error importing words:', error);
  } finally {
    // 关闭数据库连接
    await mongoose.disconnect();
    console.log('Disconnected from MongoDB');
  }
}

// 运行导入脚本
importWords(); 