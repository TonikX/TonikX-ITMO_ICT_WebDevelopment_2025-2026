import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Field, FieldDescription, FieldGroup, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'

export function SignupForm({ ...props }: React.ComponentProps<typeof Card>) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { refreshUser } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ name, email, password }),
      })

      const data = await res.json().catch(() => ({}))
      if (res.ok) {
        await refreshUser()
        await new Promise((resolve) => setTimeout(resolve, 100))
        navigate('/profile')
      } else {
        setError((data && (data.error || data.detail)) || 'Ошибка регистрации')
      }
    } catch (err) {
      setError('Ошибка сети')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>Создайте аккаунт</CardTitle>
        <CardDescription>Введите свои данные ниже, чтобы создать учетную запись.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor='name'>Имя</FieldLabel>
              <Input
                id='name'
                type='text'
                placeholder='Иван Иванов'
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </Field>
            <Field>
              <FieldLabel htmlFor='email'>Электронная почта</FieldLabel>
              <Input
                id='email'
                type='email'
                placeholder='example@mail.com'
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Field>
            <Field>
              <FieldLabel htmlFor='password'>Пароль</FieldLabel>
              <Input
                id='password'
                type='password'
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <FieldDescription>Пароль должен содержать не менее 8 символов.</FieldDescription>
            </Field>
            {error && (
              <div className='text-sm text-red-600 px-2' role='alert'>
                {error}
              </div>
            )}
            <FieldGroup>
              <Field>
                <Button type='submit' disabled={loading}>
                  {loading ? 'Создание...' : 'Создать аккаунт'}
                </Button>
                <FieldDescription className='px-6 text-center'>
                  Уже есть аккаунт? <a href='/login'>Войти</a>
                </FieldDescription>
              </Field>
            </FieldGroup>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  )
}
