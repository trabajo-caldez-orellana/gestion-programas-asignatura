import axios from 'axios'
import { camelizeKeys } from 'humps'
import { OAuthCredential, OAuthUrl, Profile } from './types'
import { BASE_URL, GOOGLE_REDIRECT_URL } from '../helpers/env-variables'

export type { OAuthCredential, OAuthUrl }

export const TOKEN_KEY = 'token'

// TODO. Modificar esto. Agregar BASE_URL como una variable de entorno
// Y leerla en un archivo constant en helpers.

export const client = axios.create({
  baseURL: BASE_URL
})

// TODO. cambiar esto una vez me funcione bien a como me parezca mejor
client.interceptors.response.use((response) => {
  if (response.data) {
    response.data = camelizeKeys(response.data)
  }

  return response
})

client.interceptors.request.use((config) => {
  // TODO: Conviene localstorage o usar cookies?
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) {
    config.headers['Authorization'] = `Token ${token}`
  }

  return config
})

export const getGoogleAuthLink = async () => {
  const response = await client.get<OAuthUrl>('/auth/o/google-oauth2/', {
    params: {
      redirect_uri: GOOGLE_REDIRECT_URL
    }
  })
  return response.data
}

export const getGoogleAuthToken = async (credential: OAuthCredential) => {
  const response = await client.post('/auth/o/google-oauth2/', credential, {
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    withCredentials: true
  })
  return response.data
}

export const getProfile = async (): Promise<Profile | null> => {
  try {
    const response = await client.get<Profile>('/auth/users/me/')
    return response.data
  } catch (error) {
    return null
  }
}
