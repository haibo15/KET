import { Request, Response } from 'express';
import Word, { IWord } from '../models/Word';

// 获取所有单词
export const getAllWords = async (req: Request, res: Response) => {
  try {
    const words = await Word.find();
    res.json(words);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching words', error });
  }
};

// 按级别获取单词
export const getWordsByLevel = async (req: Request, res: Response) => {
  try {
    const { level } = req.params;
    const words = await Word.find({ level: parseInt(level) });
    res.json(words);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching words by level', error });
  }
};

// 添加新单词
export const createWord = async (req: Request, res: Response) => {
  try {
    const word = new Word(req.body);
    const savedWord = await word.save();
    res.status(201).json(savedWord);
  } catch (error) {
    res.status(400).json({ message: 'Error creating word', error });
  }
};

// 更新单词
export const updateWord = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const updatedWord = await Word.findByIdAndUpdate(id, req.body, { new: true });
    if (!updatedWord) {
      return res.status(404).json({ message: 'Word not found' });
    }
    res.json(updatedWord);
  } catch (error) {
    res.status(400).json({ message: 'Error updating word', error });
  }
};

// 删除单词
export const deleteWord = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const deletedWord = await Word.findByIdAndDelete(id);
    if (!deletedWord) {
      return res.status(404).json({ message: 'Word not found' });
    }
    res.json({ message: 'Word deleted successfully' });
  } catch (error) {
    res.status(400).json({ message: 'Error deleting word', error });
  }
};

// 搜索单词
export const searchWords = async (req: Request, res: Response) => {
  try {
    const { query } = req.query;
    const words = await Word.find({
      $or: [
        { english: { $regex: query, $options: 'i' } },
        { chinese: { $regex: query, $options: 'i' } },
        { tags: { $regex: query, $options: 'i' } }
      ]
    });
    res.json(words);
  } catch (error) {
    res.status(500).json({ message: 'Error searching words', error });
  }
}; 