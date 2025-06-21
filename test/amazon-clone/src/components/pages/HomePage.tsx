import { Product, Category, HeroBanner } from '@/types';
import HeroBannerComponent from '../ui/HeroBanner';
import CategoryCard from '../ui/CategoryCard';
import ProductGrid from '../ui/ProductGrid';
import Carousel from '../ui/Carousel';
import ProductCard from '../ui/ProductCard';

// サンプルデータ
const sampleHeroBanner: HeroBanner = {
  id: '1',
  title: 'Prime Day セール',
  subtitle: '最大50%OFF！限定商品が続々登場',
  image: 'https://images.unsplash.com/photo-1607082349566-187342175e2f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80',
  link: '/prime-day'
};

const sampleCategories: Category[] = [
  {
    id: '1',
    name: 'エレクトロニクス',
    image: 'https://images.unsplash.com/photo-1498049794561-7780e7231661?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80',
    description: '最新の電子機器'
  },
  {
    id: '2',
    name: 'ファッション',
    image: 'https://images.unsplash.com/photo-1445205170230-053b83016050?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80',
    description: 'トレンドの服飾品'
  },
  {
    id: '3',
    name: 'ホーム・キッチン',
    image: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80',
    description: '生活用品・キッチン用品'
  },
  {
    id: '4',
    name: '本',
    image: 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80',
    description: '書籍・雑誌'
  },
  {
    id: '5',
    name: 'スポーツ',
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80',
    description: 'スポーツ用品'
  },
  {
    id: '6',
    name: 'おもちゃ',
    image: 'https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?ixlib=rb-4.0.3&auto=format&fit=crop&w=100&q=80',
    description: 'おもちゃ・ゲーム'
  }
];

const sampleProducts: Product[] = [
  {
    id: '1',
    name: 'Echo Dot (第5世代) | Alexa搭載スマートスピーカー | チャコール',
    price: 5980,
    originalPrice: 7980,
    image: 'https://images.unsplash.com/photo-1543512214-318c7553f230?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    rating: 4.5,
    reviewCount: 1247,
    isPrime: true,
    isDeal: true,
    category: 'エレクトロニクス'
  },
  {
    id: '2',
    name: 'Fire TV Stick 4K Max | Alexa対応 | ストリーミングデバイス',
    price: 6980,
    originalPrice: 8980,
    image: 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    rating: 4.3,
    reviewCount: 892,
    isPrime: true,
    isDeal: true,
    category: 'エレクトロニクス'
  },
  {
    id: '3',
    name: 'Kindle Paperwhite (8GB) | 防水対応 | 電子書籍リーダー',
    price: 12980,
    originalPrice: 14980,
    image: 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    rating: 4.7,
    reviewCount: 2156,
    isPrime: true,
    category: 'エレクトロニクス'
  },
  {
    id: '4',
    name: 'Fire HD 10 タブレット (32GB) | 10.1インチ | ブラック',
    price: 15980,
    originalPrice: 19980,
    image: 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    rating: 4.2,
    reviewCount: 743,
    isPrime: true,
    isDeal: true,
    category: 'エレクトロニクス'
  },
  {
    id: '5',
    name: 'Ring Video Doorbell 3 | 1080p HD | モーション検知',
    price: 19800,
    originalPrice: 24800,
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    rating: 4.4,
    reviewCount: 567,
    isPrime: true,
    category: 'ホーム・キッチン'
  },
  {
    id: '6',
    name: 'Blink Mini | 室内用セキュリティカメラ | 1080p HD',
    price: 3980,
    originalPrice: 5980,
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
    rating: 4.1,
    reviewCount: 1234,
    isPrime: true,
    isDeal: true,
    category: 'ホーム・キッチン'
  }
];

export default function HomePage() {
  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* ヒーローバナー */}
      <div className="mb-8">
        <HeroBannerComponent banner={sampleHeroBanner} />
      </div>

      {/* カテゴリーセクション */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">カテゴリーから探す</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {sampleCategories.map((category) => (
            <CategoryCard key={category.id} category={category} />
          ))}
        </div>
      </section>

      {/* おすすめ商品セクション */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">おすすめ商品</h2>
        <Carousel options={{ loop: true }}>
          {sampleProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </Carousel>
      </section>

      {/* 特価商品セクション */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">今日のセール</h2>
        <Carousel options={{ loop: true }}>
          {sampleProducts.filter(p => p.isDeal).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </Carousel>
      </section>

      {/* Prime商品セクション */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Prime商品</h2>
        <Carousel options={{ loop: true }}>
          {sampleProducts.filter(p => p.isPrime).map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </Carousel>
      </section>
    </div>
  );
} 