import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'

type Subscription = {
  id: number
  author_id: number
  started_at: string
  expires_at: string | null
  renewable: boolean
}

type UserRead = {
  id: number
  name: string
  email: string
  subscriptions: Array<Subscription>
  is_author: boolean
}

type AuthContextType = {
  user: UserRead | null
  loading: boolean
  refreshUser: () => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserRead | null>(null)
  const [loading, setLoading] = useState(true)

  const refreshUser = async () => {
    try {
      const res = await fetch('/api/v1/auth/me', { credentials: 'include' })
      if (res.ok) {
        const data = await res.json()
        console.log('Обновление пользователя из API:', data)
        console.log('Подписки:', data.subscriptions)
        setUser(data)
      } else {
        setUser(null)
      }
    } catch {
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    await fetch('/api/v1/auth/logout', { credentials: 'include' })
    setUser(null)
  }

  useEffect(() => {
    refreshUser()
  }, [])

  return <AuthContext.Provider value={{ user, loading, refreshUser, logout }}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
