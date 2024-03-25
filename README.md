# Gestión de Programas de Asignatura

# Setup con Docker!
1. Setear variables de entorno en el archivo `.env` del frontend y del backend
2. En el root del proyecto, correr el siguiente comando: `docker compose up`

LISTO! Ahora se puede acceder a `http://127.0.0.1:5173` para ver el proyecto. 
Si se quiere acceder al panel de admin de django, se debe acceder a `http://127.0.0.1:8000/admin/`.
Es necesario crear un superusuario, y para eso se debe ingresar al container del backend y crear un superusuario con `python manage.py createsuperuser`

# SI NO SE USA DOCKER SEGUIR LAS SIGUIENTES INSTRUCCIONES
## Setup de frontend
1. Instalar dependencias con `npm install`
2. Setear variables de entorno en el archivo `.env`
3. Correr servidor con `npm run dev`
4. Se puede visitar la pagina en `http://127.0.0.1:5173`

Para poder correr las funcionalidades del sistema, es necesario correr el backend. 

## Setup del backend
1. Crear entorno virtual de python, con versión de Python `3.11.4`.
2. Activar el entorno virtual.
3. Instalar dependencias con `pip install -r requirements.txt`
4. Correr las migraciones con `python manage.py migrate`
5. Crear instancias de prueba con el comando `python manage.py setup`
6. Correr el servidor con `python manage.py runserver`

Se puede visitar el Administrador de Django se debe:
1. Crear un superusuario con `python manage.py createsuperuser`, y seguir los pasos indicados en la terminal.
2. Visitar `http://127.0.0.1:8000/admin/`, e iniciar sesión

El comando de `setup` crea las siguientes instancias:
- 3 Carreras
- 1 plan de estudio activo por carrera y uno inactivo por carrera
- 3 años lectivos: uno arrancando el año pasado de corrido el comando, otro iniciando en el año actual, y otro el año siguiente
- 2 cuatrimestres por año lectivo
- 1 estándar por carrera
- 3 Actividades Reservadas por estándar
- 9 Descriptores y 9 ejes reservados. Cada carrera tiene 2 descriptores y ejes reservados que le pertenecen y 3 de cada uno compartido entre todos
- 12 asignaturas. 3 asignaturas son únicas para cada carrera, y 3 asignaturas compartidas. 4 serán híbridas, 4 presenciales y 4 virtuales 

## Cómo asignar un Rol a un usuario?
1. Ingresar a el panel de Administración. 
2. Ingresar al modelo Usuarios.
3. Elegir el usuario que se quiere asignar un rol, y elegir el tipo de rol, y la opción extra requerida para el usuario. Un Director de Carrera debe seleccionar una carrera. Un titular de cátedra o docente debe seleccionar una asignatura. El Secretario académico no debe elegir ni carrera ni asignatura. 