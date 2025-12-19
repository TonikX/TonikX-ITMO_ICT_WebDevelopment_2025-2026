import { z } from 'zod'

export const authorSchema = z.object({
  id: z.number(),
  name: z.string(),
  handle: z.string(),
  bio: z.string().nullable().optional(),
  is_verified: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
  user_id: z.number(),
})

export const contentSchema = z.object({
  id: z.number(),
  type: z.enum(['photo', 'video']),
  author_id: z.number().nullable().optional(),
  duration: z.number().nullable().optional(),
  width: z.number().nullable().optional(),
  height: z.number().nullable().optional(),
  created_at: z.string(),
  updated_at: z.string(),
})

export const commentSchema = z.object({
  id: z.number(),
  text: z.string(),
  user_id: z.number(),
  user_name: z.string(),
  post_id: z.number(),
  created_at: z.string(),
})

export const postSchema = z.object({
  id: z.number(),
  text: z.string().nullable().optional(),
  author: authorSchema,
  created_at: z.string(),
  updated_at: z.string(),
  contents: z.array(contentSchema),
  likes_count: z.number(),
  comments_count: z.number(),
  is_liked: z.boolean(),
})

export const postsResponseSchema = z.object({
  posts: z.array(postSchema),
  pagination: z.object({
    totalPages: z.number(),
    totalItems: z.number(),
    hasMore: z.boolean(),
    currentPage: z.number(),
  }),
})

export const GetPostsParamsSchema = z.object({
  page: z.number().optional(),
  per_page: z.number().optional(),
  author_id: z.number().optional(),
  user_id: z.number().optional(),
})

export type GetPostsOptions = z.infer<typeof GetPostsParamsSchema>
export type Post = z.infer<typeof postSchema>
export type Content = z.infer<typeof contentSchema>
export type Author = z.infer<typeof authorSchema>
export type PostsResponse = z.infer<typeof postsResponseSchema>
export type Comment = z.infer<typeof commentSchema>
