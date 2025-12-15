import '@testing-library/jest-dom'
import 'whatwg-fetch'
import { server } from './src/mocks/server'

// MSW Setup
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(() => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
    back: jest.fn(),
  })),
  usePathname: jest.fn(),
  useSearchParams: jest.fn(() => ({ get: jest.fn() })),
}))

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}))

// Mock Framer Motion
jest.mock('framer-motion', () => ({
  ...jest.requireActual('framer-motion'),
  motion: {
    div: require('react').forwardRef(({ children, ...props }: any, ref: any) => {
      return require('react').createElement('div', { ref, ...props }, children)
    }),
    span: require('react').forwardRef(({ children, ...props }: any, ref: any) => {
      return require('react').createElement('span', { ref, ...props }, children)
    }),
  },
  AnimatePresence: ({ children }: any) => require('react').createElement(require('react').Fragment, null, children),
}))
