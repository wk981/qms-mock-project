const API_BASE_URL = 'http://localhost:8000'

export interface GreetRequest {
  name: string
}

export interface GreetResponse {
  greeting: string
}

export async function greet(name: string): Promise<GreetResponse> {
  const response = await fetch(`${API_BASE_URL}/api/greet`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name } as GreetRequest),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to get greeting')
  }

  return response.json()
}
