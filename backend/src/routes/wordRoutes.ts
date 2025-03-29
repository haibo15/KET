import express from 'express';
import {
  getAllWords,
  getWordsByLevel,
  createWord,
  updateWord,
  deleteWord,
  searchWords
} from '../controllers/wordController';

const router = express.Router();

// 获取所有单词
router.get('/', getAllWords);

// 按级别获取单词
router.get('/level/:level', getWordsByLevel);

// 搜索单词
router.get('/search', searchWords);

// 添加新单词
router.post('/', createWord);

// 更新单词
router.put('/:id', updateWord);

// 删除单词
router.delete('/:id', deleteWord);

export default router; 