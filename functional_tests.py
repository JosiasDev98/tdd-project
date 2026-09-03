from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Adicionamos a importação do 'By'
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self): 
    
        # Maria decidiu utilizar o novo app TODO. Ela entra em sua página principal:
        self.browser.get('http://localhost:8000')

        # Ela nota que o título da página menciona TODO
        self.assertIn('To-Do', self.browser.title)
        
        # Note a nova sintaxe abaixo utilizando o By.TAG_NAME
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text  
        self.assertIn('To-Do', header_text)

        # Usando By.ID
        inputbox = self.browser.find_element(By.ID, 'id_new_item')  
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # Ela digita "Estudar testes funcionais" em uma caixa de texto
        inputbox.send_keys('Estudar testes funcionais')

        # Quando ela aperta enter, a página atualiza, e mostra a lista
        # "1: Estudar testes funcionais" como um item da lista TODO
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        table = self.browser.find_element(By.ID, 'id_list_table')
        
        # Para múltiplos elementos, usamos find_elements (no plural)
        rows = table.find_elements(By.TAG_NAME, 'tr')  
        self.assertTrue(
            any(row.text == '1: Estudar testes funcionais' for row in rows),
            "New to-do item did not appear in table"
        )

if __name__ == '__main__':
    unittest.main()