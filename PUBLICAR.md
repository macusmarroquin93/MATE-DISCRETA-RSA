# Publicar y entregar el enlace

Necesitas una cuenta de GitHub y otra de Streamlit Community Cloud. No necesitas
compartir contraseñas ni agregar credenciales a este proyecto.

## 1. Subir los archivos

1. Descomprime el ZIP.
2. En GitHub crea un repositorio, por ejemplo `rsa-lab-grupo-5`.
3. Sube el contenido de `Grupo_5_MMRG_Proyecto_Web` a la raíz del repositorio:
   `app.py`, `rsa.py`, `algoritmos.py`, `requirements.txt` y los demás archivos.
   Conserva también `.streamlit/config.toml` para el tema visual.
   No subas el ZIP como único archivo: Streamlit necesita leer el código.
4. Guarda los cambios con Commit changes. No subas entornos virtuales,
   `__pycache__`, contraseñas ni el video; no son necesarios para ejecutar la web.

## 2. Desplegar

1. Abre https://share.streamlit.io/ e inicia sesión; conecta GitHub si se solicita.
2. Pulsa Create app y selecciona tu repositorio y la rama que contiene el código.
3. En Main file path escribe `app.py`. Si subiste la carpeta completa dentro del
   repositorio, usa `Grupo_5_MMRG_Proyecto_Web/app.py`.
4. En Advanced settings selecciona Python 3.11, la versión usada en las pruebas.
5. Pulsa Deploy y espera a que aparezca la aplicación sin errores.

## 3. Hacer accesible la aplicación

En la configuración de acceso/compartir de la aplicación selecciona acceso
público, para que cualquiera con el enlace pueda abrirla. La aplicación no
implementa usuario ni contraseña. Comprueba que la plataforma tampoco pida
iniciar sesión al visitante. Un repositorio público por sí solo no demuestra
que la aplicación ya esté desplegada.

Abre el enlace en una ventana de incógnito y realiza el ejemplo RSA del README.
Debe permitir encriptar, transferir y desencriptar sin instalar Python.

## 4. Entregar

Copia la URL real que te asigne Streamlit, terminada en `.streamlit.app`, y
pégala en Canvas. No entregues `localhost`, la URL del repositorio ni una URL
inventada de ejemplo. La publicación queda pendiente hasta completar los pasos.

Antes de la revisión abre el enlace y verifica que esté activa. Community Cloud
puede suspender aplicaciones por inactividad; si aparece una pantalla de reposo,
reactívala y espera a que termine de iniciar. No se garantiza disponibilidad
permanente de un servicio gratuito.

## Documentación oficial

- Despliegue: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Dependencias: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- Acceso: https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app
- Límites: https://docs.streamlit.io/deploy/streamlit-community-cloud/status
