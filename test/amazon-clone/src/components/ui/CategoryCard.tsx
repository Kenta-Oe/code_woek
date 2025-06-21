import { Category } from '@/types';

interface CategoryCardProps {
  category: Category;
  className?: string;
  onClick?: () => void;
}

export default function CategoryCard({ 
  category, 
  className = "",
  onClick 
}: CategoryCardProps) {
  return (
    <div 
      className={`bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all cursor-pointer hover:border-orange-300 ${className}`}
      onClick={onClick}
    >
      <div className="flex flex-col items-center text-center space-y-3">
        {/* カテゴリー画像 */}
        <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-100 flex items-center justify-center">
          <img
            src={category.image}
            alt={category.name}
            className="w-12 h-12 object-contain"
          />
        </div>

        {/* カテゴリー名 */}
        <h3 className="text-sm font-medium text-gray-900 hover:text-orange-600 transition-colors">
          {category.name}
        </h3>

        {/* 説明（オプション） */}
        {category.description && (
          <p className="text-xs text-gray-500 line-clamp-2">
            {category.description}
          </p>
        )}
      </div>
    </div>
  );
} 