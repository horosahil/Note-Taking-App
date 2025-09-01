'use client'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import Link from 'next/link'
import { motion } from 'framer-motion'

type Note = {
  note_id: string
  note_title: string
  note_content: string
  created_on: string
  last_update: string
}

export default function HomePage() {
  const qc = useQueryClient()
  const { data, isLoading, error } = useQuery<Note[]>({
    queryKey: ['notes'],
    queryFn: async () => {
      const res = await api.get('/api/notes/',
        { withCredentials: true }
      )
      return res.data
    }
  })

  const del = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/api/notes/${id}`, { withCredentials: true })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['notes'] })
  })

  if (isLoading) return <div>Loading...</div>
  if (error) return <div className="text-red-600">Error loading notes</div>

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-semibold">Your Notes</h1>
        <Link className="btn" href="/notes/new">New Note</Link>
      </div>
      {(!data || data.length === 0) && <div className="card">No notes yet.</div>}
      <div className="grid gap-4">
        {data?.map(n => (
          <motion.div key={n.note_id} className="card" initial={{opacity:0, y:10}} animate={{opacity:1, y:0}}>
            <div className="flex justify-between items-start">
              <div>
                <Link href={`/notes/${n.note_id}`} className="text-lg font-medium hover:underline">{n.note_title}</Link>
                <p className="text-sm text-gray-600 line-clamp-2" dangerouslySetInnerHTML={{__html: n.note_content}} />
              </div>
              <button className="btn" onClick={() => del.mutate(n.note_id)}>Delete</button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}