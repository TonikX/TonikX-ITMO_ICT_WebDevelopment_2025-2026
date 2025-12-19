import { queryOptions } from '@tanstack/react-query'
import { getPosts } from './api'
import type { GetPostsOptions, Post } from './types'

export default function createPostsQueryOptions(opts?: GetPostsOptions) {
  return queryOptions<Post[]>({
    queryKey: ['posts', opts],
    queryFn: async () => {
      const data = await getPosts(opts)
      return data.posts
    },
  })
}
