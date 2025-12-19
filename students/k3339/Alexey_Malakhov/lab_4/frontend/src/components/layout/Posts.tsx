import PostBlock from '@/components/blocks/PostBlock'
import { useEffect, useMemo, useRef } from 'react'
import { Skeleton } from '../ui/skeleton'
import { useInfiniteQuery } from '@tanstack/react-query'
import { Spinner } from '@/components/ui/shadcn-io/spinner'
import createPostsInfiniteQueryOptions from '@/api/createPostsInfiniteQueryOptions'
import type { Post } from '@/api/types'

type Props = {
  activeAuthor?: number | null
}

const Posts = ({ activeAuthor }: Props) => {
  const loadMoreRef = useRef<HTMLDivElement>(null)
  const authorFilter = activeAuthor ?? undefined

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isLoading } = useInfiniteQuery(
    createPostsInfiniteQueryOptions({
      author_id: authorFilter,
      per_page: 8,
    })
  )

  const posts = useMemo<Post[] | undefined>(() => data?.pages.flatMap((p) => p.posts), [data])

  useEffect(() => {
    const target = loadMoreRef.current
    if (!target) return

    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries
        if (entry.isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage()
        }
      },
      {
        root: null,
        rootMargin: '800px 0px 800px 0px',
        threshold: 0.01,
      }
    )

    observer.observe(target)
    return () => observer.disconnect()
  }, [hasNextPage, isFetchingNextPage, fetchNextPage])

  return (
    <>
      <div className='grid grid-cols-1 md:grid-cols-1 lg:grid-cols-1 md:w-1/3 md:gap-2 md:p-2 mt-2 md:mt-0'>
        {!isLoading &&
          posts?.map((post) => {
            return <PostBlock post={post} key={post.id} />
          })}
        {/* sentinel внизу страницы */}
        <div ref={loadMoreRef} aria-hidden />
        {/*
        {isLoading &&
          Array.from({ length: 12 }).map((_, i) => (
            <a key={i}>
              <div>
                <Skeleton className='w-full h-full aspect-[16/9] rounded-2xl' />
                <div className='flex flex-row p-3 h-22.5'>
                  <Skeleton className='w-10 h-10 mr-3 rounded-full'></Skeleton>
                  <div className='flex flex-col min-w-0'>
                    <Skeleton className='h-2 w-18 mt-1'></Skeleton>
                    <Skeleton className='h-2 w-40 mt-3'></Skeleton>
                    <Skeleton className='h-2 w-16 mt-3.5'></Skeleton>
                  </div>
                </div>
              </div>
            </a>
          ))}
        */}
      </div>
      {/* 
      {posts && posts.length < 12 && isLoading && (
        <div className='flex justify-center items-center py-10'>
          <Spinner />
        </div>
      )}
      */}
      {/* {posts && posts.length < 12 && !hasNextPage && (
        <div className='flex justify-center items-center py-10 text-zinc-500'>...</div>
      )} */}
    </>
  )
}

export default Posts
