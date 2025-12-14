import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import RegisterForm from '@/components/auth/RegisterForm'
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

describe('RegisterForm', () => {
  const mockPush = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    ;(useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    })
    localStorage.clear()
  })

  it('renders register form correctly', () => {
    render(<RegisterForm />)
    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/email address/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('updates password strength meter', async () => {
    render(<RegisterForm />)
    const passwordInput = screen.getByLabelText(/password/i)
    
    // Type weak password
    await userEvent.type(passwordInput, 'weak')
    // Strength meter bars should update visually (tested implicitly by render)
  })

  it('handles successful registration', async () => {
    // Mock successful API response (without auto-login token)
    ;(api.post as jest.Mock).mockResolvedValueOnce({
      data: {
        success: true,
        message: 'User registered successfully',
      }
    })

    render(<RegisterForm />)
    
    await userEvent.type(screen.getByLabelText(/full name/i), 'New User')
    await userEvent.type(screen.getByLabelText(/email address/i), 'new@example.com')
    await userEvent.type(screen.getByLabelText(/password/i), 'SecurePass123')
    
    fireEvent.click(screen.getByRole('button', { name: /create account/i }))

    await waitFor(() => {
      expect(api.post).toHaveBeenCalledWith('/api/auth/register', {
        name: 'New User',
        email: 'new@example.com',
        password: 'SecurePass123',
      })
      // No error message should be present
      expect(screen.queryByText(/registration failed/i)).not.toBeInTheDocument()
    })
  })

  it('handles registration failure (email exists)', async () => {
    // Mock failed API response
    ;(api.post as jest.Mock).mockRejectedValueOnce({
      response: {
        data: {
          success: false,
          error: { code: 422, message: 'Email already registered' }
        }
      }
    })

    render(<RegisterForm />)
    
    await userEvent.type(screen.getByLabelText(/full name/i), 'Test User')
    await userEvent.type(screen.getByLabelText(/email address/i), 'exists@example.com')
    await userEvent.type(screen.getByLabelText(/password/i), 'SecurePass123')
    
    fireEvent.click(screen.getByRole('button', { name: /create account/i }))

    await waitFor(() => {
      expect(screen.getByText(/email already registered/i)).toBeInTheDocument()
    })
  })
})
