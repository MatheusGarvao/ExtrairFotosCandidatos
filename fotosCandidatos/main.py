from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv


def iniciar():
    with open('candidatos.csv', 'w', newline='') as f:  # abre o arquivo candidatos.csv para armazenar o nome e a foto
        fieldnames = ['pessoa', 'foto']  # nomes das colunas em que será armazenado
        escrever = csv.DictWriter(f, fieldnames=fieldnames)
        escrever.writeheader()

        # define o agente do usuário, caso esteja em outro sistema operacional, deve ser modificado de acordo com
        # o navegador

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
        firefox_options = Options()
        firefox_options.set_preference('general.useragent.override', user_agent)

        profile = FirefoxProfile()
        profile.set_preference('browser.cache.disk.enable', False)
        profile.set_preference('browser.cache.memory.enable', False)
        profile.set_preference('browser.cache.offline.enable', False)
        profile.set_preference('network.cookie.cookieBehavior', 2)

        driver = webdriver.Firefox(firefox_profile=profile)

        # tse: insira a aba dos cargos referente ao estado em que deseja obter os dados.

        tse = "https://divulgacandcontas.tse.jus.br/divulga/#/municipios/2022/2040602022/BR/cargos"  # website governo
        driver.get(tse)
        driver.maximize_window()
        driver.implicitly_wait(3000)

        # temp serve para saber a quantidade de cargos existentes
        temp = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div/section[3]/div/div/table/tbody")\
            .find_elements(By.CLASS_NAME, "ng-scope")

        # cada caminho destes serão usados ao longo do código.
        tamanho = len(temp)
        elemento = '/html/body/div[2]/div[1]/div/div/section[3]/div/div/table/tbody/tr[{}]/td'
        candidatos = '/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody/tr[{}]/td[2]'
        candidatoimagem = '/html/body/div[2]/div[1]/div/div[1]/section[1]/div/div[1]/img'
        clicarcandidato = '/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody/tr[{}]/td[1]/a'
        quantidadecandidatos = '/html/body/div[2]/div[1]/div/div/section[3]/div/div/table[1]/tbody'

        sair = 0
        pag = 0
        for i in range(1, tamanho + 1):
            if i != 3:
                time.sleep(1)
                WebDriverWait(driver, 30000).until(EC.element_to_be_clickable((By.XPATH, elemento.format(i)))).click()
                driver.implicitly_wait(3000)
                inside = len(
                    driver.find_element(By.XPATH, quantidadecandidatos)
                    .find_elements(By.TAG_NAME, 'tr'))
                for x in range(1, inside + 1):
                    anotar1 = driver.find_element(By.XPATH, candidatos.format(x)).text
                    time.sleep(1)
                    while pag == 0:
                        pag = 1
                        try:
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable
                                                            ((By.XPATH, clicarcandidato.format(x)))).click()
                        except:
                            time.sleep(1)
                            pag = 0
                    pag = 0
                    while sair == 0:
                        anotar2 = driver.find_element(By.XPATH, candidatoimagem).get_attribute('src')
                        print(anotar1, " ", anotar2)
                        if anotar2 is None:
                            time.sleep(0.5)
                            sair = 0
                        else:
                            sair = 1
                    escrever.writerow({'pessoa': anotar1, 'foto': anotar2})
                    sair = 0
                    driver.execute_script("window.history.go(-1)")
                    if x == 5:
                        driver.delete_all_cookies()
                driver.execute_script("window.history.go(-1)")


if __name__ == '__main__':
    iniciar()
