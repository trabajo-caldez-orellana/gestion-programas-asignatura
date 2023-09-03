import React, { useEffect } from "react";

import useProfile from "./hooks/useProfile";
import useGoogleAuthLink from "./hooks/useGoogleAuthLink";
import useGoogleAuthToken from "./hooks/useGoogleAuthToken";

function App() {
  // TODO. Crear un contenedor para poder wrap la app con todo esto en vez de que quede todo aca y sucio
  const { data: profile, refetch: fetchProfile } = useProfile();
  const { data: googleAuth, refetch: fetchGoogleAuth } = useGoogleAuthLink();
  const { mutate, isSuccess } = useGoogleAuthToken();

  useEffect(() => {
    if (googleAuth) {
      window.location.replace(googleAuth.authorizationUrl);
    }
  }, [googleAuth]);

  useEffect(() => {
    const searchParams = new URLSearchParams(document.location.search);

    const code = searchParams.get("code");
    const state = searchParams.get("state");

    if (code && state) {
      mutate({ code, state });
    }
  }, [mutate]);

  useEffect(() => {
    if (isSuccess) {
      fetchProfile();
    }
  }, [isSuccess, fetchProfile]);

  useEffect(() => {
    if (googleAuth) {
      window.location.replace(googleAuth.authorizationUrl);
    }
  }, [googleAuth]);

  const handleGoogleLogin = () => {
    fetchGoogleAuth();
  };

  return (
    <div className="App">
      {profile ? (
        <h1>Bienvenido {profile.firstName}! :D</h1>
      ) : (
        <button onClick={handleGoogleLogin}>Iniciar sesion con Google</button>
      )}
    </div>
  );
}

export default App;
