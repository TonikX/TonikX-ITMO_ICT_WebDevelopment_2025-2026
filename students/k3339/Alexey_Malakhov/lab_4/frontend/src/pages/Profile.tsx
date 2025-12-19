import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import axios from 'axios'

type AuthorData = {
  id: number
  name: string
  handle: string
}

const Profile = () => {
  const { user, loading, refreshUser } = useAuth()
  const [editing, setEditing] = useState(false)
  const [updateLoading, setUpdateLoading] = useState(false)
  const [updateError, setUpdateError] = useState<string | null>(null)
  const [updateSuccess, setUpdateSuccess] = useState(false)
  const [logoutLoading, setLogoutLoading] = useState(false)
  const [authors, setAuthors] = useState<Record<number, AuthorData>>({})

  // Состояния для создания автора
  const [creatingAuthor, setCreatingAuthor] = useState(false)
  const [authorName, setAuthorName] = useState('')
  const [authorHandle, setAuthorHandle] = useState('')
  const [authorBio, setAuthorBio] = useState('')
  const [authorAvatar, setAuthorAvatar] = useState<File | null>(null)
  const [authorCreateLoading, setAuthorCreateLoading] = useState(false)
  const [authorCreateError, setAuthorCreateError] = useState<string | null>(null)

  // Состояния для удаления автора
  const [deleteAuthorLoading, setDeleteAuthorLoading] = useState(false)
  const [deleteAuthorError, setDeleteAuthorError] = useState<string | null>(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  // Состояния для управления подписками
  const [subscriptionLoading, setSubscriptionLoading] = useState<number | null>(null)
  const [subscriptionError, setSubscriptionError] = useState<string | null>(null)

  const [formName, setFormName] = useState(user?.name || '')
  const [formEmail, setFormEmail] = useState(user?.email || '')
  const [formPassword, setFormPassword] = useState('')
  const [formCurrentPassword, setFormCurrentPassword] = useState('')

  const navigate = useNavigate()

  useEffect(() => {
    if (!loading && !user) {
      navigate('/login')
    }
  }, [user, loading, navigate])

  useEffect(() => {
    if (user?.subscriptions && user.subscriptions.length > 0) {
      const authorIds = [...new Set(user.subscriptions.map((sub) => sub.author_id))]

      Promise.all(
        authorIds.map((id) =>
          axios
            .get<AuthorData>(`/api/v1/authors/${id}`)
            .then((res) => ({ id, data: res.data }))
            .catch(() => ({ id, data: null }))
        )
      ).then((results) => {
        const authorsMap: Record<number, AuthorData> = {}
        results.forEach(({ id, data }) => {
          if (data) authorsMap[id] = data
        })
        setAuthors(authorsMap)
      })
    }
  }, [user])

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    setUpdateLoading(true)
    setUpdateError(null)
    setUpdateSuccess(false)

    try {
      const payload: any = { current_password: formCurrentPassword }
      if (formName !== user?.name) payload.name = formName
      if (formEmail !== user?.email) payload.email = formEmail
      if (formPassword) payload.password = formPassword

      const res = await fetch('/api/v1/auth/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload),
      })

      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || 'Ошибка обновления профиля')
      }

      await refreshUser()
      setFormPassword('')
      setFormCurrentPassword('')
      setEditing(false)
      setUpdateSuccess(true)
    } catch (e: any) {
      setUpdateError(e.message || 'Ошибка обновления')
    } finally {
      setUpdateLoading(false)
    }
  }

  const handleCreateAuthor = async (e: React.FormEvent) => {
    e.preventDefault()
    setAuthorCreateLoading(true)
    setAuthorCreateError(null)

    try {
      const formData = new FormData()
      formData.append('name', authorName)
      formData.append('handle', authorHandle)
      if (authorBio) formData.append('bio', authorBio)
      formData.append('is_verified', 'false')
      if (authorAvatar) formData.append('avatar', authorAvatar)

      await axios.post('/api/v1/authors/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      await refreshUser()
      setCreatingAuthor(false)
      setAuthorName('')
      setAuthorHandle('')
      setAuthorBio('')
      setAuthorAvatar(null)
    } catch (error: any) {
      const detail = error.response?.data?.detail
      if (typeof detail === 'string') {
        setAuthorCreateError(detail)
      } else if (Array.isArray(detail)) {
        setAuthorCreateError(detail.map((err: any) => err.msg).join(', '))
      } else {
        setAuthorCreateError('Не удалось создать профиль автора')
      }
    } finally {
      setAuthorCreateLoading(false)
    }
  }

  const handleDeleteAuthor = async () => {
    if (!user) return

    setDeleteAuthorLoading(true)
    setDeleteAuthorError(null)

    try {
      // Получаем ID автора пользователя
      const authorsResponse = await axios.get(`/api/v1/authors/?user_id=${user.id}`)
      if (!Array.isArray(authorsResponse.data) || authorsResponse.data.length === 0) {
        throw new Error('Профиль автора не найден')
      }

      const authorId = authorsResponse.data[0].id

      // Удаляем профиль автора
      await axios.delete(`/api/v1/authors/${authorId}`)

      // Обновляем данные пользователя
      await refreshUser()
      setShowDeleteConfirm(false)
    } catch (error: any) {
      setDeleteAuthorError(error.response?.data?.detail || 'Не удалось удалить профиль автора')
    } finally {
      setDeleteAuthorLoading(false)
    }
  }

  const handleCancelSubscription = async (subscriptionId: number) => {
    console.log('Отмена подписки:', subscriptionId)
    setSubscriptionLoading(subscriptionId)
    setSubscriptionError(null)
    try {
      const response = await axios.put(`/api/v1/subscriptions/${subscriptionId}/cancel`)
      console.log('Ответ отмены:', response.data)
      await refreshUser()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } }
      console.error('Ошибка отмены подписки:', err)
      setSubscriptionError(err.response?.data?.detail || 'Не удалось отменить подписку')
    } finally {
      setSubscriptionLoading(null)
    }
  }

  const handleRenewSubscription = async (subscriptionId: number) => {
    console.log('Восстановление подписки:', subscriptionId)
    setSubscriptionLoading(subscriptionId)
    setSubscriptionError(null)
    try {
      const response = await axios.put(`/api/v1/subscriptions/${subscriptionId}/renew`)
      console.log('Ответ восстановления:', response.data)
      await refreshUser()
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string } } }
      console.error('Ошибка восстановления подписки:', err)
      setSubscriptionError(err.response?.data?.detail || 'Не удалось восстановить подписку')
    } finally {
      setSubscriptionLoading(null)
    }
  }

  const handleLogout = async () => {
    setLogoutLoading(true)
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'GET',
        credentials: 'include',
      })
      await refreshUser()
      await new Promise((resolve) => setTimeout(resolve, 500))
      navigate('/login')
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      setLogoutLoading(false)
    }
  }

  if (loading) {
    return (
      <div className='container max-w-3xl mx-auto pt-14'>
        <Card>
          <CardHeader>
            <CardTitle>Загрузка профиля…</CardTitle>
            <CardDescription>Пожалуйста, подождите</CardDescription>
          </CardHeader>
          <CardContent>
            <div className='h-4 w-full bg-muted rounded mb-2' />
            <div className='h-4 w-5/6 bg-muted rounded' />
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className='container max-w-4xl mx-auto pt-14 space-y-6'>
      {updateSuccess && (
        <Alert>
          <AlertTitle>Успешно</AlertTitle>
          <AlertDescription>Профиль обновлён</AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <div className='flex items-center justify-between'>
            <div>
              <CardTitle className='text-xl'>Профиль</CardTitle>
              <CardDescription>Информация о пользователе</CardDescription>
            </div>
            <div className='flex gap-2'>
              {!editing && (
                <Button variant='outline' onClick={() => setEditing(true)}>
                  Редактировать
                </Button>
              )}
              <Button variant='destructive' onClick={handleLogout} disabled={logoutLoading}>
                {logoutLoading ? 'Выход...' : 'Выйти'}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className='space-y-4'>
          {!editing ? (
            <>
              <div className='flex gap-2 items-center'>
                <Badge variant='secondary'>ID: {user.id}</Badge>
                <Badge>{user.email}</Badge>
                {user.is_author && <Badge variant='default'>Автор</Badge>}
              </div>
              <Separator />
              <div className='text-lg font-semibold'>{user.name}</div>
            </>
          ) : (
            <form onSubmit={handleUpdate} className='space-y-4'>
              <div className='space-y-2'>
                <Label htmlFor='name'>Имя</Label>
                <Input id='name' value={formName} onChange={(e) => setFormName(e.target.value)} />
              </div>
              <div className='space-y-2'>
                <Label htmlFor='email'>Email</Label>
                <Input id='email' type='email' value={formEmail} onChange={(e) => setFormEmail(e.target.value)} />
              </div>
              <div className='space-y-2'>
                <Label htmlFor='password'>Новый пароль (оставьте пустым, если не меняете)</Label>
                <Input
                  id='password'
                  type='password'
                  value={formPassword}
                  onChange={(e) => setFormPassword(e.target.value)}
                />
              </div>
              <Separator />
              <div className='space-y-2'>
                <Label htmlFor='current_password'>Текущий пароль (обязательно)</Label>
                <Input
                  id='current_password'
                  type='password'
                  required
                  value={formCurrentPassword}
                  onChange={(e) => setFormCurrentPassword(e.target.value)}
                />
              </div>
              {updateError && (
                <Alert variant='destructive'>
                  <AlertDescription>{updateError}</AlertDescription>
                </Alert>
              )}
              <div className='flex gap-2'>
                <Button type='submit' disabled={updateLoading}>
                  {updateLoading ? 'Сохранение...' : 'Сохранить'}
                </Button>
                <Button
                  type='button'
                  variant='outline'
                  onClick={() => {
                    setEditing(false)
                    setFormName(user.name)
                    setFormEmail(user.email)
                    setFormPassword('')
                    setFormCurrentPassword('')
                    setUpdateError(null)
                  }}
                >
                  Отмена
                </Button>
              </div>
            </form>
          )}
        </CardContent>
      </Card>

      {/* Карточка для создания/удаления профиля автора */}
      {!user.is_author ? (
        <Card>
          <CardHeader>
            <CardTitle>Профиль автора</CardTitle>
            <CardDescription>Создайте профиль автора для публикации контента</CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            {!creatingAuthor ? (
              <Button onClick={() => setCreatingAuthor(true)}>Создать профиль автора</Button>
            ) : (
              <form onSubmit={handleCreateAuthor} className='space-y-4'>
                <div className='space-y-2'>
                  <Label htmlFor='author_name'>Название канала</Label>
                  <Input
                    id='author_name'
                    placeholder='Мой канал'
                    value={authorName}
                    onChange={(e) => setAuthorName(e.target.value)}
                    required
                  />
                </div>
                <div className='space-y-2'>
                  <Label htmlFor='author_handle'>Хэндл (идентификатор)</Label>
                  <Input
                    id='author_handle'
                    placeholder='mychannel'
                    value={authorHandle}
                    onChange={(e) => {
                      const value = e.target.value
                      // Разрешаем только английские буквы, цифры, дефис, нижнее подчеркивание
                      if (/^[a-zA-Z0-9_-]*$/.test(value)) {
                        setAuthorHandle(value)
                      }
                    }}
                    required
                  />
                  <p className='text-xs text-muted-foreground'>Только латиница, цифры, _ -</p>
                </div>
                <div className='space-y-2'>
                  <Label htmlFor='author_bio'>Биография</Label>
                  <Textarea
                    id='author_bio'
                    placeholder='Расскажите о себе...'
                    value={authorBio}
                    onChange={(e) => setAuthorBio(e.target.value)}
                    className='min-h-[100px]'
                  />
                </div>
                <div className='space-y-2'>
                  <Label htmlFor='author_avatar'>Аватар (необязательно)</Label>
                  <Input
                    id='author_avatar'
                    type='file'
                    accept='image/jpeg,image/png,image/jpg'
                    onChange={(e) => setAuthorAvatar(e.target.files?.[0] || null)}
                  />
                  {authorAvatar && <p className='text-sm text-muted-foreground'>Выбран файл: {authorAvatar.name}</p>}
                </div>
                {authorCreateError && (
                  <Alert variant='destructive'>
                    <AlertDescription>{authorCreateError}</AlertDescription>
                  </Alert>
                )}
                <div className='flex gap-2'>
                  <Button type='submit' disabled={authorCreateLoading}>
                    {authorCreateLoading ? 'Создание...' : 'Создать'}
                  </Button>
                  <Button
                    type='button'
                    variant='outline'
                    onClick={() => {
                      setCreatingAuthor(false)
                      setAuthorName('')
                      setAuthorHandle('')
                      setAuthorBio('')
                      setAuthorAvatar(null)
                      setAuthorCreateError(null)
                    }}
                  >
                    Отмена
                  </Button>
                </div>
              </form>
            )}
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Профиль автора</CardTitle>
            <CardDescription>Управление профилем автора</CardDescription>
          </CardHeader>
          <CardContent className='space-y-4'>
            {!showDeleteConfirm ? (
              <div className='space-y-2'>
                <p className='text-sm text-muted-foreground'>У вас есть активный профиль автора</p>
                <Button variant='destructive' onClick={() => setShowDeleteConfirm(true)}>
                  Удалить профиль автора
                </Button>
              </div>
            ) : (
              <div className='space-y-4'>
                <Alert variant='destructive'>
                  <AlertTitle>Внимание!</AlertTitle>
                  <AlertDescription>
                    Вы уверены, что хотите удалить профиль автора? Все ваши посты и контент будут удалены. Это действие
                    необратимо.
                  </AlertDescription>
                </Alert>
                {deleteAuthorError && (
                  <Alert variant='destructive'>
                    <AlertDescription>{deleteAuthorError}</AlertDescription>
                  </Alert>
                )}
                <div className='flex gap-2'>
                  <Button variant='destructive' onClick={handleDeleteAuthor} disabled={deleteAuthorLoading}>
                    {deleteAuthorLoading ? 'Удаление...' : 'Подтвердить удаление'}
                  </Button>
                  <Button
                    variant='outline'
                    onClick={() => {
                      setShowDeleteConfirm(false)
                      setDeleteAuthorError(null)
                    }}
                  >
                    Отмена
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Подписки</CardTitle>
          <CardDescription>Список активных подписок</CardDescription>
        </CardHeader>
        <CardContent className='space-y-4'>
          {subscriptionError && (
            <Alert variant='destructive'>
              <AlertDescription>{subscriptionError}</AlertDescription>
            </Alert>
          )}
          {user.subscriptions && user.subscriptions.length > 0 ? (
            <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
              {user.subscriptions.map((sub) => {
                console.log('Подписка:', sub)
                return (
                  <div key={sub.id} className='border rounded p-3 space-y-2'>
                    <div className='flex items-center justify-between'>
                      <div className='font-medium'>{authors[sub.author_id]?.name || `Автор #${sub.author_id}`}</div>
                      <Badge variant={sub.expires_at ? 'default' : 'secondary'}>
                        {sub.expires_at ? 'До ' + new Date(sub.expires_at).toLocaleDateString() : 'Бессрочная'}
                      </Badge>
                    </div>
                    <div className='text-sm text-muted-foreground'>
                      Начало: {new Date(sub.started_at).toLocaleDateString()}
                    </div>
                    <div className='flex items-center justify-between'>
                      <div className='text-xs text-muted-foreground'>
                        {sub.renewable ? (
                          <span className='text-green-600'>✓ Автопродление включено</span>
                        ) : (
                          <span className='text-orange-600'>⚠ Автопродление отключено</span>
                        )}
                      </div>
                    </div>
                    <div className='flex gap-2'>
                      {sub.renewable ? (
                        <Button
                          size='sm'
                          variant='outline'
                          onClick={() => handleCancelSubscription(sub.id)}
                          disabled={subscriptionLoading === sub.id}
                        >
                          {subscriptionLoading === sub.id ? 'Отмена...' : 'Отменить автопродление'}
                        </Button>
                      ) : (
                        <Button
                          size='sm'
                          variant='default'
                          onClick={() => handleRenewSubscription(sub.id)}
                          disabled={subscriptionLoading === sub.id}
                        >
                          {subscriptionLoading === sub.id ? 'Восстановление...' : 'Восстановить автопродление'}
                        </Button>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className='text-sm text-muted-foreground'>Нет подписок</div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default Profile
