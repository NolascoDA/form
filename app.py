'''
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
'''


from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# 1. Cargar variables de entorno
print("DEBUG: Cargando archivo .env...")
load_dotenv()
print("DEBUG: Archivo .env cargado")

# 2. Verificar que las variables se cargaron
secret_key = os.getenv('SECRET_KEY')
mail_server = os.getenv('MAIL_SERVER')
mail_username = os.getenv('MAIL_USERNAME')
mail_password = os.getenv('MAIL_PASSWORD')
mail_port = int(os.getenv('MAIL_PORT', 587))
mail_use_tls = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'

print(f"DEBUG: SECRET_KEY encontrada: {bool(secret_key)}")
print(f"DEBUG: MAIL_SERVER: {mail_server}")
print(f"DEBUG: MAIL_USERNAME: {mail_username}")
print(f"DEBUG: MAIL_PORT: {mail_port}")
print(f"DEBUG: MAIL_USE_TLS: {mail_use_tls}")

# 3. Crear la aplicación Flask
app = Flask(__name__)

# 4. Configurar la aplicación
app.config['SECRET_KEY'] = secret_key or 'clave-desarrollo-temporal-123456789012345678901234567890'

print("DEBUG: Configuración de Flask:")
print(f"DEBUG: SECRET_KEY configurada: {bool(app.config['SECRET_KEY'])}")

def enviar_email_smtp(destinatario, asunto, cuerpo, remitente_email):
    """
    Función para enviar email usando smtplib
    """
    try:
        # Crear mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = mail_username
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje['Reply-To'] = remitente_email
        
        # Adjuntar cuerpo del mensaje
        mensaje.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        
        # Crear conexión SMTP
        if mail_use_tls:
            # Usar STARTTLS
            servidor = smtplib.SMTP(mail_server, mail_port)
            servidor.starttls()
        else:
            # Usar SSL directo (puerto 465 típicamente)
            servidor = smtplib.SMTP_SSL(mail_server, mail_port)
        
        # Autenticarse
        servidor.login(mail_username, mail_password)
        
        # Enviar mensaje
        texto = mensaje.as_string()
        servidor.sendmail(mail_username, destinatario, texto)
        
        # Cerrar conexión
        servidor.quit()
        
        return True, "Correo enviado exitosamente"
        
    except smtplib.SMTPAuthenticationError as e:
        return False, f"Error de autenticación SMTP: {str(e)}"
    except smtplib.SMTPRecipientsRefused as e:
        return False, f"Destinatario rechazado: {str(e)}"
    except smtplib.SMTPServerDisconnected as e:
        return False, f"Servidor SMTP desconectado: {str(e)}"
    except smtplib.SMTPException as e:
        return False, f"Error SMTP: {str(e)}"
    except Exception as e:
        return False, f"Error general: {str(e)}"

# 5. Rutas
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
       
        # Validar configuración de email
        if not all([mail_server, mail_username, mail_password]):
            flash('Error de configuración del servidor de correo', 'error')
            return redirect(url_for('index'))
       
        # Preparar el asunto y cuerpo del mensaje
        asunto_completo = f"Contacto: {asunto}"
        cuerpo_mensaje = f"""
Nuevo mensaje de contacto:

Nombre: {nombre}
Email: {email}
Asunto: {asunto}

Mensaje:
{mensaje}
        """.strip()
       
        print("DEBUG: Intentando enviar correo con smtplib...")
       
        # Enviar correo usando smtplib
        exito, resultado = enviar_email_smtp(
            destinatario=mail_username,
            asunto=asunto_completo,
            cuerpo=cuerpo_mensaje,
            remitente_email=email
        )
       
        if exito:
            print("DEBUG: Correo enviado exitosamente")
            flash('¡Mensaje enviado correctamente!', 'success')
            return render_template('success.html', nombre=nombre)
        else:
            print(f"DEBUG: Error al enviar correo: {resultado}")
            flash(f'Error al enviar el mensaje: {resultado}', 'error')
            return redirect(url_for('index'))
       
    except Exception as e:
        print(f"DEBUG: Error general: {str(e)}")
        flash(f'Error inesperado: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    print("DEBUG: Iniciando servidor Flask...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)