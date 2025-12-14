import { render, screen, waitFor } from '@testing-library/react'
import Dashboard from '@/app/dashboard/page'
import { useRouter } from 'next/navigation'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { jwtDecode } from 'jwt-decode'

// Mock jwt-decode
jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn()
}))

// Mock axios
jest.mock('@/lib/axios', () => ({
  __esModule: true,
  default: {
    get: jest.fn(),
  },
}))

import api from '@/lib/axios'

// Mock router
const mockPush = jest.fn()
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}))

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe('Dashboard', () => {
  beforeEach(() => {
    mockPush.mockClear()
    localStorage.clear()
    jest.clearAllMocks()
  })

  it('redirects to auth if no token present', () => {
    const Wrapper = createWrapper()
    render(<Dashboard />, { wrapper: Wrapper })
    expect(mockPush).toHaveBeenCalledWith('/auth')
  })

  it('renders user name after fetching', async () => {
    // Setup valid token
    localStorage.setItem('access_token', 'valid-token')
    ;(jwtDecode as jest.Mock).mockReturnValue({ sub: 'user-123' })
    
    // Mock API response
    ;(api.get as jest.Mock).mockResolvedValueOnce({
      data: {
        id: 'user-123',
        name: 'Test User',
        email: 'user@example.com'
      }
    })

    const Wrapper = createWrapper()
    render(<Dashboard />, { wrapper: Wrapper })

    // Wait for "Welcome back, Test User" (from API mock)
    await waitFor(() => {
      expect(screen.getByText(/Test User/i)).toBeInTheDocument()
    })
  })

  it('handles invalid token by redirecting', async () => {
    // Suppress expected console.error for this test
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})
    
    localStorage.setItem('access_token', 'invalid-token')
    ;(jwtDecode as jest.Mock).mockImplementation(() => {
      throw new Error('Invalid token')
    })

    const Wrapper = createWrapper()
    render(<Dashboard />, { wrapper: Wrapper })

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/auth')
    })
    
    consoleSpy.mockRestore()
  })
})
