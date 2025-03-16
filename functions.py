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
        except ElementNotInteractableException:
            print(f"Elemento não interagível: {locator}. Tentativa {tentativa + 1} de {max_tentativas}.")
        time.sleep(delay)
    
    print(f"Falha ao escrever dados no elemento após {max_tentativas} tentativas.")
    return False  


def find_tweet(driver, count):
    """
    Encontra o tweet na posição `count` e clica na div do texto do tweet.

    Args:
        driver: Instância do WebDriver do Selenium.
        count (int): O índice do tweet a ser encontrado.

    Returns:
        bool: True se o tweet foi encontrado, False caso contrário.
    """
    try:
        # Encontra o tweet na posição `count` (article com data-testid="tweet")
        wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
        tweet = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]')))[count]
        print(f"Tweet {count + 1} encontrado!")

        # Encontra a div com data-testid="tweetText" dentro do tweet
        div_texto_tweet = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
        print("Div do texto do tweet encontrada! Clicando na div...")
        div_texto_tweet.click()  # Clica na div do texto do tweet
        return True
    except Exception as e:
        print(f"Erro ao interagir com o tweet {count + 1}: {e}")
        return False

def extract_tweets(driver, df_tweets=None):
    """
    Extrai tweets de uma página do Twitter e atualiza um DataFrame existente.

    Args:
        driver: Instância do WebDriver do Selenium.
        df_tweets (pd.DataFrame): DataFrame existente para ser atualizado. Se None, cria um novo.

    Returns:
        pd.DataFrame: DataFrame atualizado com os novos tweets.
    """
    try:
        # Encontra todas as divs com data-testid="tweetText"
        wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
        tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))

        # Se nenhum DataFrame for fornecido, cria um novo
        if df_tweets is None:
            df_tweets = pd.DataFrame(columns=["Tipo", "Texto"])

        # Lista para armazenar os novos tweets
        novos_tweets = []

        # Extrai o tweet principal (primeiro tweet)
        if tweets:
            tweet_principal = tweets[0].find_element(By.XPATH, './/span').text
            novos_tweets.append({"Tipo": "Principal", "Texto": tweet_principal})  # Adiciona o tweet principal

            # Extrai os tweets relacionados (todos os tweets após o primeiro)
            for tweet in tweets[1:]:  # Itera a partir do segundo tweet
                try:
                    span_texto = tweet.find_element(By.XPATH, './/span')
                    texto = span_texto.text
                    novos_tweets.append({"Tipo": "Relacionado", "Texto": texto})  # Adiciona o tweet relacionado
                except Exception as e:
                    print(f"Erro ao extrair texto de um tweet relacionado: {e}")

        # Converte a lista de novos tweets em um DataFrame
        df_novos_tweets = pd.DataFrame(novos_tweets)

        # Atualiza o DataFrame existente com os novos tweets
        df_tweets = pd.concat([df_tweets, df_novos_tweets], ignore_index=True)

        # Exibe o DataFrame atualizado
        print("DataFrame atualizado:")
        print(df_tweets)

        return df_tweets

    except Exception as e:
        print(f"Erro ao encontrar os tweets: {e}")
        return df_tweets

    finally:
        # Aguarda alguns segundos para visualizar o resultado
        time.sleep(5)

def print_dataframe(df_tweets):
    # Exibe o DataFrame final
    if df_tweets is not None:
        print("DataFrame final:")
        print(df_tweets)

        # Salva o DataFrame em um arquivo CSV (opcional)
        df_tweets.to_csv("tweets.csv", index=False, encoding="utf-8")
        print("DataFrame salvo em 'tweets.csv'.")