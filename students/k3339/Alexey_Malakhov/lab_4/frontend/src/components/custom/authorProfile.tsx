import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar'
import { Skeleton } from '../ui/skeleton'
import { Button } from '../ui/button'
import { useAuth } from '@/contexts/AuthContext'

type AuthorData = {
  id: number
  name: string
  handle: string
  bio: string
  user_id: number
}

type Props = {
  author_id: number | null
}

const AuthorProfile = ({ author_id }: Props) => {
  const [author, setAuthor] = useState<AuthorData | null>(null)
  const [isSubscribed, setIsSubscribed] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { user } = useAuth()

  useEffect(() => {
    if (!author_id) return

    const controller = new AbortController()
    axios
      .get<AuthorData>(`/api/v1/authors/${author_id}`, { signal: controller.signal })
      .then((res) => setAuthor(res.data))
      .catch(() => setAuthor(null))

    // Проверяем, подписан ли пользователь
    if (user) {
      axios
        .get('/api/v1/subscriptions/', { signal: controller.signal })
        .then((res) => {
          const subscriptions = res.data
          const hasSubscription = subscriptions.some((sub: any) => sub.author_id === author_id)
          setIsSubscribed(hasSubscription)
        })
        .catch(() => setIsSubscribed(false))
    }

    return () => controller.abort()
  }, [author_id, user])

  const handleSubscribe = async () => {
    if (!author_id || !user) return

    setIsLoading(true)
    try {
      await axios.post('/api/v1/subscriptions/', {
        author_id: author_id,
        duration_days: 30,
      })
      setIsSubscribed(true)
    } catch (error) {
      console.error('Subscription failed:', error)
      alert('Не удалось оформить подписку')
    } finally {
      setIsLoading(false)
    }
  }

  if (!author) return null

  return (
    <div className='pb-3 flex justify-center flex-col items-center'>
      <div>
        <Avatar className='h-48 w-48'>
          <AvatarImage
            src={`/api/v1/authors/${author.id}/avatar`}
            loading='lazy'
            onError={(e) => {
              const target = e.target as HTMLImageElement
              target.src = '/default-avatar.png'
            }}
          />
          <AvatarFallback>
            <img src='/default-avatar.png' alt='Default avatar' className='h-full w-full object-cover' />
          </AvatarFallback>
        </Avatar>
      </div>
      <p className='text-lg font-bold mt-2'>{author.name}</p>
      <p className='text-sm text-gray-500'>{author.handle}</p>
      <p className='text-sm text-gray-400 mt-1 max-w-4/5 text-center'>{author.bio}</p>

      {user && !isSubscribed && user.id !== author.user_id && (
        <Button
          onClick={handleSubscribe}
          disabled={isLoading}
          className='mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2'
        >
          {isLoading ? 'Подписываюсь...' : 'Подписаться на 30 дней за 40$'}
        </Button>
      )}

      {user && isSubscribed && <p className='mt-4 text-sm text-green-500'>Вы подписаны на этого автора</p>}
    </div>
  )
}

export default AuthorProfile
