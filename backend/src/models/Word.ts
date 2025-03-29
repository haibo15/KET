import mongoose, { Schema, Document } from 'mongoose';

export interface IWord extends Document {
  english: string;
  chinese: string;
  phonetic: string;
  pos: string; // part of speech
  level: number;
  frequency: number;
  examples: string[];
  images: string[];
  audio: string;
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
}

const WordSchema: Schema = new Schema({
  english: { type: String, required: true, unique: true },
  chinese: { type: String, required: true },
  phonetic: { type: String },
  pos: { type: String, required: true },
  level: { type: Number, required: true, min: 1, max: 5 },
  frequency: { type: Number, default: 0 },
  examples: [{ type: String }],
  images: [{ type: String }],
  audio: { type: String },
  tags: [{ type: String }]
}, {
  timestamps: true
});

// 添加索引以提高查询性能
WordSchema.index({ english: 1 });
WordSchema.index({ level: 1 });
WordSchema.index({ frequency: -1 });
WordSchema.index({ tags: 1 });

export default mongoose.model<IWord>('Word', WordSchema); 