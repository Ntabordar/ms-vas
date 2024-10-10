import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env en desarrollo
if os.getenv('ENVIRONMENT', 'dev') == 'dev':
    load_dotenv()  # Carga las variables del archivo .env

# Cargar las variables de entorno
URL_MOTOR = os.getenv('URL_MOTOR')
