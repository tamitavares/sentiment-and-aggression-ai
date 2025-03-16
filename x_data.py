from imports import *
from config import *
from functions import *

open_page(x_page_futebol)

######################################################################################## LOGIN ########################################################################################

# Email
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input", data=email, locator_type=By.XPATH)
# Avançar 
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]", locator_type=By.XPATH)
# Username
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input", data=username, locator_type=By.XPATH)
# Avançar 
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button", locator_type=By.XPATH)
# Password
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input", data=password, locator_type=By.XPATH)
# Entrar
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button", locator_type=By.XPATH)

######################################################################################## DATA ########################################################################################

driver.maximize_window()
driver.execute_script("document.body.style.zoom='70%'")
time.sleep(10)

# Encontra o primeiro tweet (article com data-testid="tweet")
try:
    wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
    tweet = wait.until(EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]')))
    print("Tweet encontrado!")

    # Encontra a div com data-testid="tweetText" dentro do tweet
    div_texto_tweet = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
    print("Div do texto do tweet encontrada! Clicando na div...")
    div_texto_tweet.click()  # Clica na div do texto do tweet
except Exception as e:
    print(f"Erro ao interagir com o tweet: {e}")

time.sleep(5)

# Encontra todas as divs com data-testid="tweetText"
try:
    wait = WebDriverWait(driver, 10)  # Espera até 10 segundos
    tweets = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))

    # Lista para armazenar os textos dos tweets
    array_final = []

    # Extrai o tweet principal (primeiro tweet)
    if tweets:
        tweet_principal = tweets[0].find_element(By.XPATH, './/span').text
        array_final.append(tweet_principal)  # Adiciona o tweet principal ao array

        # Extrai os tweets relacionados (todos os tweets após o primeiro)
        tweets_relacionados = []
        for tweet in tweets[1:]:  # Itera a partir do segundo tweet
            try:
                span_texto = tweet.find_element(By.XPATH, './/span')
                texto = span_texto.text
                tweets_relacionados.append(texto)  # Adiciona o texto à lista de tweets relacionados
            except Exception as e:
                print(f"Erro ao extrair texto de um tweet relacionado: {e}")

        array_final.append(tweets_relacionados)  # Adiciona a lista de tweets relacionados ao array

    # Exibe o array final
    print("Array final:")
    print(array_final)

except Exception as e:
    print(f"Erro ao encontrar os tweets: {e}")

# Aguarda alguns segundos para visualizar o resultado
time.sleep(5)