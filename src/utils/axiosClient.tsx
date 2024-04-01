import axios from 'axios'
import Cookies from 'js-cookie'
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

client.interceptors.request.use(async (config) => {
  const token = Cookies.get('token')

  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }

  const refreshToken = Cookies.get('refresh_token');

  // Verificar si hay un token de actualización y el token de acceso ha caducado
  if (!token && refreshToken) {
    try {
      const res = await client.post("auth/token/refresh/", {
        refresh: refreshToken,
      });

      if (res.status === 200) {
        const horaActual = new Date();
        const quinceMinutosDespues = new Date(horaActual.getTime() + 15 * 60 * 1000);
        Cookies.set('token', res.data.access, { expires: quinceMinutosDespues, secure: true });

        // Actualiza el encabezado de autorización con el nuevo token
        config.headers['Authorization'] = `Bearer ${res.data.access}`;
      } else {
        window.location.href = '/login'
      }
    } catch (error) {
      console.log(error);
    }
  }

  return config
})
