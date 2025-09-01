'use client'
import { useState } from 'react'
import { api } from '@/lib/api'
import { useRouter } from 'next/navigation'

export default function SignInPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState<string | null>(null)
  const router = useRouter()

  const submit = async (e: any) => {
    e.preventDefault()
    setErr(null)
    try {
      await api.post('/api/auth/login', { user_email: email, password }, { withCredentials: true })
      router.push('/')
    } catch (e:any) {
      setErr(e?.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="card max-w-md mx-auto">
      <h1 className="text-xl font-semibold mb-4">Sign In</h1>
      <form onSubmit={submit} className="space-y-3">
        <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="input" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        {err && <div className="text-sm text-red-600">{err}</div>}
        <button className="btn w-full" type="submit">Sign In</button>
      </form>
    </div>
  )
}