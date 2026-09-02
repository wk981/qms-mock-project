import { useState } from 'react'
import { greet } from './api'
import './App.css'

function App() {
  const [name, setName] = useState('')
  const [greeting, setGreeting] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setGreeting(null)
    setLoading(true)

    try {
      const response = await greet(name)
      setGreeting(response.greeting)
      setName('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Greeting App</h1>

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your name"
          className="input"
          disabled={loading}
        />
        <button type="submit" disabled={loading} className="button">
          {loading ? 'Loading...' : 'Get Greeting'}
        </button>
      </form>

      {greeting && (
        <div className="result success">
          <p>{greeting}</p>
        </div>
      )}

      {error && (
        <div className="result error">
          <p>Error: {error}</p>
        </div>
      )}
    </div>
  )
}

export default App
