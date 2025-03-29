import Layout from '@/components/layout/Layout';
import Link from 'next/link';

export default function HomePage() {
  return (
    <Layout>
      <div className="py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            欢迎使用KET备考系统
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            通过科学的学习方法，帮助你轻松掌握KET考试所需的英语技能
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto mt-12">
          <Link href="/words" className="block">
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow text-center">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">词汇学习</h2>
              <p className="text-gray-600">
                通过智能复习系统，掌握KET考试核心词汇
              </p>
            </div>
          </Link>

          <Link href="/sentences" className="block">
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow text-center">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">句子练习</h2>
              <p className="text-gray-600">
                练习常见句型，提高语法和表达能力
              </p>
            </div>
          </Link>

          <Link href="/reading" className="block">
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow text-center">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">阅读理解</h2>
              <p className="text-gray-600">
                通过分级阅读材料，提升阅读理解能力
              </p>
            </div>
          </Link>
        </div>

        <div className="text-center mt-12">
          <Link
            href="/words"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            开始学习
          </Link>
        </div>
      </div>
    </Layout>
  );
}
