import { HeroBanner as HeroBannerType } from '@/types';

interface HeroBannerProps {
  banner: HeroBannerType;
  className?: string;
}

export default function HeroBanner({ banner, className = "" }: HeroBannerProps) {
  return (
    <div className={`relative w-full h-96 overflow-hidden rounded-lg ${className}`}>
      {/* 背景画像 */}
      <img
        src={banner.image}
        alt={banner.title}
        className="w-full h-full object-cover"
      />
      
      {/* オーバーレイ */}
      <div className="absolute inset-0 bg-black bg-opacity-30"></div>
      
      {/* コンテンツ */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center text-white px-6">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 drop-shadow-lg">
            {banner.title}
          </h1>
          {banner.subtitle && (
            <p className="text-xl md:text-2xl mb-6 drop-shadow-lg">
              {banner.subtitle}
            </p>
          )}
          {banner.link && (
            <button className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-8 rounded-lg transition-colors text-lg drop-shadow-lg">
              今すぐ見る
            </button>
          )}
        </div>
      </div>
    </div>
  );
} 