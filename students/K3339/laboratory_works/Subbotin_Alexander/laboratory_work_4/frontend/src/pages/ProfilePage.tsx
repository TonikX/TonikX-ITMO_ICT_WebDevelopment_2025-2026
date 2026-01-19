import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Loader2, User, Mail, Calendar, Lock, Edit2 } from 'lucide-react';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { useToast } from '@/components/ui/use-toast';
import { authApi } from '@/api';
import { useAuthStore } from '@/store';

const profileSchema = z.object({
  date_of_birth: z.string().optional(),
});

const userSchema = z.object({
  username: z.string().min(3, 'Минимум 3 символа').max(150),
  email: z.string().email('Некорректный email'),
});

const passwordSchema = z.object({
  currentPassword: z.string().min(1, 'Введите текущий пароль'),
  newPassword: z.string().min(6, 'Минимум 6 символов'),
  confirmPassword: z.string().min(6, 'Минимум 6 символов'),
}).refine((data) => data.newPassword === data.confirmPassword, {
  message: 'Пароли не совпадают',
  path: ['confirmPassword'],
});

type ProfileFormData = z.infer<typeof profileSchema>;
type UserFormData = z.infer<typeof userSchema>;
type PasswordFormData = z.infer<typeof passwordSchema>;

export function ProfilePage() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const { user, fetchUser } = useAuthStore();
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isEditingUser, setIsEditingUser] = useState(false);
  const [isPasswordDialogOpen, setIsPasswordDialogOpen] = useState(false);

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: authApi.getProfile,
  });

  // Profile mutation (date_of_birth)
  const updateProfileMutation = useMutation({
    mutationFn: authApi.updateProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] });
      toast({
        title: 'Успешно!',
        description: 'Профиль обновлён',
      });
      setIsEditingProfile(false);
    },
    onError: () => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: 'Не удалось обновить профиль',
      });
    },
  });

  // User mutation (username, email)
  const updateUserMutation = useMutation({
    mutationFn: authApi.updateUser,
    onSuccess: async () => {
      await fetchUser();
      toast({
        title: 'Успешно!',
        description: 'Данные обновлены',
      });
      setIsEditingUser(false);
    },
    onError: (error: any) => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: error.response?.data?.detail || 'Не удалось обновить данные',
      });
    },
  });

  // Password mutation
  const changePasswordMutation = useMutation({
    mutationFn: ({ currentPassword, newPassword }: { currentPassword: string; newPassword: string }) =>
      authApi.changePassword(currentPassword, newPassword),
    onSuccess: () => {
      toast({
        title: 'Успешно!',
        description: 'Пароль изменён',
      });
      setIsPasswordDialogOpen(false);
      passwordForm.reset();
    },
    onError: (error: any) => {
      toast({
        variant: 'destructive',
        title: 'Ошибка',
        description: error.response?.data?.detail || 'Не удалось изменить пароль',
      });
    },
  });

  const profileForm = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      date_of_birth: profile?.date_of_birth ? format(new Date(profile.date_of_birth), 'yyyy-MM-dd') : '',
    },
  });

  const userForm = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      username: user?.username || '',
      email: user?.email || '',
    },
  });

  const passwordForm = useForm<PasswordFormData>({
    resolver: zodResolver(passwordSchema),
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    },
  });

  const onProfileSubmit = async (data: ProfileFormData) => {
    updateProfileMutation.mutate({
      date_of_birth: data.date_of_birth || undefined,
    });
  };

  const onUserSubmit = async (data: UserFormData) => {
    updateUserMutation.mutate(data);
  };

  const onPasswordSubmit = async (data: PasswordFormData) => {
    changePasswordMutation.mutate({
      currentPassword: data.currentPassword,
      newPassword: data.newPassword,
    });
  };

  const handleCancelProfile = () => {
    setIsEditingProfile(false);
    profileForm.reset({
      date_of_birth: profile?.date_of_birth ? format(new Date(profile.date_of_birth), 'yyyy-MM-dd') : '',
    });
  };

  const handleCancelUser = () => {
    setIsEditingUser(false);
    userForm.reset({
      username: user?.username || '',
      email: user?.email || '',
    });
  };

  if (profileLoading) {
    return (
      <div className="container py-8 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="container py-8">
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Профиль</h1>
          <p className="text-muted-foreground">Управление вашими учётными данными</p>
        </div>

        {/* Account Info Card */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Информация об аккаунте</CardTitle>
              <CardDescription>Основные данные вашей учётной записи</CardDescription>
            </div>
            {!isEditingUser && (
              <Button variant="outline" size="sm" onClick={() => setIsEditingUser(true)}>
                <Edit2 className="h-4 w-4 mr-2" />
                Редактировать
              </Button>
            )}
          </CardHeader>
          <CardContent className="space-y-4">
            {isEditingUser ? (
              <form onSubmit={userForm.handleSubmit(onUserSubmit)} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="username">Имя пользователя</Label>
                  <Input
                    id="username"
                    {...userForm.register('username')}
                  />
                  {userForm.formState.errors.username && (
                    <p className="text-sm text-destructive">{userForm.formState.errors.username.message}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    {...userForm.register('email')}
                  />
                  {userForm.formState.errors.email && (
                    <p className="text-sm text-destructive">{userForm.formState.errors.email.message}</p>
                  )}
                </div>
                <div className="flex space-x-2">
                  <Button type="submit" disabled={updateUserMutation.isPending}>
                    {updateUserMutation.isPending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                    Сохранить
                  </Button>
                  <Button type="button" variant="outline" onClick={handleCancelUser}>
                    Отмена
                  </Button>
                </div>
              </form>
            ) : (
              <>
                <div className="flex items-center space-x-4">
                  <User className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Имя пользователя</p>
                    <p className="text-sm text-muted-foreground">{user?.username}</p>
                  </div>
                </div>
                <Separator />
                <div className="flex items-center space-x-4">
                  <Mail className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Email</p>
                    <p className="text-sm text-muted-foreground">{user?.email}</p>
                  </div>
                </div>
                <Separator />
                <div className="flex items-center space-x-4">
                  <Calendar className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">Дата регистрации</p>
                    <p className="text-sm text-muted-foreground">
                      {user?.created_at
                        ? format(new Date(user.created_at), 'd MMMM yyyy', { locale: ru })
                        : 'Не указана'}
                    </p>
                  </div>
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Personal Data Card */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Личные данные</CardTitle>
              <CardDescription>Дополнительная информация о вас</CardDescription>
            </div>
            {!isEditingProfile && (
              <Button variant="outline" size="sm" onClick={() => setIsEditingProfile(true)}>
                <Edit2 className="h-4 w-4 mr-2" />
                Редактировать
              </Button>
            )}
          </CardHeader>
          <CardContent>
            {isEditingProfile ? (
              <form onSubmit={profileForm.handleSubmit(onProfileSubmit)} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="date_of_birth">Дата рождения</Label>
                  <Input
                    id="date_of_birth"
                    type="date"
                    {...profileForm.register('date_of_birth')}
                  />
                </div>
                <div className="flex space-x-2">
                  <Button type="submit" disabled={updateProfileMutation.isPending}>
                    {updateProfileMutation.isPending && (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    )}
                    Сохранить
                  </Button>
                  <Button type="button" variant="outline" onClick={handleCancelProfile}>
                    Отмена
                  </Button>
                </div>
              </form>
            ) : (
              <div className="flex items-center space-x-4">
                <Calendar className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Дата рождения</p>
                  <p className="text-sm text-muted-foreground">
                    {profile?.date_of_birth
                      ? format(new Date(profile.date_of_birth), 'd MMMM yyyy', { locale: ru })
                      : 'Не указана'}
                  </p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Security Card */}
        <Card>
          <CardHeader>
            <CardTitle>Безопасность</CardTitle>
            <CardDescription>Управление паролем</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Lock className="h-5 w-5 text-muted-foreground" />
                <div>
                  <p className="text-sm font-medium">Пароль</p>
                  <p className="text-sm text-muted-foreground">••••••••</p>
                </div>
              </div>
              <Button variant="outline" onClick={() => setIsPasswordDialogOpen(true)}>
                Изменить пароль
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Password Change Dialog */}
        <Dialog open={isPasswordDialogOpen} onOpenChange={setIsPasswordDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Изменить пароль</DialogTitle>
              <DialogDescription>
                Введите текущий пароль и новый пароль
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={passwordForm.handleSubmit(onPasswordSubmit)} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="currentPassword">Текущий пароль</Label>
                <Input
                  id="currentPassword"
                  type="password"
                  {...passwordForm.register('currentPassword')}
                />
                {passwordForm.formState.errors.currentPassword && (
                  <p className="text-sm text-destructive">{passwordForm.formState.errors.currentPassword.message}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="newPassword">Новый пароль</Label>
                <Input
                  id="newPassword"
                  type="password"
                  {...passwordForm.register('newPassword')}
                />
                {passwordForm.formState.errors.newPassword && (
                  <p className="text-sm text-destructive">{passwordForm.formState.errors.newPassword.message}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Подтвердите пароль</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  {...passwordForm.register('confirmPassword')}
                />
                {passwordForm.formState.errors.confirmPassword && (
                  <p className="text-sm text-destructive">{passwordForm.formState.errors.confirmPassword.message}</p>
                )}
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setIsPasswordDialogOpen(false)}>
                  Отмена
                </Button>
                <Button type="submit" disabled={changePasswordMutation.isPending}>
                  {changePasswordMutation.isPending && (
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  )}
                  Изменить
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}
