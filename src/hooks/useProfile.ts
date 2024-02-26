import { useState, useEffect } from 'react'

// TODO. Configurar ts para no usar import relativos y usar imports absolutos
import { getProfile } from '../api'
import { Profile } from 'api/types'

type useProfileType = {
  profileData: Profile | undefined
  refetch: () => void
  isLoading: boolean
}

const useProfile = (): useProfileType => {
  const [profileData, setProfileData] = useState<Profile>()
  const [isLoading, setIsLoading] = useState<boolean>(true)

  const refetch = async () => {
    setIsLoading(true)
    const response = await getProfile()
    setProfileData(response || undefined)
    setIsLoading(false)
  }

  useEffect(() => {
    refetch()
  }, [])

  return { profileData, isLoading, refetch }
}

export default useProfile
