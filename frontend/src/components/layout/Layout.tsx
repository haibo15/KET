import { ReactNode } from 'react';
import Header from './Header';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-gray-100">
        <div className="container mx-auto px-4 py-4 text-center text-gray-600">
          © 2024 KET备考系统 - 助你轻松通过考试
        </div>
      </footer>
    </div>
  );
} 