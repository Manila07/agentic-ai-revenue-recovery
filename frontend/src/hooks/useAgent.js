import { useEffect, useState } from 'react'
import api from '../services/api'

export function useAgent() {
  const [actions, setActions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/agent/activity')
      .then(res => setActions(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return { actions, loading }
}