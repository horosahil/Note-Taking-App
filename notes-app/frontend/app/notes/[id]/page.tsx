'use client'
import { useParams, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import NoteEditor from '@/components/NoteEditor'

export default function NotePage(){
  const { id } = useParams<{id:string}>()
  const router = useRouter()
  const isNew = id === 'new'
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [err, setErr] = useState<string | null>(null)

  useEffect(()=>{
    const load = async () => {
      if(!isNew){
        try {
          const res = await api.get(`/api/notes/${id}`, { withCredentials: true })
          setTitle(res.data.note_title)
          setContent(res.data.note_content)
        } catch (e:any) {
          setErr(e?.response?.data?.detail || 'Failed to load note')
        }
      }
    }
    load()
  }, [id, isNew])

  const save = async () => {
    setErr(null)
    try {
      if(isNew){
        await api.post('/api/notes/', { note_title: title, note_content: content }, { withCredentials: true })
      } else {
        await api.put(`/api/notes/${id}`, { note_title: title, note_content: content }, { withCredentials: true })
      }
      router.push('/')
    } catch (e:any) {
      setErr(e?.response?.data?.detail || 'Save failed')
    }
  }

  return (
    <div className="card">
      <div className="space-y-3">
        <input className="input" placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} />
        <NoteEditor value={content} onChange={setContent} />
        {err && <div className="text-sm text-red-600">{err}</div>}
        <div className="flex gap-2">
          <button className="btn" onClick={save}>{isNew ? 'Create' : 'Save'}</button>
          <button className="btn" onClick={()=>router.push('/')}>Cancel</button>
        </div>
      </div>
    </div>
  )
}