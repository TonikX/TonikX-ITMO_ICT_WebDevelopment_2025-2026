import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Loader2,
  MapPin,
  Calendar,
  Building,
  CreditCard,
  ArrowLeft,
  Edit,
  Trash2,
  Star,
  Users,
  Check,
  Clock,
  X,
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { toursApi, reservationsApi, reviewsApi } from '@/api';
import { useAuthStore } from '@/store';
import type { Reservation } from '@/types';

const reservationSchema = z.object({
  notes: z.string().optional(),
});

const reviewSchema = z.object({
  text: z.string().min(1, 'Введите текст отзыва'),
  rating: z.coerce.number().min(1).max(10),
});

type ReservationFormData = z.infer<typeof reservationSchema>;
type ReviewFormData = z.infer<typeof reviewSchema>;

export function TourDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const { isAuthenticated, user } = useAuthStore();
  const [isReservationOpen, setIsReservationOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [isEditingReview, setIsEditingReview] = useState(false);

  const tourId = parseInt(id || '0');

  const { data: tour, isLoading: tourLoading } = useQuery({
    queryKey: ['tour', tourId],
    queryFn: () => toursApi.getById(tourId),
    enabled: tourId > 0,
  });

  const { data: reviews, isLoading: reviewsLoading } = useQuery({
    queryKey: ['reviews', tourId],
    queryFn: () => reviewsApi.getByTour(tourId),
    enabled: tourId > 0,
  });

  // Получаем свои бронирования и проверяем есть ли бронь на этот тур
  const { data: myReservations } = useQuery({
    queryKey: ['myReservations'],
    queryFn: () => reservationsApi.getMy(),
    enabled: isAuthenticated,
  });

  // Получаем свой отзыв на этот тур
  const { data: myReview } = useQuery({
    queryKey: ['myReview', tourId],
    queryFn: () => reviewsApi.getMyForTour(tourId),
    enabled: isAuthenticated && tourId > 0,
  });

  // Находим бронирование пользователя на этот тур
  const myReservationForTour: Reservation | undefined = myReservations?.find(
    (r) => r.tour_id === tourId
  );
  const hasReservation = !!myReservationForTour;
  const hasConfirmedReservation = myReservationForTour?.status === 'confirmed';
  const hasReview = !!myReview;

  // Статус бронирования для отображения
  const getReservationStatusInfo = (status: string) => {
    switch (status) {
      case 'confirmed':
        return { label: 'Подтверждено', icon: Check, variant: 'default' as const };
      case 'rejected':
        return { label: 'Отклонено', icon: X, variant: 'destructive' as const };
      default:
        return { label: 'На рассмотрении', icon: Clock, variant: 'secondary' as const };
    }
  };

  const deleteMutation = useMutation({
    mutationFn: () => toursApi.delete(tourId),
    onSuccess: () => {
      toast({
        title: 'Успешно!',
        description: 'Тур удалён',
      });
      navigate('/tours');
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось удалить тур',
      });
    },
  });

  const reservationMutation = useMutation({
    mutationFn: (data: { tour_id: number; notes?: string }) =>
      reservationsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['myReservations'] });
      toast({
        title: 'Успешно!',
        description: 'Бронирование создано',
      });
      setIsReservationOpen(false);
      reservationForm.reset();
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось создать бронирование',
      });
    },
  });

  const reviewMutation = useMutation({
    mutationFn: (data: { tour_id: number; text: string; rating: number }) =>
      reviewsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', tourId] });
      queryClient.invalidateQueries({ queryKey: ['myReview', tourId] });
      toast({
        title: 'Успешно!',
        description: 'Отзыв добавлен',
      });
      reviewForm.reset();
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось добавить отзыв',
      });
    },
  });

  const updateReviewMutation = useMutation({
    mutationFn: (data: { id: number; text: string; rating: number }) =>
      reviewsApi.update(data.id, { text: data.text, rating: data.rating }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', tourId] });
      queryClient.invalidateQueries({ queryKey: ['myReview', tourId] });
      toast({
        title: 'Успешно!',
        description: 'Отзыв обновлён',
      });
      setIsEditingReview(false);
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось обновить отзыв',
      });
    },
  });

  const reservationForm = useForm<ReservationFormData>({
    resolver: zodResolver(reservationSchema),
    defaultValues: {
      notes: '',
    },
  });

  const reviewForm = useForm<ReviewFormData>({
    resolver: zodResolver(reviewSchema),
    defaultValues: {
      text: '',
      rating: 5,
    },
  });

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const onReservationSubmit = (data: ReservationFormData) => {
    reservationMutation.mutate({
      tour_id: tourId,
      notes: data.notes,
    });
  };

  const onReviewSubmit = (data: ReviewFormData) => {
    if (isEditingReview && myReview) {
      updateReviewMutation.mutate({
        id: myReview.id,
        text: data.text,
        rating: data.rating,
      });
    } else {
      reviewMutation.mutate({
        tour_id: tourId,
        text: data.text,
        rating: data.rating,
      });
    }
  };

  // Заполнение формы при редактировании
  useEffect(() => {
    if (isEditingReview && myReview) {
      reviewForm.setValue('text', myReview.text);
      reviewForm.setValue('rating', myReview.rating);
    }
  }, [isEditingReview, myReview, reviewForm]);

  if (tourLoading) {
    return (
      <div className="container py-8 flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!tour) {
    return (
      <div className="container py-8">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Тур не найден</p>
          <Button asChild>
            <Link to="/tours">Вернуться к турам</Link>
          </Button>
        </div>
      </div>
    );
  }

  const averageRating = reviews && reviews.length > 0
    ? (reviews.reduce((acc, r) => acc + r.rating, 0) / reviews.length).toFixed(1)
    : null;

  return (
    <div className="container py-8">
      <Button variant="ghost" asChild className="mb-6">
        <Link to="/tours">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Назад к турам
        </Link>
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Info */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-2xl">{tour.title}</CardTitle>
                  <CardDescription className="flex items-center mt-2">
                    <Building className="h-4 w-4 mr-1" />
                    {tour.agency}
                  </CardDescription>
                </div>
                {isAuthenticated && user?.is_admin && (
                  <div className="flex gap-2">
                    <Button variant="outline" size="icon" asChild>
                      <Link to={`/tours/${tour.id}/edit`}>
                        <Edit className="h-4 w-4" />
                      </Link>
                    </Button>
                    <Dialog open={isDeleteOpen} onOpenChange={setIsDeleteOpen}>
                      <DialogTrigger asChild>
                        <Button variant="outline" size="icon">
                          <Trash2 className="h-4 w-4 text-destructive" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Удалить тур?</DialogTitle>
                          <DialogDescription>
                            Это действие нельзя отменить. Тур будет удалён навсегда.
                          </DialogDescription>
                        </DialogHeader>
                        <DialogFooter>
                          <Button variant="outline" onClick={() => setIsDeleteOpen(false)}>
                            Отмена
                          </Button>
                          <Button
                            variant="destructive"
                            onClick={() => deleteMutation.mutate()}
                            disabled={deleteMutation.isPending}
                          >
                            {deleteMutation.isPending && (
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            )}
                            Удалить
                          </Button>
                        </DialogFooter>
                      </DialogContent>
                    </Dialog>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                {tour.description || 'Описание отсутствует'}
              </p>

              <Separator />

              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center">
                  <MapPin className="h-5 w-5 mr-2 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Город</p>
                    <p className="text-sm text-muted-foreground">{tour.city}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <Calendar className="h-5 w-5 mr-2 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Даты</p>
                    <p className="text-sm text-muted-foreground">
                      {format(new Date(tour.start_date), 'd MMM', { locale: ru })} —{' '}
                      {format(new Date(tour.end_date), 'd MMM yyyy', { locale: ru })}
                    </p>
                  </div>
                </div>
              </div>

              {tour.payment_terms && (
                <>
                  <Separator />
                  <div className="flex items-start">
                    <CreditCard className="h-5 w-5 mr-2 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-sm font-medium">Условия оплаты</p>
                      <p className="text-sm text-muted-foreground">{tour.payment_terms}</p>
                    </div>
                  </div>
                </>
              )}
            </CardContent>
          </Card>

          {/* Reviews Section */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle className="flex items-center gap-2">
                  <Star className="h-5 w-5" />
                  Отзывы
                  {averageRating && (
                    <Badge variant="secondary">{averageRating} / 10</Badge>
                  )}
                </CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Показываем форму только если есть подтвержденное бронирование И (нет отзыва ИЛИ редактируем) */}
              {isAuthenticated && hasConfirmedReservation && (!hasReview || isEditingReview) && (
                <form onSubmit={reviewForm.handleSubmit(onReviewSubmit)} className="space-y-4 border rounded-lg p-4">
                  <div className="space-y-2">
                    <Label htmlFor="text">{isEditingReview ? 'Редактирование отзыва' : 'Ваш отзыв'}</Label>
                    <Textarea
                      id="text"
                      placeholder="Расскажите о вашем опыте..."
                      {...reviewForm.register('text')}
                    />
                    {reviewForm.formState.errors.text && (
                      <p className="text-sm text-destructive">
                        {reviewForm.formState.errors.text.message}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="space-y-2">
                      <Label>Оценка</Label>
                      <Select
                        value={reviewForm.watch('rating').toString()}
                        onValueChange={(value) => reviewForm.setValue('rating', parseInt(value))}
                      >
                        <SelectTrigger className="w-24">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => (
                            <SelectItem key={n} value={n.toString()}>
                              {n}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <Button 
                      type="submit" 
                      disabled={reviewMutation.isPending || updateReviewMutation.isPending} 
                      className="mt-auto"
                    >
                      {(reviewMutation.isPending || updateReviewMutation.isPending) && (
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      )}
                      {isEditingReview ? 'Сохранить' : 'Отправить'}
                    </Button>
                    {isEditingReview && (
                      <Button 
                        type="button" 
                        variant="outline"
                        onClick={() => {
                          setIsEditingReview(false);
                          reviewForm.reset();
                        }}
                        className="mt-auto"
                      >
                        Отмена
                      </Button>
                    )}
                  </div>
                </form>
              )}

              {/* Показываем мой отзыв с кнопкой редактирования если есть отзыв и не редактируем */}
              {isAuthenticated && hasReview && myReview && !isEditingReview && (
                <div className="border-2 border-primary/20 rounded-lg p-4 bg-primary/5">
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-medium">Ваш отзыв</span>
                    <div className="flex items-center gap-2">
                      <Badge>{myReview.rating} / 10</Badge>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => setIsEditingReview(true)}
                      >
                        <Edit className="h-4 w-4 mr-1" />
                        Изменить
                      </Button>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">{myReview.text}</p>
                  <p className="text-xs text-muted-foreground mt-2">
                    {format(new Date(myReview.created_at), 'd MMMM yyyy', { locale: ru })}
                    {myReview.updated_at && (
                      <span className="ml-2 italic">(изменено)</span>
                    )}
                  </p>
                </div>
              )}

              {/* Сообщение если нет подтвержденного бронирования */}
              {isAuthenticated && !hasConfirmedReservation && !hasReview && (
                <div className="text-center text-muted-foreground py-4 border rounded-lg">
                  {hasReservation ? (
                    <p>Оставить отзыв можно после подтверждения бронирования</p>
                  ) : (
                    <p>Оставить отзыв можно после бронирования и подтверждения тура</p>
                  )}
                </div>
              )}

              {reviewsLoading ? (
                <div className="flex justify-center py-4">
                  <Loader2 className="h-6 w-6 animate-spin" />
                </div>
              ) : reviews && reviews.length > 0 ? (
                <div className="space-y-4">
                  {reviews
                    .filter((review) => !myReview || review.id !== myReview.id) // Исключаем свой отзыв из общего списка
                    .map((review) => (
                    <div key={review.id} className="border rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-medium">{review.username || 'Аноним'}</span>
                        <Badge>{review.rating} / 10</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">{review.text}</p>
                      <p className="text-xs text-muted-foreground mt-2">
                        {format(new Date(review.created_at), 'd MMMM yyyy', { locale: ru })}
                        {review.updated_at && (
                          <span className="ml-2 italic">(изменено)</span>
                        )}
                      </p>
                    </div>
                  ))}
                </div>
              ) : !hasReview && (
                <p className="text-center text-muted-foreground py-4">
                  Пока нет отзывов
                </p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Booking Sidebar */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-3xl">{formatPrice(tour.price)}</CardTitle>
              <CardDescription>за человека</CardDescription>
            </CardHeader>
            <CardContent>
              {isAuthenticated ? (
                hasReservation ? (
                  // Показываем статус бронирования
                  <div className="space-y-4">
                    {myReservationForTour && (() => {
                      const statusInfo = getReservationStatusInfo(myReservationForTour.status);
                      const StatusIcon = statusInfo.icon;
                      return (
                        <div className="text-center space-y-2">
                          <Badge variant={statusInfo.variant} className="text-sm px-3 py-1">
                            <StatusIcon className="h-4 w-4 mr-1" />
                            {statusInfo.label}
                          </Badge>
                          <p className="text-sm text-muted-foreground">
                            Вы уже забронировали этот тур
                          </p>
                          <Button asChild variant="outline" className="w-full">
                            <Link to="/profile">
                              Перейти к бронированиям
                            </Link>
                          </Button>
                        </div>
                      );
                    })()}
                  </div>
                ) : (
                  // Показываем кнопку бронирования
                  <Dialog open={isReservationOpen} onOpenChange={setIsReservationOpen}>
                    <DialogTrigger asChild>
                      <Button className="w-full" size="lg">
                        <Users className="h-4 w-4 mr-2" />
                        Забронировать
                      </Button>
                    </DialogTrigger>
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Бронирование тура</DialogTitle>
                        <DialogDescription>
                          {tour.title} — {formatPrice(tour.price)} / чел.
                        </DialogDescription>
                      </DialogHeader>
                      <form onSubmit={reservationForm.handleSubmit(onReservationSubmit)}>
                        <div className="space-y-4 py-4">
                          <div className="space-y-2">
                            <Label htmlFor="notes">Примечания (опционально)</Label>
                            <Textarea
                              id="notes"
                              placeholder="Дополнительные пожелания..."
                              {...reservationForm.register('notes')}
                            />
                          </div>
                        </div>
                        <DialogFooter>
                          <Button
                            type="button"
                            variant="outline"
                            onClick={() => setIsReservationOpen(false)}
                          >
                            Отмена
                          </Button>
                          <Button type="submit" disabled={reservationMutation.isPending}>
                            {reservationMutation.isPending && (
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            )}
                            Забронировать
                          </Button>
                        </DialogFooter>
                      </form>
                    </DialogContent>
                  </Dialog>
                )
              ) : (
                <div className="space-y-4">
                  <p className="text-sm text-muted-foreground text-center">
                    Войдите, чтобы забронировать тур
                  </p>
                  <Button asChild className="w-full">
                    <Link to="/login">Войти</Link>
                  </Button>
                </div>
              )}
            </CardContent>
            <CardFooter className="flex flex-col items-start text-sm text-muted-foreground">
              <p>✓ Бесплатная отмена за 24 часа</p>
              <p>✓ Безопасная оплата</p>
              <p>✓ Поддержка 24/7</p>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  );
}
