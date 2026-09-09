from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
import time

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Usuário 1 (Maria) inicia uma nova lista
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Estudar testes funcionais')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Estudar testes funcionais')

        # O teste exige que a lista dela tenha um URL específico
        maria_list_url = self.browser.current_url
        self.assertRegex(maria_list_url, '/lists/.+')

        # Agora um novo usuário (João) entra no site.
        # Fechamos e reabrimos o navegador para limpar os cookies da Maria
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # João acessa a página inicial e não vê os itens de Maria
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Estudar testes funcionais', page_text)

        # João adiciona um item novo
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Comprar leite')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Comprar leite')

        # João ganha seu próprio URL exclusivo
        joao_list_url = self.browser.current_url
        self.assertRegex(joao_list_url, '/lists/.+')
        self.assertNotEqual(joao_list_url, maria_list_url)

        # Não há sinal dos itens de Maria
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Estudar testes funcionais', page_text)
        self.assertIn('Comprar leite', page_text)