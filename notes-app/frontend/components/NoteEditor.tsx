'use client'
import { useEffect, useRef } from 'react'

export default function NoteEditor({ value, onChange }:{ value:string, onChange:(html:string)=>void }){
  const ref = useRef<HTMLDivElement>(null)

  useEffect(()=>{
    if(ref.current && ref.current.innerHTML !== value){
      ref.current.innerHTML = value || ''
    }
  }, [value])

  return (
    <div
      ref={ref}
      className="textarea prose max-w-none"
      contentEditable
      onInput={(e)=> onChange((e.target as HTMLDivElement).innerHTML)}
      suppressContentEditableWarning
      style={{minHeight: 200}}
    />
  )
}