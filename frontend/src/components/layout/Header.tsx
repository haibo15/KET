import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-blue-600 text-white">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            KET备考系统
          </Link>
          <div className="space-x-6">
            <Link href="/words" className="hover:text-blue-200">
              词汇学习
            </Link>
            <Link href="/sentences" className="hover:text-blue-200">
              句子练习
            </Link>
            <Link href="/reading" className="hover:text-blue-200">
              阅读理解
            </Link>
            <Link href="/profile" className="hover:text-blue-200">
              个人中心
            </Link>
          </div>
        </div>
      </nav>
    </header>
  );
} 