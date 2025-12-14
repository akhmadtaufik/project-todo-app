import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import LoginForm from '@/components/auth/LoginForm'
import { useRouter } from 'next/navigation'

// Mock axios
jest.mock('@/lib/axios', () => ({
  __esModule: true,
  default: {
    post: jest.fn(),
  },
}))

// Mock toast
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
  }
}))

import api from '@/lib/axios'

describe('LoginForm', () => {
  const mockPush = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    ;(useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    })
    localStorage.clear()
  })

  it('renders login form correctly', () => {
    render(<LoginForm />)
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
  })

  it('prevents submission with invalid email', async () => {
    render(<LoginForm />)
    const emailInput = screen.getByLabelText(/email address/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitBtn = screen.getByRole('button', { name: /sign in/i })

    // Type invalid email and valid password
    await userEvent.type(emailInput, 'invalid-email')
    await userEvent.type(passwordInput, 'somepassword')
    
    // Submit form
    await userEvent.click(submitBtn)

    // API should NOT be called because validation fails
    await waitFor(() => {
      expect(api.post).not.toHaveBeenCalled()
    }, { timeout: 1000 })
  })

  it('handles successful login', async () => {
    // Mock successful API response
    ;(api.post as jest.Mock).mockResolvedValueOnce({
      data: {
        success: true,
        message: 'Login successful',
        access_token: 'fake-access-token',
        refresh_token: 'fake-refresh-token',
      }
    })

    render(<LoginForm />)
    const emailInput = screen.getByLabelText(/email address/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitBtn = screen.getByRole('button', { name: /sign in/i })

    await userEvent.type(emailInput, 'user@example.com')
    await userEvent.type(passwordInput, 'Password123')
    
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/api/auth/login', {
        email: 'user@example.com',
        password: 'Password123',
      })
      expect(localStorage.getItem('access_token')).toBe('fake-access-token')
      expect(mockPush).toHaveBeenCalledWith('/dashboard')
    })
  })

  it('handles login failure', async () => {
    // Mock failed API response
    ;(api.post as jest.Mock).mockRejectedValueOnce({
      response: {
        data: {
          success: false,
          error: { code: 401, message: 'Invalid credentials' }
        }
      }
    })

    render(<LoginForm />)
    const emailInput = screen.getByLabelText(/email address/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitBtn = screen.getByRole('button', { name: /sign in/i })

    await userEvent.type(emailInput, 'wrong@example.com')
    await userEvent.type(passwordInput, 'wrongpass')
    
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })
})
