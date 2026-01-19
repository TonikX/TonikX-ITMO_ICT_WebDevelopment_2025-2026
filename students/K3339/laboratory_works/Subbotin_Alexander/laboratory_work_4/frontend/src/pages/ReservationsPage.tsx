import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { Loader2, Trash2, MapPin, Calendar, Check, X, Clock } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useToast } from '@/components/ui/use-toast';
import { reservationsApi } from '@/api';
import type { Reservation } from '@/types';

export function ReservationsPage() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [deleteId, setDeleteId] = useState<number | null>(null);

  const { data: reservations, isLoading, error } = useQuery({
    queryKey: ['reservations'],
    queryFn: () => reservationsApi.getMy(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => reservationsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reservations'] });
      toast({
        title: 'Успешно!',
        description: 'Бронирование отменено',
      });
      setDeleteId(null);
    },
    onError: (error: any) => {
      const message = error?.response?.data?.detail || 'Не удалось отменить бронирование';
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: message,
      });
      setDeleteId(null);
    },
  });

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const getStatusBadge = (reservation: Reservation) => {
    switch (reservation.status) {
      case 'confirmed':
        return <Badge className="bg-green-500"><Check className="h-3 w-3 mr-1" />Подтверждено</Badge>;
      case 'rejected':
        return <Badge variant="destructive"><X className="h-3 w-3 mr-1" />Отклонено</Badge>;
      default:
        return <Badge variant="secondary"><Clock className="h-3 w-3 mr-1" />Ожидает</Badge>;
    }
  };

  // Можно отменить только ожидающие брони
  const canCancel = (reservation: Reservation) => reservation.status === 'pending';

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
          Ошибка при загрузке бронирований. Попробуйте позже.
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Мои бронирования</h1>
        <p className="text-muted-foreground">История ваших бронирований</p>
      </div>

      {reservations && reservations.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground mb-4">У вас пока нет бронирований</p>
          <Button asChild>
            <Link to="/tours">Выбрать тур</Link>
          </Button>
        </div>
      ) : (
        <div className="grid gap-6">
          {reservations?.map((reservation) => (
            <Card key={reservation.id}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle>
                      <Link
                        to={`/tours/${reservation.tour.id}`}
                        className="hover:underline"
                      >
                        {reservation.tour.title}
                      </Link>
                    </CardTitle>
                    <CardDescription>{reservation.tour.agency}</CardDescription>
                  </div>
                  {getStatusBadge(reservation)}
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="flex items-center">
                    <MapPin className="h-4 w-4 mr-2 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">Город</p>
                      <p className="text-sm text-muted-foreground">{reservation.tour.city}</p>
                    </div>
                  </div>
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">Даты</p>
                      <p className="text-sm text-muted-foreground">
                        {format(new Date(reservation.tour.start_date), 'd MMM', { locale: ru })} —{' '}
                        {format(new Date(reservation.tour.end_date), 'd MMM', { locale: ru })}
                      </p>
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Стоимость</p>
                    <p className="text-lg font-bold">
                      {formatPrice(reservation.tour.price)}
                    </p>
                  </div>
                </div>
                {reservation.notes && (
                  <div className="mt-4 p-3 bg-muted rounded-lg">
                    <p className="text-sm font-medium">Примечания:</p>
                    <p className="text-sm text-muted-foreground">{reservation.notes}</p>
                  </div>
                )}
              </CardContent>
              <CardFooter className="flex justify-between">
                <p className="text-sm text-muted-foreground">
                  Забронировано: {format(new Date(reservation.created_at), 'd MMMM yyyy', { locale: ru })}
                </p>
                {canCancel(reservation) && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setDeleteId(reservation.id)}
                  >
                    <Trash2 className="h-4 w-4 mr-2 text-destructive" />
                    Отменить
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={deleteId !== null} onOpenChange={() => setDeleteId(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Отменить бронирование?</DialogTitle>
            <DialogDescription>
              Это действие нельзя отменить. Бронирование будет удалено.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setDeleteId(null)}>
              Отмена
            </Button>
            <Button
              variant="destructive"
              onClick={() => deleteId && deleteMutation.mutate(deleteId)}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending && (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              )}
              Подтвердить отмену
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
