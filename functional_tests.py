from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # Este é o nosso método auxiliar para evitar repetição de código
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self): 
        # Maria entra na página principal
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text  
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element(By.ID, 'id_new_item')  
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Ela digita "Estudar testes funcionais" e aperta enter
        inputbox.send_keys('Estudar testes funcionais')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # O teste usa o helper method para checar se o primeiro item aparece
        self.check_for_row_in_list_table('1: Estudar testes funcionais')

        # A caixa de texto ainda a convida a adicionar outro item.
        # Ela digita "Fazer a licao de casa" e aperta enter
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Fazer a licao de casa')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A página atualiza novamente e agora mostra os dois itens na lista
        self.check_for_row_in_list_table('1: Estudar testes funcionais')
        self.check_for_row_in_list_table('2: Fazer a licao de casa')

if __name__ == '__main__':
    unittest.main()