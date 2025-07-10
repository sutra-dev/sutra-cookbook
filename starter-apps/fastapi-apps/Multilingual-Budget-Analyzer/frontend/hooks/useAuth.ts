import { useState, useEffect } from 'react'

interface User {
  id: string
  email: string
  preferred_language: string
  currency: string
  created_at: string
}

interface LoginData {
  email: string
  password: string
}

interface RegisterData extends LoginData {
  preferred_language?: string
  currency?: string
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for stored token on mount
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
      fetchUser(storedToken)
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async (authToken: string) => {
    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${authToken}`,
        },
      })
      
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      } else {
        // Token is invalid
        localStorage.removeItem('token')
        setToken(null)
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
      localStorage.removeItem('token')
      setToken(null)
    } finally {
      setLoading(false)
    }
  }

  const login = async (data: LoginData) => {
    try {
      const formData = new URLSearchParams()
      formData.append('username', data.email)
      formData.append('password', data.password)

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      })

      if (response.ok) {
        const { access_token } = await response.json()
        setToken(access_token)
        localStorage.setItem('token', access_token)
        await fetchUser(access_token)
        return { success: true }
      } else {
        const errorData = await response.json()
        return { success: false, error: errorData.detail || 'Login failed' }
      }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, error: 'Network error' }
    }
  }

  const register = async (data: RegisterData) => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      if (response.ok) {
        // Auto-login after successful registration
        return await login({ email: data.email, password: data.password })
      } else {
        const errorData = await response.json()
        return { success: false, error: errorData.detail || 'Registration failed' }
      }
    } catch (error) {
      console.error('Registration error:', error)
      return { success: false, error: 'Network error' }
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    loading,
    login,
    register,
    logout,
  }
} 