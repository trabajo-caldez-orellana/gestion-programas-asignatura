import styled from 'styled-components'

export const Portada = styled.div`
  width: 100%;
  background-color: var(--secondary-color);
  height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
`

export const Division = styled.div`
  width: 100%;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-color);
  color: white;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 20px;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
`

export const SeccionFuncionalidades = styled.div`
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  flex-direction: row;
  flex-wrap: wrap;
  margin: 30px 0;
`

export const Funcionalidad = styled.div`
  margin: 30px;
  border-radius: 10px;
  height: 300px;
  width: 420px;
  background-color: #00000008;
  box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -webkit-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  -moz-box-shadow: 5px 5px 5px 0px rgba(0, 0, 0, 0.1);
  transition: 0.5s ease-in-out;

  &:hover {
    transform: scale(1.05);
  }
`

export const TituloFuncionalidad = styled.h1`
  width: 100%;
  text-align: center;
  font-size: 20px;
  border-radius: 10px 10px 0 0;
  padding: 10px 0;
  color: var(--primary-color);
  text-transform: uppercase;
  font-weight: 400;
  letter-spacing: 1.5px;
`

export const IconoFuncionalidad = styled.div`
  height: 100px;
  width: 100px;
  background-color: var(--secondary-color);
  color: #ffffffaa;
  border-radius: 50%;
  margin: 20px auto 10px auto;
  font-size: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
`

export const DescripcionFuncionalidad = styled.div`
  padding: 5px 20px;
  font-size: 15px;
  letter-spacing: 1px;
  line-height: 20px;
  text-align: center;
`

export const TextoBienvenidaContainer = styled.div`
  width: 450px;
  padding: 30px 20px;
  border-radius: 10px;
  display: flex;
  background-color: #0000000f;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 50px 0 auto;
`

export const LogoFacet = styled.img`
  position: absolute;
  bottom: 30px;
  left: 10px;
  height: 70px;
`
