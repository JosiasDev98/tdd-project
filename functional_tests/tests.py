from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        # Mantive o Chrome já que funcionou melhor no seu ambiente
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self): 
        # Trocamos o localhost fixo pela URL dinâmica do servidor de testes
        self.browser.get(self.live_server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text  
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')  
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Estudar testes funcionais')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Estudar testes funcionais')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Fazer a licao de casa')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Estudar testes funcionais')
        self.check_for_row_in_list_table('2: Fazer a licao de casa')