"""Tests for CocosBot.utils.gmail_2fa"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from CocosBot.utils.gmail_2fa import (
    conectar_imap,
    buscar_correos,
    procesar_html,
    extraer_y_eliminar_codigo_2fa,
    eliminar_correo,
    obtener_codigo_2FA,
)


class TestConectarImap:
    """Tests for conectar_imap"""

    @patch('CocosBot.utils.gmail_2fa.imaplib.IMAP4_SSL')
    def test_conectar_imap_success(self, mock_imap):
        mock_mail = Mock()
        mock_imap.return_value = mock_mail

        result = conectar_imap("test@gmail.com", "app_pass")

        mock_imap.assert_called_once_with('imap.gmail.com')
        mock_mail.login.assert_called_once_with("test@gmail.com", "app_pass")
        mock_mail.select.assert_called_once_with('inbox')
        assert result == mock_mail

    @patch('CocosBot.utils.gmail_2fa.imaplib.IMAP4_SSL')
    def test_conectar_imap_login_fails(self, mock_imap):
        mock_mail = Mock()
        mock_mail.login.side_effect = Exception("Login failed")
        mock_imap.return_value = mock_mail

        with pytest.raises(Exception, match="Login failed"):
            conectar_imap("test@gmail.com", "wrong_pass")


class TestBuscarCorreos:
    """Tests for buscar_correos"""

    def test_buscar_correos_finds_emails(self):
        mock_mail = Mock()
        mock_mail.search.return_value = ('OK', [b'1 2 3'])

        result = buscar_correos(mock_mail, "no-reply@cocos.capital")

        mock_mail.search.assert_called_once_with(None, '(FROM "no-reply@cocos.capital")')
        assert result == [b'1', b'2', b'3']

    def test_buscar_correos_no_emails(self):
        mock_mail = Mock()
        mock_mail.search.return_value = ('OK', [b''])

        result = buscar_correos(mock_mail, "no-reply@cocos.capital")

        # b''.split() returns []
        assert result == []


class TestProcesarHtml:
    """Tests for procesar_html"""

    def test_procesar_html_finds_code(self):
        html = b'<html><body><span style="font-size: 32px; color: blue;">123456</span></body></html>'
        result = procesar_html(html)

        assert result == "123456"

    def test_procesar_html_no_code(self):
        html = b'<html><body><span style="font-size: 14px;">No code here</span></body></html>'
        result = procesar_html(html)

        assert result is None

    def test_procesar_html_different_style(self):
        html = b'<html><body><span style="color: red; font-size: 32px; font-weight: bold;">654321</span></body></html>'
        result = procesar_html(html)

        assert result == "654321"


class TestExtraerYEliminarCodigo:
    """Tests for extraer_y_eliminar_codigo_2fa"""

    def test_extraer_multipart(self):
        mock_mail = Mock()
        html_content = b'<html><body><span style="font-size: 32px;">987654</span></body></html>'

        # Build a multipart email
        html_part = Mock()
        html_part.get_content_type.return_value = 'text/html'
        html_part.get_payload.return_value = html_content

        text_part = Mock()
        text_part.get_content_type.return_value = 'text/plain'

        import email as email_module
        raw_email = (
            b'Content-Type: multipart/alternative; boundary="boundary"\r\n'
            b'Subject: 2FA Code\r\n\r\n'
            b'--boundary\r\n'
            b'Content-Type: text/plain\r\n\r\n'
            b'Your code is 987654\r\n'
            b'--boundary\r\n'
            b'Content-Type: text/html\r\n\r\n'
            b'<html><body><span style="font-size: 32px;">987654</span></body></html>\r\n'
            b'--boundary--\r\n'
        )

        mock_mail.fetch.return_value = ('OK', [(b'1 (RFC822 {1234}', raw_email), b')'])

        result = extraer_y_eliminar_codigo_2fa(mock_mail, b'1')

        assert result == "987654"
        # Should delete the email after extraction
        mock_mail.store.assert_called_once_with(b'1', '+FLAGS', '\\Deleted')
        mock_mail.expunge.assert_called_once()

    def test_extraer_single_part(self):
        mock_mail = Mock()
        raw_email = (
            b'Content-Type: text/html\r\n'
            b'Subject: 2FA Code\r\n\r\n'
            b'<html><body><span style="font-size: 32px;">111222</span></body></html>'
        )

        mock_mail.fetch.return_value = ('OK', [(b'1 (RFC822 {500}', raw_email), b')'])

        result = extraer_y_eliminar_codigo_2fa(mock_mail, b'1')

        assert result == "111222"
        mock_mail.store.assert_called_once()

    def test_extraer_no_code_found(self):
        mock_mail = Mock()
        raw_email = (
            b'Content-Type: text/html\r\n'
            b'Subject: Other Email\r\n\r\n'
            b'<html><body><p>No code here</p></body></html>'
        )

        mock_mail.fetch.return_value = ('OK', [(b'1 (RFC822 {300}', raw_email), b')'])

        result = extraer_y_eliminar_codigo_2fa(mock_mail, b'1')

        assert result is None
        # Should NOT delete when no code found
        mock_mail.store.assert_not_called()


class TestEliminarCorreo:
    """Tests for eliminar_correo"""

    def test_eliminar_correo(self):
        mock_mail = Mock()
        eliminar_correo(mock_mail, b'5')

        mock_mail.store.assert_called_once_with(b'5', '+FLAGS', '\\Deleted')
        mock_mail.expunge.assert_called_once()


class TestObtenerCodigo2FA:
    """Tests for obtener_codigo_2FA"""

    @patch('CocosBot.utils.gmail_2fa.time.sleep')
    @patch('CocosBot.utils.gmail_2fa.extraer_y_eliminar_codigo_2fa')
    @patch('CocosBot.utils.gmail_2fa.buscar_correos')
    @patch('CocosBot.utils.gmail_2fa.conectar_imap')
    def test_obtener_codigo_happy_path(self, mock_connect, mock_search, mock_extract, mock_sleep):
        mock_mail = Mock()
        mock_connect.return_value = mock_mail
        mock_search.return_value = [b'1', b'2', b'3']
        mock_extract.return_value = "123456"

        result = obtener_codigo_2FA("test@gmail.com", "app_pass", "sender@example.com")

        assert result == "123456"
        mock_sleep.assert_called_once_with(20)
        mock_connect.assert_called_once_with("test@gmail.com", "app_pass")
        mock_search.assert_called_once_with(mock_mail, "sender@example.com")
        # Should use the last email
        mock_extract.assert_called_once_with(mock_mail, b'3')

    @patch('CocosBot.utils.gmail_2fa.time.sleep')
    @patch('CocosBot.utils.gmail_2fa.buscar_correos')
    @patch('CocosBot.utils.gmail_2fa.conectar_imap')
    def test_obtener_codigo_no_emails(self, mock_connect, mock_search, mock_sleep):
        mock_mail = Mock()
        mock_connect.return_value = mock_mail
        mock_search.return_value = []

        result = obtener_codigo_2FA("test@gmail.com", "app_pass", "sender@example.com")

        assert result is None

    @patch('CocosBot.utils.gmail_2fa.time.sleep')
    @patch('CocosBot.utils.gmail_2fa.extraer_y_eliminar_codigo_2fa')
    @patch('CocosBot.utils.gmail_2fa.buscar_correos')
    @patch('CocosBot.utils.gmail_2fa.conectar_imap')
    def test_obtener_codigo_uses_latest_email(self, mock_connect, mock_search, mock_extract, mock_sleep):
        mock_mail = Mock()
        mock_connect.return_value = mock_mail
        mock_search.return_value = [b'10', b'20', b'30']
        mock_extract.return_value = "654321"

        result = obtener_codigo_2FA("test@gmail.com", "app_pass", "sender@example.com")

        # Should pick the last email id
        mock_extract.assert_called_once_with(mock_mail, b'30')
        assert result == "654321"
