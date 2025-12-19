import { postsResponseSchema, type GetPostsOptions } from './types'

const BASE_URL = '/api/v1'

export const getPosts = async (options?: GetPostsOptions) => {
  const { page, per_page, author_id, user_id } = options ?? {}
  const queryParams = new URLSearchParams()
  if (page) queryParams.append('page', String(page))
  if (per_page) queryParams.append('per_page', String(per_page))
  if (author_id) queryParams.append('author_id', String(author_id))
  if (user_id) queryParams.append('user_id', String(user_id))

  const queryString = queryParams.toString()
  const response = await fetch(`${BASE_URL}/posts/${queryString ? `?${queryString}` : ''}`)
  const data = await response.json()

  return postsResponseSchema.parse(data)
}

// DELETE --> /rest/user/${id}
// POST --> /rest/users (name & email in body)
// GET --> /rest/users
