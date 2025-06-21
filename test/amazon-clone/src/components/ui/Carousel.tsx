'use client';

import { ReactNode } from 'react';
import useEmblaCarousel from 'embla-carousel-react';

interface CarouselProps {
  children: ReactNode[];
  options?: any;
}

export default function Carousel({ children, options }: CarouselProps) {
  const [emblaRef] = useEmblaCarousel(options);

  return (
    <div className="overflow-hidden" ref={emblaRef}>
      <div className="flex">
        {children.map((child, index) => (
          <div className="flex-shrink-0 w-1/4 min-w-0 pl-4" key={index}>
            {child}
          </div>
        ))}
      </div>
    </div>
  );
} 