from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # Mantenha o navegador que você já estava usando (Chrome ou Firefox)
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by='id', value='id_list_table')
                rows = table.find_elements(by='tag name', value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        # Agora usamos a URL do servidor de testes automático do Django
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(by='tag name', value='h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element(by='id', value='id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        
        # Substituímos o time.sleep() pela nossa função inteligente de espera
        self.wait_for_row_in_list_table('1: Comprar leite')

        inputbox = self.browser.find_element(by='id', value='id_new_item')
        inputbox.send_keys('Comprar pao')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Comprar leite')
        self.wait_for_row_in_list_table('2: Comprar pao')