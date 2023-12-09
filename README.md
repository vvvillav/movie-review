# Movie Reviews

Movie Reviews es una app para poder ver reviews de peliculas

# Pre requisitos
- Tener instalado y en ejecucion, una instancia local de PostgreSQL
- Node 18 y NPM
- Python3

# Migraciones
Poner aqui los pasos para crear la tabla y poner los datos en la tabla
1.Descargar el archivo del dataset, colocarlo en la carpeta `movies/movies/migrations` y guardarlo como movie.txt
2. Ejecutar el siguiente comando `python3 python.py`
3. Ir a la carpeta `movies/movies/migrations` y copiar el contenido del archivo `reviews.sql`
4. python manage.py makemigrations
5. python manage.py migrate

# Instalacion

Movie Reviews consta de un backend en Django y un frontend en Vue.js

### Backend

1. Ir mediante consola a la carpeta `movies` con el comando `cd movies`   
2. Ejecutar el backend con el comando `python manage.py runserver`


### Frontend

1. Ir mediante consola a la carpeta `movie-review` con el comando `cd movie-review`
2. Instalar las dependencias con el comando `npm install`
3. Ejecutar el frontend con el comando `npm run dev`
