from imports import *
from config import *

driver = webdriver.Firefox()

def open_page(link):
    driver.get(link)
    time.sleep(10)

def click_element(driver, locator, locator_type=By.XPATH, max_retries=3, delay=2):
    """
    Clica em um elemento na página web.

    Parâmetros:
        driver: Instância do driver do Selenium.
        locator: Localizador do elemento (por exemplo, XPath, CSS Selector, ID).
        locator_type: Tipo de localizador (padrão: By.XPATH, ou By.CSS_SELECTOR, By.ID, By.NAME, By.CLASS_NAME, By.TAG_NAME, By.LINK_TEXT, By.PARTIAL_LINK_TEXT).
        max_retries: Número máximo de tentativas em caso de falha (padrão: 3).
        delay: Tempo de espera entre tentativas (padrão: 2 segundos).

    Retorna:
        True se o elemento foi clicado com sucesso, False caso contrário.
    """
    for attempt in range(max_retries):
        try:
            element = driver.find_element(locator_type, locator)
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            return True 
        except NoSuchElementException:
            print(f"Elemento não encontrado: {locator}. Tentativa {attempt + 1} de {max_retries}.")
        except ElementClickInterceptedException:
            print(f"Elemento não clicável: {locator}. Tentativa {attempt + 1} de {max_retries}.")
        time.sleep(delay)
    
    print(f"Falha ao clicar no elemento após {max_retries} tentativas.")
    return False 


def write_data(driver, locator, data, locator_type=By.XPATH, max_tentativas=3, delay=2):
    """
    Escreve dados em um campo de entrada em uma página web.

    Parâmetros:
        driver: Instância do driver do Selenium.
        locator: Localizador do elemento (por exemplo, XPath, CSS Selector, ID).
        data: O texto a ser escrito no campo de entrada.
        locator_type: Tipo de localizador (padrão: By.XPATH).
        max_tentativas: Número máximo de tentativas em caso de falha (padrão: 3).
        delay: Tempo de espera entre tentativas (padrão: 2 segundos).

    Retorna:
        True se os dados foram escritos com sucesso, False caso contrário.
    """
    for tentativa in range(max_tentativas):
        try:
            elemento = driver.find_element(locator_type, locator)
            driver.execute_script("arguments[0].scrollIntoView();", elemento)
            elemento.clear()
            elemento.send_keys(data)
            return True
        except NoSuchElementException:
            print(f"Elemento não encontrado: {locator}. Tentativa {tentativa + 1} de {max_tentativas}.")
        time.sleep(delay)
    
    print(f"Falha ao escrever dados no elemento após {max_tentativas} tentativas.")
    return False  

def print_dataframe(df_tweets, filename):
    # Exibe o DataFrame final
    if df_tweets is not None:
        print("DataFrame final:")
        print(df_tweets)
        # Salva o DataFrame em um arquivo CSV com o nome especificado
        df_tweets.to_csv(filename, index=False, encoding="utf-8")
        print(f"DataFrame salvo em '{filename}'.")

def find_tweet(driver, count):
    try:
        wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
        tweet = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]')))[count]
        print(f"Tweet {count + 1} encontrado!")
    
        # Encontra a div com data-testid="tweetText" dentro do tweet
        div_texto_tweet = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
        driver = abrir_tweet_em_nova_aba(driver, tweet)
        rolar_ate_o_final(driver)

        print("Div do texto do tweet encontrada! Clicando na div...")
        div_texto_tweet.click()  # Clica na div do texto do tweet
    except Exception as e:
        print(f"Erro ao interagir com o tweet: {e}")
    
    time.sleep(5)

def reload_function(n):
    for _ in range(n): 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
    verificar_e_clicar_retry(driver)

def rolar_ate_o_final(driver, max_tentativas=5):
    ultima_altura = driver.execute_script("return document.body.scrollHeight")
    tentativas = 0
    
    while tentativas < max_tentativas:
        verificar_e_clicar_retry(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Aguardar carregamento
        nova_altura = driver.execute_script("return document.body.scrollHeight")
        if nova_altura == ultima_altura:
            print("Fim da página alcançado.")
            break
        ultima_altura = nova_altura
        tentativas += 1

def abrir_tweet_em_nova_aba(driver, tweet_element):
    link = tweet_element.find_element(By.CSS_SELECTOR, 'a[href*="/status/"]').get_attribute("href")
    driver.execute_script(f"window.open('{link}', '_blank');")

    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)  
    
    return driver

def extract_tweet(driver, df_tweets):
    try:
        wait = WebDriverWait(driver, 10)  # Espera até 10 segundos

        tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))
        novos_tweets = []

        if tweets:
            tweet_principal = tweets[0].find_element(By.XPATH, './/span').text
            novos_tweets.append({"Tipo": "Principal", "Texto": tweet_principal}) 

            # Extrai os tweets relacionados
            for tweet in tweets[1:]: 
                try:
                    span_texto = tweet.find_element(By.XPATH, './/span')
                    texto = span_texto.text
                    novos_tweets.append({"Tipo": "Relacionado", "Texto": texto}) 
                except Exception as e:
                    print(f"Erro ao extrair texto de um tweet relacionado: {e}")
                
        df_novos_tweets = pd.DataFrame(novos_tweets)
        if not df_novos_tweets.empty:
            df_tweets = pd.concat([df_tweets, df_novos_tweets], ignore_index=True)
            print("DataFrame atualizado com sucesso!")
        else:
            print("Nenhum novo tweet foi extraído.")
        return df_tweets
    
    except Exception as e:
        print(f"Erro ao encontrar os tweets: {e}")
        return df_tweets

    finally:
        time.sleep(5)
    # Localizar todos os containers com data-testid="cellInnerDiv"
    # containers = WebDriverWait(driver, 15).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="cellInnerDiv"]'))
    # )
    
    # # Array para armazenar os textos dos spans
    # novos_tweets = []
    
    # # Iterar sobre cada container
    # for container in containers:
    #     # Coletar todos os spans dentro do container
    #     spans = container.find_elements(By.TAG_NAME, "span")
        
    #     # Extrair o texto de cada span e adicionar ao array
    #     for span in spans:
    #         texto = span.text.strip()  # Remove espaços em branco
    #         if texto:  # Ignora spans vazios
    #             novos_tweets.append({"Tipo": "Relacionado", "Texto": texto})
    
    # # Criar DataFrame com os novos tweets
    # if novos_tweets:
    #     df_novos = pd.DataFrame(novos_tweets)
    #     df_tweets = pd.concat([df_tweets, df_novos], ignore_index=True)
    #     print(f"{len(novos_tweets)} novos tweets coletados!")
    # else:
    #     print("Nenhum novo tweet foi encontrado.")
    
    # return df_tweets

def verificar_e_clicar_retry(driver):
    try:
        # Localiza o botão que contém um span com o texto "Retry"
        botao_retry = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button//div//span[text()="Retry"]'))
        )
        # Clica no botão "Retry"
        botao_retry.click()
        print("Botão 'Retry' encontrado e clicado!")
        return True
    except Exception as e:
        # Se o botão não for encontrado, apenas continua a execução
        return False
    
def clicar_botao_voltar(driver):
    try:
        botao_voltar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Back"]'))
        )
        botao_voltar.click()
        print("Botão de voltar clicado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao clicar no botão de voltar: {e}")
        return False

# Função principal
def processar_tweets(driver, max_iteracoes, df_tweets_futebol, count):
    while count < max_iteracoes:
        print(f"Processando tweet {count + 1} de {max_iteracoes}")
        driver.execute_script("window.scrollBy(0, 500);")
        # verificar_e_clicar_retry(driver)
        # Extrai o tweet
        find_tweet(driver, count)
        df_tweets_futebol = extract_tweet(driver, df_tweets_futebol)
        print_dataframe(df_tweets_futebol, "df_tweets_futebol.csv")
        if not clicar_botao_voltar(driver):
            break 
        time.sleep(3)
        count += 1

def verificar_link(driver):
    try:
        # Localiza o botão que contém um span com o texto "Retry"
        botao_retry = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button//div//span[text()="Retry"]'))
        )
        # Clica no botão "Retry"
        botao_retry.click()
        print("Botão 'Retry' encontrado e clicado!")
        return True
    except Exception as e:
        # Se o botão não for encontrado, apenas continua a execução
        return False
    
def verificar_link(driver, url_correta):
    try:
        # Verifica se a URL atual é a correta
        if driver.current_url == url_correta:
            return True
        else:
            print(f"Não está no link correto. URL atual: {driver.current_url}")
            driver.back()
            time.sleep(3)
            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(3)
    except Exception as e:
        print(f"Erro ao verificar o link: {e}")
        return False
    