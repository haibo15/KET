import WordCard from './WordCard';
import { Word } from '@/lib/api';

interface WordListProps {
  words: Word[];
  onPlayWord?: (word: Word) => void;
}

export default function WordList({ words, onPlayWord }: WordListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {words.map((word) => (
        <WordCard
          key={word._id}
          english={word.english}
          chinese={word.chinese}
          phonetic={word.phonetic}
          pos={word.pos}
          examples={word.examples}
          onPlay={onPlayWord ? () => onPlayWord(word) : undefined}
        />
      ))}
    </div>
  );
} 