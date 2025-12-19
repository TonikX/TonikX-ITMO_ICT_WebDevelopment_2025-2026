import { infiniteQueryOptions } from '@tanstack/react-query'
import { getPosts } from './api'
import type { GetPostsOptions } from './types'

export default function createPostsInfiniteQueryOptions(opts?: GetPostsOptions) {
  return infiniteQueryOptions({
    queryKey: ['posts', opts],
    queryFn: ({ pageParam = 1 }) =>
      getPosts({ page: pageParam, per_page: opts?.per_page ?? 8, author_id: opts?.author_id, user_id: opts?.user_id }),
    initialPageParam: 1,
    getNextPageParam: (lastPage: any) =>
      lastPage?.pagination?.hasMore ? lastPage.pagination.currentPage + 1 : undefined,
  })
}
