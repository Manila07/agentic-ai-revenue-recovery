import { useEffect, useState } from 'react'
import api from '../services/api'

export function useRecovery() {
  const [recoveryData, setRecoveryData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/recovery/analyze/')
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return { recoveryData, loading }
}