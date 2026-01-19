import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plane, MapPin, Star, ChevronLeft, ChevronRight, Calendar } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuthStore } from '@/store';

const slides = [
  { src: '/images/slide1.jpg', alt: 'Хоккайдо 1' },
  { src: '/images/slide2.jpg', alt: 'Хоккайдо 2' },
  { src: '/images/slide3.jpg', alt: 'Хоккайдо 3' },
  { src: '/images/slide4.jpg', alt: 'Хоккайдо 4' },
  { src: '/images/slide5.jpg', alt: 'Хоккайдо 5' },
  { src: '/images/slide6.jpg', alt: 'Хоккайдо 6' },
];

export function HomePage() {
  const { isAuthenticated } = useAuthStore();
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  const nextSlide = () => setCurrentSlide((prev) => (prev + 1) % slides.length);
  const prevSlide = () => setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);

  return (
    <div className="flex flex-col min-h-[calc(100vh-3.5rem)]">
      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center space-y-4 text-center">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                Откройте Хоккайдо вместе с нами
              </h1>
              <p className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                Туристическое агентство Hokkaido Tours предлагает незабываемые путешествия 
                по всему Хоккайдо. Найдите свой идеальный тур уже сегодня!
              </p>
            </div>

            {/* Image Carousel */}
            <div className="relative w-full max-w-7xl mt-8 px-4">
              <div className="relative overflow-hidden rounded-xl shadow-2xl aspect-[16/9] min-h-[450px] md:min-h-[550px] lg:min-h-[700px]">
                {slides.map((slide, index) => (
                  <img
                    key={index}
                    src={slide.src}
                    alt={slide.alt}
                    className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-700 ${
                      index === currentSlide ? 'opacity-100' : 'opacity-0'
                    }`}
                  />
                ))}
                {/* Navigation buttons */}
                <button
                  onClick={prevSlide}
                  className="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-colors"
                >
                  <ChevronLeft className="h-6 w-6" />
                </button>
                <button
                  onClick={nextSlide}
                  className="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full transition-colors"
                >
                  <ChevronRight className="h-6 w-6" />
                </button>
                {/* Dots */}
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                  {slides.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentSlide(index)}
                      className={`w-3 h-3 rounded-full transition-colors ${
                        index === currentSlide ? 'bg-white' : 'bg-white/50'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </div>

            <div className="space-x-4 mt-8">
              <Button asChild size="lg">
                <Link to="/tours">Посмотреть туры</Link>
              </Button>
              {!isAuthenticated && (
                <Button variant="outline" size="lg" asChild>
                  <Link to="/register">Зарегистрироваться</Link>
                </Button>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 md:py-24 bg-muted/50">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
                Почему выбирают нас
              </h2>
              <p className="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                Мы заботимся о каждой детали вашего путешествия
              </p>
            </div>
          </div>
          <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <Plane className="h-10 w-10 mb-2 text-primary" />
                <CardTitle>Широкий выбор туров</CardTitle>
                <CardDescription>
                  Более 10 направлений по всему Хоккайдо
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  От пляжного отдыха до горнолыжных курортов - мы найдём тур для каждого
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <MapPin className="h-10 w-10 mb-2 text-primary" />
                <CardTitle>Лучшие локации</CardTitle>
                <CardDescription>
                  Проверенные отели и маршруты
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Мы лично проверяем каждый отель и маршрут перед включением в программу
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <Star className="h-10 w-10 mb-2 text-primary" />
                <CardTitle>Отзывы клиентов</CardTitle>
                <CardDescription>
                  Тысячи довольных путешественников
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  Читайте реальные отзывы и оставляйте свои после путешествия
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 md:py-24">
        <div className="container px-4 md:px-6">
          <div className="flex flex-col items-center justify-center space-y-4 text-center">
            <div className="space-y-2">
              <Calendar className="h-12 w-12 mx-auto mb-4 text-primary" />
              <h2 className="text-3xl font-bold tracking-tighter sm:text-4xl">
                Готовы к путешествию?
              </h2>
              <p className="max-w-[600px] text-gray-500 md:text-xl dark:text-gray-400">
                {isAuthenticated 
                  ? 'Выберите тур и отправляйтесь в незабываемое путешествие!'
                  : 'Зарегистрируйтесь сейчас и получите доступ к эксклюзивным предложениям'
                }
              </p>
            </div>
            <div className="space-x-4">
              <Button asChild size="lg">
                <Link to="/tours">Выбрать тур</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
