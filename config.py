import os
from dotenv import load_dotenv  # Opcional: para usar variables de entorno (.env)

# Cargar variables del archivo .env (si existe)
load_dotenv()

class Config:
    # Clave secreta (¡obligatoria para sesiones y CSRF!)
    SECRET_KEY = os.getenv('SECRET_KEY', 'una-clave-secreta-por-defecto')  # Usa una clave fuerte en producción


    # Otras configuraciones
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = False

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')  # En producción, NUNCA uses una clave por defecto

