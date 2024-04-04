import axios from 'axios'
import { BASE_URL } from '../helpers/env-variables'
export const TOKEN_KEY = 'token'

export const client = axios.create({
  baseURL: BASE_URL
})

client.defaults.withCredentials = true;


client.interceptors.response.use((response) => {
  if (response.data) {
    response.data
  }

  return response
})
