from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Lista de equipamentos a serem pesquisados
equipamentos = ["medidor de umidade relativa"]

# Inicializar o navegador
navegador = webdriver.Chrome()
wait = WebDriverWait(navegador, 10)
navegador.get("http://www.inmetro.gov.br/laboratorios/rbc/consulta.asp")
navegador.maximize_window()
contador = 1
try:
    for equipamento in equipamentos:
        print(f"Pesquisando por: {equipamento}\n")

        # Localizar e preencher o campo de pesquisa
        campo_nome = wait.until(EC.presence_of_element_located((By.NAME, "nom_servico")))
        campo_nome.clear()
        campo_nome.send_keys(equipamento)

        # Clicar no botão de pesquisar
        botao_pesquisar = navegador.find_element(By.NAME, "Submit")
        botao_pesquisar.click()

        pagina = 1

        while True:
            try:
                # Esperar a tabela de resultados carregar
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "listagem")))
                empresas = navegador.find_elements(By.CLASS_NAME, "listagem")
                lista_de_empresas = []

                # Coletar dados das empresas
                for i in range(0, len(empresas), 6):
                    if i + 5 < len(empresas):
                        empresa = {
                            "ID": empresas[i].text,
                            "Nome": empresas[i + 1].text,
                            "Status": empresas[i + 2].text,
                            "Estado": empresas[i + 3].text,
                            "Categoria": empresas[i + 4].text,
                        }
                        lista_de_empresas.append(empresa)

                # Exibir resultados da página atual
                if lista_de_empresas:
                    for empresa in lista_de_empresas:
                        print("-" * 40)
                        print(f"ID: {empresa['ID']}")
                        print(f"Nome: {empresa['Nome']}")
                        print(f"Status: {empresa['Status']}")
                        print(f"Estado: {empresa['Estado']}")
                        print(f"Categoria: {empresa['Categoria']}")
                        print("-" * 40, "\n")
                        contador +=1
                else:
                    print("Nenhuma empresa encontrada para este equipamento.")
                    break

                # Procurar botão de próxima página apenas depois de exibir os resultados
                botoes = navegador.find_elements(By.TAG_NAME, "a")
                proxima_pagina = None

                for botao in botoes:
                    try:
                        if botao.text.isdigit() and int(botao.text) == pagina + 1:
                            proxima_pagina = botao
                            break
                    except ValueError:
                        continue

                if proxima_pagina:
                    print(f"Indo para a página {pagina + 1}\n")
                    proxima_pagina.click()
                    pagina += 1
                    time.sleep(3)
                else:
                    print("Fim dos resultados.\n")
                    break
            except Exception as e:
                print(f"Erro ao processar página {pagina}: {e}")
                break

except Exception as e:
    print(f"Erro geral: {e}")
finally:
    time.sleep(5)
    navegador.quit()
    print("Foram encontradas {} empresas que realizam este tipo de equipamento".format(contador))
    print("Navegador fechado.")
