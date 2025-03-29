interface WordCardProps {
  english: string;
  chinese: string;
  phonetic: string;
  pos: string;
  examples: string[];
  onPlay?: () => void;
}

export default function WordCard({
  english,
  chinese,
  phonetic,
  pos,
  examples,
  onPlay
}: WordCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-2xl font-bold text-gray-800">{english}</h3>
          <p className="text-gray-600 mt-1">/{phonetic}/</p>
        </div>
        {onPlay && (
          <button
            onClick={onPlay}
            className="text-blue-500 hover:text-blue-600"
            aria-label="播放发音"
          >
            🔊
          </button>
        )}
      </div>
      
      <div className="mt-4">
        <p className="text-lg text-gray-700">{chinese}</p>
        <p className="text-sm text-gray-500 mt-1">{pos}</p>
      </div>

      {examples.length > 0 && (
        <div className="mt-4 border-t pt-4">
          <p className="text-sm font-medium text-gray-700">例句：</p>
          <ul className="mt-2 space-y-2">
            {examples.map((example, index) => (
              <li key={index} className="text-sm text-gray-600">
                {example}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
} 