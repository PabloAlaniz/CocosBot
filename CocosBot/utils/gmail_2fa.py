import imaplib
import email
import time
from bs4 import BeautifulSoup


def conectar_imap(email_address, password):
    """Conecta al servidor IMAP y autentica al usuario."""
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_address, password)
    mail.select('inbox')
    return mail


def buscar_correos(mail, sender_address):
    """Busca correos del remitente especificado y devuelve los IDs de los correos."""
    status, data = mail.search(None, f'(FROM "{sender_address}")')
    mail_ids = data[0]
    return mail_ids.split()


def extraer_y_eliminar_codigo_2fa(mail, email_id):
    """Extrae el código 2FA del correo y lo elimina después de la extracción."""
    codigo_2fa = None
    status, data = mail.fetch(email_id, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])
            if message.is_multipart():
                for part in message.get_payload():
                    if part.get_content_type() == 'text/html':
                        codigo_2fa = procesar_html(part.get_payload(decode=True))
            else:
                if message.get_content_type() == 'text/html':
                    codigo_2fa = procesar_html(message.get_payload(decode=True))

    if codigo_2fa:
        eliminar_correo(mail, email_id)

    return codigo_2fa


def eliminar_correo(mail, email_id):
    """Elimina el correo especificado por email_id."""
    mail.store(email_id, '+FLAGS', '\\Deleted')
    mail.expunge()


def procesar_html(html_content):
    """Procesa el contenido HTML para encontrar y devolver el código 2FA."""
    soup = BeautifulSoup(html_content, 'html.parser')

    codigo_2fa = soup.find('span', style=lambda value: value and 'font-size: 32px' in value)
    return codigo_2fa.text if codigo_2fa else None


def obtener_codigo_2FA(email_address, password, sender_address):
    time.sleep(20)
    mail = conectar_imap(email_address, password)
    ids_correos = buscar_correos(mail, sender_address)
    latest_email_id = ids_correos[-1] if ids_correos else None
    if latest_email_id:
        return extraer_y_eliminar_codigo_2fa(mail, latest_email_id)
    return None
