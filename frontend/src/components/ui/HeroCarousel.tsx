import { useState, useEffect, useCallback } from 'react';
import { ChevronLeft, ChevronRight, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import govscemes from "../../IMAGES/carousel.image/govscemes.jpg";
import healthcare from "../../IMAGES/carousel.image/healthcare.webp";
import farmer from "../../IMAGES/carousel.image/farmer.webp";
import education from "../../IMAGES/carousel.image/education.webp";
import entueneuurprinship from "../../IMAGES/carousel.image/entueneuurprinship.jpg";
import oldpeople from "../../IMAGES/carousel.image/oldpeople.webp";
interface CarouselSlide {
  image: string;
  title: string;
  subtitle: string;
  badge: string;
  link: string;
}

const slides: CarouselSlide[] = [
  {
    image: govscemes,
    title: 'Empowering Every Citizen',
    subtitle: 'Discover schemes tailored to your needs — from education to entrepreneurship, all in one place.',
    badge: '',
    link: '/schemes',
  },
  {
    image: healthcare,
    title: 'Healthcare for All',
    subtitle: 'Find health insurance and medical assistance schemes you qualify for — up to ₹5 lakh coverage.',
    badge: 'Healthcare',
    link: '/schemes?category=healthcare',
  },
  {
    image: farmer,
    title: 'Supporting Our Farmers',
    subtitle: 'Income support, crop insurance, and agricultural subsidies — matched to your land and crops.',
    badge: 'Agriculture',
    link: '/schemes?category=farmers',
  },
  {
    image: education,
    title: 'Education for Every Student',
    subtitle: 'Scholarships and fellowships matched to your background, category, and qualifications.',
    badge: 'Education',
    link: '/schemes?category=students',
  },
  {
    image: entueneuurprinship,
    title: 'Building Entrepreneurs',
    subtitle: 'Collateral-free business loans, startup support, and mentorship — up to ₹10 lakh.',
    badge: 'Entrepreneurship',
    link: '/schemes?category=entrepreneurs',
  },
  {
    image: oldpeople,
    title: 'Providing support to our senior citizens',
    subtitle: 'Pension schemes, healthcare benefits, travel concessions, and financial assistance designed to support senior citizens.',
    badge: 'Senior citizens',
    link: '/schemes?category=',
  },
];

export function HeroCarousel() {
  const [current, setCurrent] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  const next = useCallback(() => {
    setCurrent((prev) => (prev + 1) % slides.length);
  }, []);

  const prev = useCallback(() => {
    setCurrent((prev) => (prev - 1 + slides.length) % slides.length);
  }, []);

  useEffect(() => {
    if (isPaused) return;
    const timer = setInterval(next, 5000);
    return () => clearInterval(timer);
  }, [next, isPaused]);

  return (
    <div
      className="relative w-full h-full rounded-2xl overflow-hidden shadow-elevated group"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      {/* Slides */}
      <div className="relative h-full">
        {slides.map((slide, i) => (
          <div
            key={i}
            className={`absolute inset-0 transition-all duration-700 ease-in-out ${
              i === current ? 'opacity-100 scale-100' : 'opacity-0 scale-105 pointer-events-none'
            }`}
          >
            <img
              src={slide.image}
              alt={slide.title}
              className="w-full h-full object-cover"
              loading={i === 0 ? 'eager' : 'lazy'}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-navy-950/85 via-navy-900/40 to-navy-900/10" />
            <div className="absolute bottom-0 left-0 right-0 p-6 lg:p-8">
              <div
                className="transform transition-all duration-500"
                style={{
                  opacity: i === current ? 1 : 0,
                  transform: i === current ? 'translateY(0)' : 'translateY(24px)',
                  transitionDelay: i === current ? '200ms' : '0ms',
                }}
              >
                <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-saffron-500/90 text-white text-xs font-semibold mb-3 backdrop-blur-sm">
                  {slide.badge}
                </span>
                <h3 className="font-heading font-bold text-white text-xl lg:text-2xl mb-2 leading-tight">
                  {slide.title}
                </h3>
                <p className="text-sm text-white/80 leading-relaxed max-w-md mb-4">
                  {slide.subtitle}
                </p>
                <Link
                  to={slide.link}
                  className="inline-flex items-center gap-1.5 text-sm font-medium text-saffron-300 hover:text-saffron-200 transition-colors group/link"
                >
                  Explore schemes
                  <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div className="absolute top-0 left-0 right-0 h-1 z-10 bg-white/20">
        <div
          key={current}
          className="h-full bg-saffron-400"
          style={{
            animation: isPaused ? 'none' : 'progressBar 5s linear forwards',
          }}
        />
        <style>{`
          @keyframes progressBar {
            from { width: 0%; }
            to { width: 100%; }
          }
        `}</style>
      </div>

      {/* Navigation Arrows */}
      <button
        onClick={prev}
        className="absolute left-3 top-1/2 -translate-y-1/2 z-10 w-9 h-9 rounded-full bg-white/20 backdrop-blur-sm text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all hover:bg-white/30"
        aria-label="Previous slide"
      >
        <ChevronLeft className="w-5 h-5" />
      </button>
      <button
        onClick={next}
        className="absolute right-3 top-1/2 -translate-y-1/2 z-10 w-9 h-9 rounded-full bg-white/20 backdrop-blur-sm text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all hover:bg-white/30"
        aria-label="Next slide"
      >
        <ChevronRight className="w-5 h-5" />
      </button>

      {/* Dots */}
      <div className="absolute bottom-3 right-4 z-10 flex gap-1.5">
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`h-1.5 rounded-full transition-all duration-300 ${
              i === current ? 'w-6 bg-saffron-400' : 'w-1.5 bg-white/50 hover:bg-white/70'
            }`}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
