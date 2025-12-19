import axios from 'axios'
import { useEffect, useState } from 'react'
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar'
import AuthorProfile from '../custom/AuthorProfile'

type AuthorData = {
  id: number
  name: string
  handle: string
  bio: string
  is_verified: boolean
  created_at: string
  updated_at: string
}

type SubscriptionRead = {
  id: number
  subscriber_id: number
  author_id: number
  started_at: string
  expires_at: string | null
}

type UserRead = {
  id: number
  name: string
  email: string
  subscriptions: SubscriptionRead[]
}

type Props = {
  activeAuthor: number | null
  onSelectAuthor: (id: number | null) => void
}

const Authors = ({ activeAuthor, onSelectAuthor }: Props) => {
  const [authors, setAuthors] = useState<AuthorData[] | null>(null)
  const [user, setUser] = useState<UserRead | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    // Загружаем авторов
    axios
      .get<AuthorData[]>('/api/v1/authors/', { signal: controller.signal })
      .then((res) => setAuthors(res.data))
      .catch(() => setAuthors([]))

    // Загружаем данные пользователя (если авторизован)
    fetch('/api/v1/auth/me', { credentials: 'include', signal: controller.signal })
      .then((res) => (res.ok ? res.json() : null))
      .then((data: UserRead | null) => setUser(data))
      .catch(() => setUser(null))

    return () => controller.abort()
  }, [])

  const selectedAuthor = authors?.find((author) => author.id === activeAuthor)

  // Множество author_id, на которых подписан юзер
  const subscribedAuthorIds = new Set(user?.subscriptions.map((s) => s.author_id) || [])

  return (
    <div className='pt-14'>
      {activeAuthor && selectedAuthor && <AuthorProfile author_id={selectedAuthor.id} />}
      <div className='flex flex-row gap-2 overflow-x-scroll overflow-y-hidden scrollbar-hide pt-2'>
        {authors?.map((author) => {
          const isSubscribed = subscribedAuthorIds.has(author.id)
          const isActive = activeAuthor === author.id

          return (
            <a key={author.id} onClick={() => onSelectAuthor(isActive ? null : author.id)}>
              <div className={'relative flex flex-col items-center'}>
                <div
                  className={`absolute bottom-0 left-0 w-full h-full z-0 transition-transform duration-300 rounded-t-full 
                  ${isActive ? 'bg-zinc-800 scale-110' : 'bg-transparent'}`}
                />
                <Avatar className={`h-16 w-16 ${isSubscribed ? 'outline-3 outline-blue-400' : ''}`}>
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
                <span
                  className={`text-xs text-center mt-2 w-16 h-5 truncate relative z-10 ${
                    isSubscribed ? 'text-blue-400 font-semibold' : 'text-zinc-600'
                  }`}
                >
                  {author.name}
                </span>{' '}
              </div>
            </a>
          )
        })}
      </div>
    </div>
  )
}

export default Authors
