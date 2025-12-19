import type { Post, Comment } from '@/api/types'
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar'
import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight, Heart, MessageSquare, Edit, Trash2, Send } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

type Props = {
  post: Post
}

const PostBlock = ({ post }: Props) => {
  const { user } = useAuth()
  const [expanded, setExpanded] = useState(false)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [liked, setLiked] = useState(post.is_liked)
  const [likesCount, setLikesCount] = useState(post.likes_count)
  const [commentsOpen, setCommentsOpen] = useState(false)
  const [comments, setComments] = useState<Comment[]>([])
  const [commentsCount, setCommentsCount] = useState(post.comments_count)
  const [newCommentText, setNewCommentText] = useState('')
  const [isEditing, setIsEditing] = useState(false)
  const [editText, setEditText] = useState(post.text || '')
  const contents = post.contents || []
  const hasMedia = contents.length > 0
  const currentContent = contents[currentIndex]

  // Проверяем, является ли текущий пользователь автором поста
  const isOwner = user?.id === post.author.user_id

  // Загрузка комментариев
  const loadComments = async () => {
    try {
      const response = await fetch(`/api/v1/posts/${post.id}/comments`, {
        credentials: 'include',
      })
      if (response.ok) {
        const data = await response.json()
        setComments(data)
      }
    } catch (error) {
      console.error('Failed to load comments:', error)
    }
  }

  // Добавление комментария
  const handleAddComment = async () => {
    if (!newCommentText.trim()) return

    try {
      const token = localStorage.getItem('my_access_token')
      const response = await fetch(`/api/v1/posts/${post.id}/comments`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify({ text: newCommentText }),
      })

      if (response.ok) {
        const newComment = await response.json()
        setComments([newComment, ...comments])
        setCommentsCount(commentsCount + 1)
        setNewCommentText('')
      } else if (response.status === 401) {
        console.error('Unauthorized: Please log in')
      }
    } catch (error) {
      console.error('Failed to add comment:', error)
    }
  }

  // Удаление комментария
  const handleDeleteComment = async (commentId: number) => {
    if (!confirm('Удалить комментарий?')) return

    try {
      const token = localStorage.getItem('my_access_token')
      const response = await fetch(`/api/v1/posts/${post.id}/comments/${commentId}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      })

      if (response.ok) {
        setComments(comments.filter((c) => c.id !== commentId))
        setCommentsCount(commentsCount - 1)
      }
    } catch (error) {
      console.error('Failed to delete comment:', error)
    }
  }

  // Загружаем комментарии при открытии
  useEffect(() => {
    if (commentsOpen && comments.length === 0) {
      loadComments()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [commentsOpen])

  const handleLike = async () => {
    try {
      const token = localStorage.getItem('my_access_token')
      const method = liked ? 'DELETE' : 'POST'
      const response = await fetch(`/api/v1/posts/${post.id}/like`, {
        method,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      })

      if (response.ok) {
        setLiked(!liked)
        setLikesCount((prev) => (liked ? prev - 1 : prev + 1))
      } else if (response.status === 401) {
        console.error('Unauthorized: Please log in')
      }
    } catch (error) {
      console.error('Failed to toggle like:', error)
    }
  }

  const handleEdit = async () => {
    if (!isEditing) {
      setIsEditing(true)
      return
    }

    try {
      const formData = new FormData()
      formData.append('text', editText)

      const response = await fetch(`/api/v1/posts/${post.id}`, {
        method: 'PUT',
        credentials: 'include',
        body: formData,
      })

      if (response.ok) {
        post.text = editText
        setIsEditing(false)
      }
    } catch (error) {
      console.error('Failed to edit post:', error)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Удалить пост?')) return

    try {
      const response = await fetch(`/api/v1/posts/${post.id}`, {
        method: 'DELETE',
        credentials: 'include',
      })

      if (response.ok) {
        window.location.reload()
      }
    } catch (error) {
      console.error('Failed to delete post:', error)
    }
  }

  const nextSlide = () => setCurrentIndex((i) => (i + 1) % contents.length)
  const prevSlide = () => setCurrentIndex((i) => (i - 1 + contents.length) % contents.length)

  const thumbnailUrl = currentContent ? `/api/v1/content/${currentContent.id}/stream` : undefined

  return (
    <div className='mb-4 outline-2 outline-zinc-800 mx-1 rounded-2xl'>
      <div className='flex flex-row px-3 pt-3'>
        <Avatar className='w-10 h-10 mr-3'>
          <AvatarImage src={`/api/v1/authors/${post.author.id}/avatar`} />
          <AvatarFallback>
            {' '}
            <img src='/default-avatar.png' alt='Default avatar' className='h-full w-full object-cover' />
          </AvatarFallback>
        </Avatar>
        <div className='flex flex-col w-full overflow-hidden'>
          <div className='flex w-full justify-between items-center'>
            <p className='text-sm truncate text-zinc-500'>{post.author.name}</p>
            <p className='text-xs text-zinc-600'>{formatDate(post.created_at)}</p>
          </div>
          {post.text && (
            <div className='overflow-hidden'>
              {isEditing ? (
                <div className='space-y-2'>
                  <textarea
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                    className='w-full p-2 text-sm bg-zinc-800 text-white rounded resize-none'
                    rows={4}
                  />
                  <div className='flex gap-2'>
                    <button onClick={handleEdit} className='px-3 py-1 text-xs bg-blue-600 hover:bg-blue-700 rounded'>
                      Сохранить
                    </button>
                    <button
                      onClick={() => {
                        setIsEditing(false)
                        setEditText(post.text || '')
                      }}
                      className='px-3 py-1 text-xs bg-zinc-700 hover:bg-zinc-600 rounded'
                    >
                      Отмена
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <p className={`text-sm break-words ${expanded ? '' : 'line-clamp-4'}`}>{post.text}</p>
                  {post.text.length > 200 && (
                    <button
                      onClick={() => setExpanded(!expanded)}
                      className='text-xs text-zinc-500 hover:text-zinc-400'
                    >
                      {expanded ? 'Скрыть' : 'Читать дальше'}
                    </button>
                  )}
                </>
              )}
            </div>
          )}
        </div>
      </div>
      {hasMedia && (
        <div className='relative rounded-xl m-3 aspect-[3/4] overflow-hidden bg-gradient-to-br from-zinc-900 via-zinc-700 to-zinc-900'>
          {/* Медиа */}
          {currentContent?.type === 'video' ? (
            <video
              key={currentContent.id}
              className='w-full h-full object-contain'
              controls
              src={`/api/v1/content/${currentContent.id}/stream`}
            />
          ) : (
            <img className='w-full h-full object-contain' src={thumbnailUrl} alt={`content-${currentContent?.id}`} />
          )}

          {/* Навигация */}
          {contents.length > 1 && (
            <>
              <button
                onClick={prevSlide}
                className='absolute left-2 top-1/2 -translate-y-1/2 bg-black/30 hover:bg-black/70 p-2 rounded-full transition'
              >
                <ChevronLeft className='w-6 h-6 text-white' />
              </button>
              <button
                onClick={nextSlide}
                className='absolute right-2 top-1/2 -translate-y-1/2 bg-black/30 hover:bg-black/70 p-2 rounded-full transition'
              >
                <ChevronRight className='w-6 h-6 text-white' />
              </button>

              {/* Индикаторы */}
              <div className='absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-1.5'>
                {contents.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrentIndex(i)}
                    className={`w-2 h-2 rounded-full transition ${
                      i === currentIndex ? 'bg-white' : 'bg-white/50 hover:bg-white/75'
                    }`}
                  />
                ))}
              </div>
            </>
          )}
        </div>
      )}
      <div className='flex justify-between items-center my-3 px-4'>
        <div className='flex items-center gap-3'>
          <button
            onClick={handleLike}
            className={`flex items-center gap-1 text-sm ${liked ? 'text-red-500' : 'text-zinc-500 hover:text-red-500'}`}
          >
            <Heart className='w-5 h-5' fill={liked ? 'currentColor' : 'none'} />
            {likesCount}
          </button>
          <button
            onClick={() => setCommentsOpen(!commentsOpen)}
            className='flex items-center gap-1 text-sm text-zinc-500 hover:text-blue-500'
          >
            <MessageSquare className='w-5 h-5' />
            {commentsCount}
          </button>
        </div>
        {isOwner && (
          <div className='flex items-center gap-2'>
            <button
              onClick={handleEdit}
              className='p-1.5 text-zinc-500 hover:text-blue-500 transition'
              title='Редактировать'
            >
              <Edit className='w-4 h-4' />
            </button>
            <button
              onClick={handleDelete}
              className='p-1.5 text-zinc-500 hover:text-red-500 transition'
              title='Удалить'
            >
              <Trash2 className='w-4 h-4' />
            </button>
          </div>
        )}
      </div>
      {commentsOpen && (
        <div className='mt-3 px-3 pb-3 space-y-3'>
          {/* Форма добавления комментария */}
          {user && (
            <div className='flex gap-2'>
              <input
                type='text'
                value={newCommentText}
                onChange={(e) => setNewCommentText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleAddComment()
                  }
                }}
                placeholder='Добавить комментарий...'
                className='flex-1 px-3 py-2 text-sm bg-zinc-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
              />
              <button
                onClick={handleAddComment}
                disabled={!newCommentText.trim()}
                className='px-3 py-2 text-sm bg-blue-600 hover:bg-blue-700 disabled:bg-zinc-700 disabled:text-zinc-500 rounded-lg transition'
              >
                <Send className='w-4 h-4' />
              </button>
            </div>
          )}

          {/* Список комментариев */}
          <div className='space-y-2'>
            {comments.map((comment) => (
              <CommentItem
                key={comment.id}
                comment={comment}
                currentUserId={user?.id}
                isPostOwner={isOwner}
                onDelete={handleDeleteComment}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// Компонент для отображения одного комментария
type CommentItemProps = {
  comment: Comment
  currentUserId?: number
  isPostOwner: boolean
  onDelete: (commentId: number) => void
}

const CommentItem = ({ comment, currentUserId, isPostOwner, onDelete }: CommentItemProps) => {
  const [expanded, setExpanded] = useState(false)
  const isCommentOwner = currentUserId === comment.user_id
  const canDelete = isCommentOwner || isPostOwner
  const needsExpansion = comment.text.length > 200

  return (
    <div className='flex justify-between items-start gap-2 p-2 rounded-lg bg-zinc-800/50'>
      <div className='flex-1 min-w-0'>
        <p className='text-sm text-zinc-400 mb-1'>{comment.user_name}</p>
        <p className={`text-sm break-words ${expanded ? '' : 'line-clamp-3'}`}>{comment.text}</p>
        {needsExpansion && (
          <button onClick={() => setExpanded(!expanded)} className='text-xs text-zinc-500 hover:text-zinc-400 mt-1'>
            {expanded ? 'Скрыть' : 'Читать дальше'}
          </button>
        )}
      </div>
      {canDelete && (
        <button
          onClick={() => onDelete(comment.id)}
          className='p-1 text-zinc-500 hover:text-red-500 transition flex-shrink-0'
          title='Удалить'
        >
          <Trash2 className='w-4 h-4' />
        </button>
      )}
    </div>
  )
}

export default PostBlock
