import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import LoginForm from '@/components/auth/LoginForm'
import { useRouter } from 'next/navigation'

// Mock toast
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
  }
}))

describe('LoginForm', () => {
  const mockPush = jest.fn()

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({
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

  it('shows validation error for invalid email', async () => {
    render(<LoginForm />)
    const emailInput = screen.getByLabelText(/email address/i)
    const submitBtn = screen.getByRole('button', { name: /sign in/i })

    // Type invalid email
    await userEvent.type(emailInput, 'invalid-email')
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(screen.getByText(/invalid email address/i)).toBeInTheDocument()
    })
  })

  it('handles successful login', async () => {
    render(<LoginForm />)
    const emailInput = screen.getByLabelText(/email address/i)
    const passwordInput = screen.getByLabelText(/password/i)
    const submitBtn = screen.getByRole('button', { name: /sign in/i })

    await userEvent.type(emailInput, 'user@example.com')
    await userEvent.type(passwordInput, 'Password123')
    
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(localStorage.getItem('access_token')).toBe('fake-access-token')
      expect(mockPush).toHaveBeenCalledWith('/dashboard')
    })
  })

  it('handles login failure', async () => {
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
