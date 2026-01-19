import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { Loader2, MapPin, Calendar, Plus, Search } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { toursApi } from '@/api';
import { useAuthStore } from '@/store';

export function ToursPage() {
  const { isAuthenticated, user } = useAuthStore();
  const [cityFilter, setCityFilter] = useState('');

  const { data: tours, isLoading, error } = useQuery({
    queryKey: ['tours', cityFilter],
    queryFn: () => toursApi.getAll({ city: cityFilter || undefined }),
  });

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  };

  if (isLoading) {
    return (
      <div className="container py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-8">
        <div className="text-center text-destructive">
          Ошибка при загрузке туров. Попробуйте позже.
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold">Туры</h1>
          <p className="text-muted-foreground">Выберите идеальное путешествие</p>
        </div>
        <div className="flex gap-2 w-full md:w-auto">
          <div className="relative flex-1 md:w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Поиск по городу..."
              value={cityFilter}
              onChange={(e) => setCityFilter(e.target.value)}
              className="pl-9"
            />
          </div>
          {isAuthenticated && user?.is_admin && (
            <Button asChild>
              <Link to="/tours/new">
                <Plus className="h-4 w-4 mr-2" />
                Добавить тур
              </Link>
            </Button>
          )}
        </div>
      </div>

      {tours && tours.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground">Туры не найдены</p>
          {cityFilter && (
            <Button variant="link" onClick={() => setCityFilter('')}>
              Сбросить фильтр
            </Button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tours?.map((tour) => (
            <Card key={tour.id} className="flex flex-col">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="line-clamp-1">{tour.title}</CardTitle>
                    <CardDescription className="line-clamp-1">{tour.agency}</CardDescription>
                  </div>
                  <Badge variant="secondary">{formatPrice(tour.price)}</Badge>
                </div>
              </CardHeader>
              <CardContent className="flex-1">
                <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
                  {tour.description || 'Описание отсутствует'}
                </p>
                <div className="space-y-2">
                  <div className="flex items-center text-sm">
                    <MapPin className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>{tour.city}</span>
                  </div>
                  <div className="flex items-center text-sm">
                    <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>
                      {format(new Date(tour.start_date), 'd MMM', { locale: ru })} —{' '}
                      {format(new Date(tour.end_date), 'd MMM yyyy', { locale: ru })}
                    </span>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button asChild className="w-full">
                  <Link to={`/tours/${tour.id}`}>Подробнее</Link>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
