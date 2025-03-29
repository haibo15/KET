import mongoose from 'mongoose';
import dotenv from 'dotenv';
import Word from '../models/Word';
import { basicWords } from '../data/ket_words_basic';

// 加载环境变量
dotenv.config();

// 连接数据库
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/ket_exam';

async function initializeDatabase() {
  try {
    // 连接MongoDB
    await mongoose.connect(MONGODB_URI);
    console.log('Connected to MongoDB');

    // 清空现有数据
    await Word.deleteMany({});
    console.log('Cleared existing words');

    // 插入基础词汇
    const result = await Word.insertMany(basicWords);
    console.log(`Inserted ${result.length} basic words`);

    // 创建索引
    await Word.collection.createIndex({ english: 1 });
    await Word.collection.createIndex({ level: 1 });
    await Word.collection.createIndex({ frequency: -1 });
    await Word.collection.createIndex({ tags: 1 });
    console.log('Created indexes');

    console.log('Database initialization completed');
  } catch (error) {
    console.error('Error initializing database:', error);
  } finally {
    // 关闭数据库连接
    await mongoose.disconnect();
    console.log('Disconnected from MongoDB');
  }
}

// 运行初始化
initializeDatabase(); 