from imports import *
from config import *
from functions import *

open_page(x_page_futebol)

######################################################################################## LOGIN ########################################################################################

# Email
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input", data=email, locator_type=By.XPATH)
# Avançar 
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]", locator_type=By.XPATH)
# # Username
# write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input", data=username, locator_type=By.XPATH)
# Avançar 
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button", locator_type=By.XPATH)
# Password
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input", data=password, locator_type=By.XPATH)
# Entrar
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button", locator_type=By.XPATH)

######################################################################################## DATA FUTEBOL ########################################################################################

driver.maximize_window()
time.sleep(10)

df_tweets_futebol = pd.DataFrame(columns=["Tipo", "Texto", "Chave"])

max_iteracoes = 500 # lembrar que a qtde de tweets extraidos é max_iteracoes*5
count = 0  

iteracoes = 0
for i in range(max_iteracoes):
    for count in range(4):  # Removido 'count = 0'
        try:
            iteracoes += 1
            print(f"Processando tweet {iteracoes} de {max_iteracoes}")
            verificar_e_clicar_retry(driver)
            verificar_link(driver, x_page_futebol)
            find_tweet(driver, count)
            
            df_tweets_futebol = extract_tweet(driver, df_tweets_futebol, iteracoes)
            
            # Verificar se o df_tweets_futebol não está vazio antes de salvar
            if not df_tweets_futebol.empty:
                print_dataframe(df_tweets_futebol, "df_tweets_futebol.csv")
            else:
                print(f"DataFrame vazio após a coleta do tweet {iteracoes}.")
            
            fechar_aba_e_retornar_para_main(driver)
            verificar_e_clicar_retry(driver)

            time.sleep(3)
        except Exception as e:
            print(f"Erro durante o processamento do tweet {iteracoes}: {e}")
            continue  # Continuar para o próximo tweet mesmo em caso de erro
        print(driver)

    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 5000);")
    time.sleep(3)  # Esperar após rolar a página
    verificar_e_clicar_retry(driver)



# ######################################################################################## DATA POLITICA ########################################################################################

# open_page(x_page_politica)

# driver.maximize_window()
# driver.execute_script("document.body.style.zoom='70%'")
# time.sleep(10)


# df_tweets_politica = pd.DataFrame(columns=["Tipo", "Texto"])

# max_iteracoes = 3000 
# count = 0  

# while count < max_iteracoes:
#     print(f"Processando tweet {count + 1} de {max_iteracoes}")

#     find_tweet(driver, count)
#     df_tweets_politica = extract_tweet(driver, df_tweets_politica)

#     print_dataframe(df_tweets_politica)

#     # Volta para a timeline (clica no botão "Back")
#     click_element(
#         driver,
#         locator='//*[@aria-label="Back"]', 
#         locator_type=By.XPATH
#     )
#     time.sleep(3)
#     count += 1