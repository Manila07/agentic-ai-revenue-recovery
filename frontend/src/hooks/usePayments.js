import { useEffect, useState } from 'react'
import api from '../services/api'

export function usePayments() {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/payments')
      .then(res => setPayments(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  return { payments, loading }
}