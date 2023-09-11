import { useMutation } from "@tanstack/react-query";
import { getGoogleAuthToken, OAuthCredential, TOKEN_KEY } from "../api";

// Obtiene el token y lo guarda en el local storage

const useGoogleAuthToken = () =>
  useMutation({
    mutationKey: ["google_auth_token"],
    mutationFn: (credential: OAuthCredential) => getGoogleAuthToken(credential),
    onSuccess: (data) => {
      const { access } = data;
      // Usar cookies en vez de local storage??
      localStorage.setItem(TOKEN_KEY, access);
    },
  });

export default useGoogleAuthToken;
