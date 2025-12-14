import { http, HttpResponse } from 'msw'

export const handlers = [
  // LOGIN - matches both http://localhost:5000/api/auth/login and relative paths
  http.post('*/api/auth/login', async ({ request }) => {
    const { email, password } = await request.json() as any

    if (email === 'user@example.com' && password === 'Password123') {
      return HttpResponse.json({
        success: true,
        message: 'Login successful',
        access_token: 'fake-access-token',
        refresh_token: 'fake-refresh-token',
      })
    }
    
    return HttpResponse.json({
      success: false, 
      error: { code: 401, message: 'Invalid credentials' }
    }, { status: 401 })
  }),

  // REGISTER
  http.post('*/api/auth/register', async ({ request }) => {
    const { email } = await request.json() as any

    if (email === 'exists@example.com') {
      return HttpResponse.json({
         success: false,
         error: { code: 422, message: 'Email already registered' }
      }, { status: 422 })
    }

    return HttpResponse.json({
      success: true,
      message: 'User registered successfully',
    }, { status: 201 })
  }),

  // USER PROFILE
  http.get('*/api/users/:id', () => {
    return HttpResponse.json({
      id: 'user-123',
      name: 'Test User',
      email: 'user@example.com'
    })
  }),
]
