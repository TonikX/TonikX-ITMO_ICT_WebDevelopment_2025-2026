import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ImagePlus, X } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

const PostCreation = () => {
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const [text, setText] = useState('')
  const [files, setFiles] = useState<File[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isFreePost, setIsFreePost] = useState(false)

  const createPostMutation = useMutation({
    mutationFn: async (formData: FormData) => {
      console.log('Creating post with formData:', {
        text: formData.get('text'),
        is_free_post: formData.get('is_free_post'),
        files: formData.getAll('files'),
      })

      const response = await fetch('/api/v1/posts/', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      })

      console.log('Response status:', response.status)

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        console.error('Error creating post:', data)
        throw new Error(data.detail || 'Не удалось создать пост')
      }

      const result = await response.json()
      console.log('Post created successfully:', result)
      return result
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] })
      setText('')
      setFiles([])
      setIsFreePost(false)
      setError(null)
    },
    onError: (err: Error) => {
      setError(err.message)
    },
  })

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || [])
    if (files.length + selectedFiles.length > 10) {
      setError('Максимум 10 файлов')
      return
    }
    setFiles((prev) => [...prev, ...selectedFiles])
    setError(null)
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim()) {
      setError('Текст обязателен')
      return
    }

    const formData = new FormData()
    formData.append('text', text)
    formData.append('is_free_post', isFreePost ? 'true' : 'false')
    files.forEach((file) => {
      formData.append('files', file)
    })

    createPostMutation.mutate(formData)
  }

  // Показываем форму только если пользователь является автором
  // и либо не выбран конкретный автор, либо это его собственная страница
  if (!user || !user.is_author) {
    return null
  }

  return (
    <Card className='mb-3 py-0 md:w-2/5 outline-1 outline-zinc-800 mx-1 rounded-2xl w-full overflow-hidden'>
      <CardContent className='p-3 bg-black'>
        <form onSubmit={handleSubmit} className='space-y-3'>
          <Textarea
            placeholder='Что вы хотите опубликовать?'
            value={text}
            onChange={(e) => setText(e.target.value)}
            className='min-h-[120px] resize-none bg-zinc-800 text-white placeholder-zinc-500 '
          />

          {files.length > 0 && (
            <div className='grid grid-cols-3 gap-2'>
              {files.map((file, index) => (
                <div key={index} className='relative group'>
                  <img
                    src={URL.createObjectURL(file)}
                    alt={`Предпросмотр ${index}`}
                    className='w-full h-24 object-cover rounded bg-zinc-700'
                  />
                  <Button
                    type='button'
                    variant='destructive'
                    size='icon'
                    className='absolute top-1 right-1 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity bg-zinc-800 text-white'
                    onClick={() => removeFile(index)}
                  >
                    <X className='h-4 w-4' />
                  </Button>
                </div>
              ))}
            </div>
          )}

          {error && (
            <Alert variant='destructive' className='bg-zinc-800 text-red-500'>
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className='flex items-center gap-2'>
            <Button
              type='button'
              variant='outline'
              size='sm'
              className='relative text-zinc-500 hover:text-zinc-300 bg-zinc-800'
            >
              <ImagePlus className='h-4 w-4 mr-2' />
              Добавить медиа
              <input
                type='file'
                multiple
                accept='image/*,video/mp4'
                onChange={handleFileChange}
                className='absolute inset-0 opacity-0 cursor-pointer'
              />
            </Button>
            <span className='text-sm text-zinc-500'>{files.length}/10 файлов</span>
            <Button
              type='submit'
              disabled={createPostMutation.isPending}
              className='ml-auto bg-zinc-900 hover:bg-zinc-800 text-white'
            >
              {createPostMutation.isPending ? 'Публикую...' : 'Опубликовать'}
            </Button>
          </div>

          {/* Чекбокс бесплатного поста */}
          <div className='flex items-center gap-2'>
            <input
              type='checkbox'
              id='freePost'
              checked={isFreePost}
              onChange={(e) => setIsFreePost(e.target.checked)}
              className='cursor-pointer bg-zinc-800 text-white'
            />
            <label htmlFor='freePost' className='text-sm text-zinc-500'>
              Бесплатный пост
            </label>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export default PostCreation
