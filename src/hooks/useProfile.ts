import { useQuery } from "@tanstack/react-query";

// TODO. Configurar ts para no usar import relativos y usar imports absolutos
import { getProfile } from "../api";

const useProfile = () =>
  useQuery({
    queryKey: ["profile"],
    queryFn: getProfile,
  });

export default useProfile;
