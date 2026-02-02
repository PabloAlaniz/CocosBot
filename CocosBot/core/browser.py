from playwright.sync_api import sync_playwright
from typing import Optional, Dict, Any
from CocosBot.config.general import DEFAULT_TIMEOUT
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import time

class PlaywrightBrowser:
    """
    Abstracción de Playwright para automatización web.
    
    Proporciona métodos de alto nivel para interactuar con páginas web,
    manejar elementos, interceptar requests, y procesar respuestas.
    """

    def __init__(self, headless=False):
        """
        Inicializa el navegador Playwright.
        
        Args:
            headless: Si True, ejecuta el navegador en modo headless (sin UI).
        """
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        logger.info("Navegador y página iniciados.")

    def __enter__(self):
        """Método para usar la clase con 'with'."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el navegador al salir del bloque 'with'."""
        self.close_browser()

    def close_browser(self):
        """Cierra el navegador y el contexto Playwright."""
        self.browser.close()
        self.playwright.stop()
        logger.info("Navegador cerrado.")

    def go_to(self, url, log_message=None):
        """
        Navega a una URL específica.
        
        Args:
            url: URL de destino.
            log_message: Mensaje opcional para logging.
        """
        self.page.goto(url)
        logger.info(f"Navegado a {url}")

    def wait_for_element(self, selector, log_message=None, timeout=None):
        """
        Espera a que un elemento sea visible en la página.
        
        Args:
            selector: Selector CSS del elemento.
            log_message: Mensaje opcional para logging.
            timeout: Tiempo máximo de espera en ms (usa DEFAULT_TIMEOUT si no se especifica).
        """
        timeout = timeout or DEFAULT_TIMEOUT
        self.page.wait_for_selector(selector, timeout=timeout, state="visible")
        logger.info(f"Elemento encontrado: {selector}")
        if log_message:
            logger.info(log_message)

    def click_element(self, selector, log_message=None, timeout=None):
        """
        Espera a que un elemento sea visible y hace clic en él.
        
        Args:
            selector: Selector CSS del elemento.
            log_message: Mensaje opcional para logging.
            timeout: Tiempo máximo de espera en ms.
        """
        self.wait_for_element(selector, timeout)
        self.page.click(selector)
        logger.info(f"Clic en el elemento: {selector}")
        if log_message:
            logger.info(log_message)

    def fill_input(self, selector, value, log_message=None, timeout=None):
        """
        Espera a que un input sea visible y lo llena con un valor.
        
        Args:
            selector: Selector CSS del input.
            value: Valor a ingresar.
            log_message: Mensaje opcional para logging.
            timeout: Tiempo máximo de espera en ms.
        """
        self.wait_for_element(selector, timeout)
        self.page.fill(selector, value)
        logger.info(f"Input {selector} llenado con el valor: {value}")
        if log_message:
            logger.info(log_message)

    def fill_input_with_events(self, selector, value, log_message=None, timeout=None):
        """
        Espera a que un input sea visible, lo llena con un valor y simula eventos adicionales para su procesamiento.

        Args:
            selector (str): Selector del input.
            value (str): Valor a ingresar.
            log_message (str): Mensaje opcional para el log.
            timeout (int): Tiempo máximo de espera para encontrar el elemento.
        """
        self.wait_for_element(selector, timeout)
        self.page.fill(selector, value)
        logger.info(f"Input {selector} llenado con el valor: {value}")
        if log_message:
            logger.info(log_message)

        # Simular un evento 'Enter' y 'Blur'
        self.page.keyboard.press("Enter")  # Simula que el usuario presiona Enter
        self.page.locator(selector).evaluate("el => el.blur()")  # Simula pérdida de foco (blur)
        logger.info(f"Eventos adicionales simulados para el selector: {selector}")

    import time

    def fill_input_with_delay(self, selector, value, log_message=None, timeout=None, delay=0.4):
        """
        Llena un input carácter por carácter con un retraso entre cada tecla.

        Args:
            selector (str): Selector del input.
            value (str): Valor a ingresar.
            log_message (str): Mensaje opcional para log.
            timeout (int): Tiempo máximo para esperar el elemento.
            delay (float): Tiempo en segundos entre cada tecla.

        """
        self.wait_for_element(selector, timeout)
        input_element = self.page.locator(selector)

        # Limpiar el campo antes de escribir
        input_element.fill("")
        logger.info(f"Input {selector} limpiado.")

        # Escribir carácter por carácter con retraso
        for char in value:
            input_element.type(char)
            time.sleep(delay)

        logger.info(f"Input {selector} llenado con el valor: {value}")
        if log_message:
            logger.info(log_message)

    def get_text_content(self, selector, timeout=None):
        """
        Obtiene el contenido de texto de un elemento.
        
        Args:
            selector: Selector CSS del elemento.
            timeout: Tiempo máximo de espera en ms.
            
        Returns:
            str: Contenido de texto del elemento.
        """
        self.wait_for_element(selector, timeout)
        text = self.page.text_content(selector)
        logger.info(f"Contenido de texto del elemento {selector}: {text}")
        return text

    def take_screenshot(self, filename="screenshot.png"):
        """
        Toma una captura de pantalla de la página actual.
        
        Args:
            filename: Nombre del archivo donde guardar la captura (default: screenshot.png).
        """
        self.page.screenshot(path=filename)
        logger.info(f"Captura de pantalla guardada en: {filename}")


    def process_response(self, response, success_message=None):
        """
        Procesa una respuesta interceptada por Playwright.

        Args:
            response: La respuesta interceptada por Playwright.
            success_message (str): Mensaje opcional que se registra en caso de éxito.

        Returns:
            dict: El contenido JSON de la respuesta si es exitosa, de lo contrario, None.
        """
        try:
            if response.status == 200:
                data = response.json()
                if success_message:
                    logger.info(success_message)
                return data
            else:
                logger.error(f"Error en la solicitud interceptada: {response.status}")
                logger.debug(f"Encabezados de respuesta: {response.headers}")
                logger.debug(f"Cuerpo de respuesta: {response.text()}")
                return None
        except Exception as e:
            logger.error(f"Error al procesar la respuesta: {e}")
            return None

    def search_and_select(self, search_input_selector, search_term, list_item_selector, log_message):
        """
        Busca un término en un campo y selecciona el ítem correspondiente de una lista.

        Args:
            search_input_selector (str): Selector del campo de búsqueda.
            search_term (str): Término a buscar.
            list_item_selector (str): Selector del ítem a seleccionar.
            log_message (str): Mensaje de registro para la acción.
        """
        self.fill_input(search_input_selector, search_term, f"Ingresando '{search_term}' en el campo de búsqueda.")
        self.click_element(list_item_selector.format(search_term), log_message)

    def fetch_data(self, request_url: str, navigation_url: str, process_response=None,
                   timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict[str, Any]]:
        """
        Intercepta un request específico y procesa su respuesta.
        
        Args:
            request_url: URL del request a interceptar.
            navigation_url: URL a la que navegar para disparar el request.
            process_response: Función opcional para procesar la respuesta antes de retornarla.
            timeout: Tiempo máximo de espera en ms.
            
        Returns:
            Optional[Dict[str, Any]]: Datos de la respuesta procesados o None si falla.
        """
        try:
            self.go_to(navigation_url)

            # Registrar respuestas generales mientras esperamos una específica
            def handle_response(response):
                if request_url in response.url:
                    logger.info(f"Respuesta interceptada: URL={response.url}, Estado={response.status}")
                    return response

            self.page.on("response", handle_response)

            with self.page.expect_response(request_url, timeout=timeout) as response_info:
                logger.info(f"Esperando la respuesta de {request_url}...")
                response = response_info.value

            # Procesar respuesta
            if response and response.status == 200:
                try:
                    data = response.json()
                    logger.debug("Contenido de la respuesta (JSON): %s", data)
                    if not data:
                        logger.info(f"No se encontraron datos en la respuesta para {request_url}.")
                        return None
                    if process_response:
                        return process_response(data)
                    return data
                except Exception as e:
                    logger.error("No se pudo decodificar el JSON de la respuesta: %s", e)
                    return None
            else:
                logger.warning(f"Respuesta no exitosa o nula. Estado: {getattr(response, 'status', 'Desconocido')}")
                return None

        except TimeoutError:
            logger.info(f"No se encontraron datos para {request_url} antes del timeout.")
            return None
        except Exception as e:
            logger.error(f"Error general en fetch_data: {e}")
            return None
