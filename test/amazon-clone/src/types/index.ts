export interface Product {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  image: string;
  rating: number;
  reviewCount: number;
  isPrime?: boolean;
  isDeal?: boolean;
  category: string;
  description?: string;
}

export interface Category {
  id: string;
  name: string;
  image: string;
  description?: string;
}

export interface HeroBanner {
  id: string;
  title: string;
  subtitle?: string;
  image: string;
  link?: string;
}

export interface SearchResult {
  query: string;
  results: Product[];
  totalCount: number;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
  isPrime?: boolean;
} 