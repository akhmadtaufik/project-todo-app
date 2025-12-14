import { render, screen, waitFor } from '@testing-library/react'
import Dashboard from '@/app/dashboard/page'
import { useRouter } from 'next/navigation'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { jwtDecode } from 'jwt-decode'

// Mock jwt-decode
jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn()
}))

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

    const Wrapper = createWrapper()
    render(<Dashboard />, { wrapper: Wrapper })

    // Should show loading initially
    // expect(screen.getByRole('status')).toBeInTheDocument() // Loader has no role by default unless added

    // Wait for "Welcome back, Test User" (from MSW handler)
    await waitFor(() => {
      expect(screen.getByText(/Test User/i)).toBeInTheDocument()
    })
  })

  it('handles invalid token by redirecting', async () => {
    localStorage.setItem('access_token', 'invalid-token')
    ;(jwtDecode as jest.Mock).mockImplementation(() => {
      throw new Error('Invalid token')
    })

    const Wrapper = createWrapper()
    render(<Dashboard />, { wrapper: Wrapper })

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/auth')
    })
  })
})
