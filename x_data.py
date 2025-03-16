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


df_tweets = pd.DataFrame(columns=["Tipo", "Texto"])

max_iteracoes = 5 
count = 0  

while count < max_iteracoes:
    print(f"Processando tweet {count + 1} de {max_iteracoes}")

    find_tweet(driver, count)
    df_tweets = extract_tweet(driver, df_tweets)

    print_dataframe(df_tweets)

    # Volta para a timeline (clica no botão "Back")
    click_element(
        driver,
        locator='//*[@aria-label="Back"]',  # XPath para o botão "Back"
        locator_type=By.XPATH
    )

    # Aguarda o carregamento da timeline
    time.sleep(3)

    # Incrementa o contador para processar o próximo tweet
    count += 1