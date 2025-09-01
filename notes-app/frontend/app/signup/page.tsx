'use client'
import { useState } from 'react'
import { api } from '@/lib/api'
import { useRouter } from 'next/navigation'

export default function SignUpPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState<string | null>(null)
  const router = useRouter()

  const submit = async (e: any) => {
    e.preventDefault()
    setErr(null)
    try {
      await api.post('/api/auth/register', { user_name: name, user_email: email, password })
      // auto-login
      await api.post('/api/auth/login', { user_email: email, password }, { withCredentials: true })
      router.push('/')
    } catch (e:any) {
      setErr(e?.response?.data?.detail || 'Sign up failed')
    }
  }

  return (
    <div className="card max-w-md mx-auto">
      <h1 className="text-xl font-semibold mb-4">Sign Up</h1>
      <form onSubmit={submit} className="space-y-3">
        <input className="input" placeholder="Your name" value={name} onChange={e=>setName(e.target.value)} />
        <input className="input" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="input" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        {err && <div className="text-sm text-red-600">{err}</div>}
        <button className="btn w-full" type="submit">Create Account</button>
      </form>
    </div>
  )
}