import { useNavigate, useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Loader2, ArrowLeft } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/components/ui/use-toast';
import { toursApi } from '@/api';

const tourSchema = z.object({
  title: z.string().min(1, 'Введите название тура').max(255),
  agency: z.string().min(1, 'Введите название агентства').max(255),
  description: z.string().optional(),
  start_date: z.string().min(1, 'Выберите дату начала'),
  end_date: z.string().min(1, 'Выберите дату окончания'),
  price: z.coerce.number().min(1, 'Цена должна быть больше 0'),
  city: z.string().min(1, 'Введите город').max(100),
  payment_terms: z.string().optional(),
});

type TourFormData = z.infer<typeof tourSchema>;

export function TourFormPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const isEditing = Boolean(id);
  const tourId = parseInt(id || '0');

  const { data: tour, isLoading: tourLoading } = useQuery({
    queryKey: ['tour', tourId],
    queryFn: () => toursApi.getById(tourId),
    enabled: isEditing && tourId > 0,
  });

  const createMutation = useMutation({
    mutationFn: toursApi.create,
    onSuccess: (newTour) => {
      queryClient.invalidateQueries({ queryKey: ['tours'] });
      toast({
        title: 'Успешно!',
        description: 'Тур создан',
      });
      navigate(`/tours/${newTour.id}`);
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось создать тур',
      });
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: TourFormData) => toursApi.update(tourId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tours'] });
      queryClient.invalidateQueries({ queryKey: ['tour', tourId] });
      toast({
        title: 'Успешно!',
        description: 'Тур обновлён',
      });
      navigate(`/tours/${tourId}`);
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось обновить тур',
      });
    },
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TourFormData>({
    resolver: zodResolver(tourSchema),
    values: tour
      ? {
          title: tour.title,
          agency: tour.agency,
          description: tour.description || '',
          start_date: tour.start_date.split('T')[0],
          end_date: tour.end_date.split('T')[0],
          price: tour.price,
          city: tour.city,
          payment_terms: tour.payment_terms || '',
        }
      : undefined,
  });

  const onSubmit = (data: TourFormData) => {
    const formattedData = {
      ...data,
      start_date: new Date(data.start_date).toISOString(),
      end_date: new Date(data.end_date).toISOString(),
    };

    if (isEditing) {
      updateMutation.mutate(formattedData);
    } else {
      createMutation.mutate(formattedData);
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  if (isEditing && tourLoading) {
    return (
      <div className="container py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="container py-8">
      <Button variant="ghost" asChild className="mb-6">
        <Link to="/tours">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Назад к турам
        </Link>
      </Button>

      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>{isEditing ? 'Редактирование тура' : 'Новый тур'}</CardTitle>
          <CardDescription>
            {isEditing
              ? 'Измените данные тура'
              : 'Заполните информацию о новом туре'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="title">Название тура *</Label>
                <Input
                  id="title"
                  placeholder="Введите название"
                  {...register('title')}
                />
                {errors.title && (
                  <p className="text-sm text-destructive">{errors.title.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="agency">Агентство *</Label>
                <Input
                  id="agency"
                  placeholder="Название агентства"
                  {...register('agency')}
                />
                {errors.agency && (
                  <p className="text-sm text-destructive">{errors.agency.message}</p>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Описание</Label>
              <Textarea
                id="description"
                placeholder="Подробное описание тура..."
                rows={4}
                {...register('description')}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">Город *</Label>
                <Input
                  id="city"
                  placeholder="Город назначения"
                  {...register('city')}
                />
                {errors.city && (
                  <p className="text-sm text-destructive">{errors.city.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="price">Цена (₽) *</Label>
                <Input
                  id="price"
                  type="number"
                  min="1"
                  placeholder="0"
                  {...register('price')}
                />
                {errors.price && (
                  <p className="text-sm text-destructive">{errors.price.message}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="start_date">Дата начала *</Label>
                <Input
                  id="start_date"
                  type="date"
                  {...register('start_date')}
                />
                {errors.start_date && (
                  <p className="text-sm text-destructive">{errors.start_date.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="end_date">Дата окончания *</Label>
                <Input
                  id="end_date"
                  type="date"
                  {...register('end_date')}
                />
                {errors.end_date && (
                  <p className="text-sm text-destructive">{errors.end_date.message}</p>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="payment_terms">Условия оплаты</Label>
              <Textarea
                id="payment_terms"
                placeholder="Условия оплаты..."
                rows={2}
                {...register('payment_terms')}
              />
            </div>

            <div className="flex gap-4">
              <Button type="submit" disabled={isLoading}>
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                {isEditing ? 'Сохранить' : 'Создать'}
              </Button>
              <Button type="button" variant="outline" onClick={() => navigate(-1)}>
                Отмена
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
