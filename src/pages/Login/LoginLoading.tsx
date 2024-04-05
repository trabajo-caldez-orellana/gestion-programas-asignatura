import React, { useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import queryString from 'query-string'
import useAuth from '../../hooks/useAuth'
import { client } from '../../utils/axiosClient'
import { Spinner } from '../../components'

const LoginLoading: React.FC = () => {
  const location = useLocation()
  const { getAuthUser } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    const values = queryString.parse(location.search)
    const code = values.code ? values.code : null

    if (code) {
      onGooglelogin()
    }
  }, [])

  const googleLoginHandler = (code: string) => {
    return client
      .get(`auth/login/google/${code}`)
      .then((res) => {
        getAuthUser()
        navigate('/')
        return true
      })
      .catch(() => {
        navigate('/')
      })
  }

  const onGooglelogin = async () => {
    await googleLoginHandler(location.search)
  }

  return <Spinner />
}

export default LoginLoading
