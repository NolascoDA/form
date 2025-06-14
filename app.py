from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# 1. Cargar variables de entorno
print("DEBUG: Cargando archivo .env...")
load_dotenv()
print("DEBUG: Archivo .env cargado")

# 2. Verificar que las variables se cargaron
secret_key = os.getenv('SECRET_KEY')
mail_server = os.getenv('MAIL_SERVER')
mail_username = os.getenv('MAIL_USERNAME')

print(f"DEBUG: SECRET_KEY encontrada: {bool(secret_key)}")
print(f"DEBUG: MAIL_SERVER: {mail_server}")
print(f"DEBUG: MAIL_USERNAME: {mail_username}")

# 3. CREAR la aplicación Flask (¡IMPORTANTE: Esto va ANTES de la configuración!)
app = Flask(__name__)

# 4. CONFIGURAR la aplicación (DESPUÉS de crearla)
app.config['SECRET_KEY'] = secret_key or 'clave-desarrollo-temporal-123456789012345678901234567890'
app.config['MAIL_SERVER'] = mail_server
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Verificar configuración crítica
print("DEBUG: Configuración de Flask:")
print(f"DEBUG: SECRET_KEY configurada: {bool(app.config['SECRET_KEY'])}")
print(f"DEBUG: MAIL_SERVER configurado: {app.config['MAIL_SERVER']}")
print(f"DEBUG: MAIL_USERNAME configurado: {app.config['MAIL_USERNAME']}")

# 5. Inicializar extensiones
mail = Mail(app)
print("DEBUG: Flask-Mail inicializado")

# 6. Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar_correo():
    try:
        # Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']
        
        print(f"DEBUG: Datos recibidos - Nombre: {nombre}, Email: {email}")
        
        # Validar campos obligatorios
        if not all([nombre, email, asunto, mensaje]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('index'))
        
        # Crear mensaje
        msg = Message(
            subject=f"Contacto: {asunto}",
            recipients=[app.config['MAIL_USERNAME']],
            reply_to=email
        )
        
        # Cuerpo del mensaje
        msg.body = f"""
        Nuevo mensaje de contacto:
        
        Nombre: {nombre}
        Email: {email}
        Asunto: {asunto}
        
        Mensaje:
        {mensaje}
        """
        
        print("DEBUG: Intentando enviar correo...")
        
        # Enviar correo
        mail.send(msg)
        
        print("DEBUG: Correo enviado exitosamente")
        flash('¡Mensaje enviado correctamente!', 'success')
        return render_template('success.html', nombre=nombre)
        
    except Exception as e:
        print(f"DEBUG: Error al enviar correo: {str(e)}")
        flash(f'Error al enviar el mensaje: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    print("DEBUG: Iniciando servidor Flask...")
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto de Render o 5000 por defecto
    app.run(host='0.0.0.0', port=port)
    app.run(debug=False)