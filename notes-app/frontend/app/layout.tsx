import type { Metadata } from 'next'
import './globals.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactNode, useState } from 'react'

export const metadata: Metadata = {
  title: 'Notes App',
  description: 'Simple notes app with auth and CRUD',
  keywords: ['notes','nextjs','fastapi','mongodb'],
  openGraph: {
    title: 'Notes App',
    description: 'Simple notes app with auth and CRUD',
    url: 'http://localhost:3000',
    type: 'website'
  }
}

export default function RootLayout({ children }: { children: ReactNode }) {
  const [client] = useState(new QueryClient())
  return (
    <html lang="en">
      <body>
        <QueryClientProvider client={client}>
          <div className="container py-6">
            <header className="flex items-center justify-between mb-6">
              <a href="/" className="text-2xl font-bold">Notes</a>
              <nav className="flex gap-3">
                <a className="btn" href="/signin">Sign In</a>
                <a className="btn" href="/signup">Sign Up</a>
              </nav>
            </header>
            {children}
          </div>
        </QueryClientProvider>
      </body>
    </html>
  )
}