import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { Loader2, MapPin, Calendar, Check, X, User, TrendingUp, DollarSign, Users, Clock } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';
import { reservationsApi } from '@/api';
import { useAuthStore } from '@/store';
import type { ReservationAdmin, ReservationStatus } from '@/types';

export function AdminReservationsPage() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const { user } = useAuthStore();
  const [filter, setFilter] = useState<string>('all');

  // Redirect if not admin
  if (!user?.is_admin) {
    return (
      <div className="container py-8">
        <div className="text-center text-destructive">
          Доступ запрещён. Требуются права администратора.
        </div>
      </div>
    );
  }

  const statusParam: ReservationStatus | undefined = filter === 'all' ? undefined : filter as ReservationStatus;

  const { data: reservations, isLoading, error } = useQuery({
    queryKey: ['admin-reservations', filter],
    queryFn: () => reservationsApi.getAllAdmin({ status: statusParam }),
  });

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: () => reservationsApi.getStats(),
  });

  const confirmMutation = useMutation({
    mutationFn: (id: number) => reservationsApi.confirm(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-reservations'] });
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] });
      toast({
        title: 'Успешно!',
        description: 'Бронирование подтверждено',
      });
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось подтвердить бронирование',
      });
    },
  });

  const rejectMutation = useMutation({
    mutationFn: (id: number) => reservationsApi.reject(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-reservations'] });
      queryClient.invalidateQueries({ queryKey: ['admin-stats'] });
      toast({
        title: 'Успешно!',
        description: 'Бронирование отклонено',
      });
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось отклонить бронирование',
      });
    },
  });

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0,
    }).format(price);
  };

  const getStatusBadge = (reservation: ReservationAdmin) => {
    switch (reservation.status) {
      case 'confirmed':
        return <Badge className="bg-green-500"><Check className="h-3 w-3 mr-1" />Подтверждено</Badge>;
      case 'rejected':
        return <Badge variant="destructive"><X className="h-3 w-3 mr-1" />Отклонено</Badge>;
      default:
        return <Badge variant="secondary"><Clock className="h-3 w-3 mr-1" />Ожидает</Badge>;
    }
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
          Ошибка при загрузке бронирований. Попробуйте позже.
        </div>
      </div>
    );
  }

  return (
    <div className="container py-8">
      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Подтверждённых бронирований</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? <Loader2 className="h-6 w-6 animate-spin" /> : stats?.confirmed_reservations || 0}
            </div>
            <p className="text-xs text-muted-foreground">Проданных туров</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Общая выручка</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? <Loader2 className="h-6 w-6 animate-spin" /> : formatPrice(stats?.total_revenue || 0)}
            </div>
            <p className="text-xs text-muted-foreground">От подтверждённых бронирований</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Клиентов</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {statsLoading ? <Loader2 className="h-6 w-6 animate-spin" /> : stats?.total_customers || 0}
            </div>
            <p className="text-xs text-muted-foreground">Уникальных покупателей</p>
          </CardContent>
        </Card>
      </div>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold">Управление бронированиями</h1>
          <p className="text-muted-foreground">Администрирование всех бронирований</p>
        </div>
        <Select value={filter} onValueChange={setFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Фильтр" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все</SelectItem>
            <SelectItem value="pending">Ожидающие</SelectItem>
            <SelectItem value="confirmed">Подтверждённые</SelectItem>
            <SelectItem value="rejected">Отклонённые</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {reservations && reservations.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-muted-foreground">Бронирования не найдены</p>
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
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                  <div className="flex items-center">
                    <User className="h-4 w-4 mr-2 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">Пользователь</p>
                      <p className="text-sm text-muted-foreground">{reservation.username || 'Неизвестно'}</p>
                    </div>
                  </div>
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
                  <div className="mb-4 p-3 bg-muted rounded-lg">
                    <p className="text-sm font-medium">Заметки:</p>
                    <p className="text-sm text-muted-foreground">{reservation.notes}</p>
                  </div>
                )}
                <div className="flex gap-2 justify-end">
                  {reservation.status === 'pending' && (
                    <>
                      <Button
                        size="sm"
                        onClick={() => confirmMutation.mutate(reservation.id)}
                        disabled={confirmMutation.isPending}
                      >
                        {confirmMutation.isPending ? (
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        ) : (
                          <Check className="h-4 w-4 mr-2" />
                        )}
                        Подтвердить
                      </Button>
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => rejectMutation.mutate(reservation.id)}
                        disabled={rejectMutation.isPending}
                      >
                        {rejectMutation.isPending ? (
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        ) : (
                          <X className="h-4 w-4 mr-2" />
                        )}
                        Отклонить
                      </Button>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
