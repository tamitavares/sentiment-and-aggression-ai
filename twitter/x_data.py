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

######################################################################################## DATA FUTEBOL ########################################################################################

driver.maximize_window()
time.sleep(10)

df_tweets_futebol = pd.DataFrame(columns=["Tipo", "Texto", "Chave"])

max_iteracoes = 20 
count = 0  

# while count < max_iteracoes:
#     driver.execute_script("window.scrollBy(0, 2000);")
#     verificar_e_clicar_retry(driver)
#     count += 1    

# count = 0 
# while count < max_iteracoes:
#     print(f"Processando tweet {count + 1} de {max_iteracoes}")
#     # driver.execute_script("document.body.style.zoom='70%'")

#     verificar_e_clicar_retry(driver)
#     verificar_link(driver, x_page_futebol)
    
#     find_tweet(driver, count)
#     df_tweets_futebol = extract_tweet(driver, df_tweets_futebol)
#     fechar_aba_e_retornar_para_main(driver)
#     verificar_e_clicar_retry(driver)

#     print_dataframe(df_tweets_futebol,"df_tweets_futebol.csv")

#     # Volta para a timeline (clica no botão "Back")
#     # click_element(
#     #     driver,
#     #     locator='//*[@aria-label="Back"]', 
#     #     locator_type=By.XPATH
#     # )
#     time.sleep(3)
#     # driver.execute_script("window.scrollBy(0, 1500);")
#     count += 1
iteracoes = 0
for i in range(max_iteracoes):
    for count in range(5):  # Removido 'count = 0'
        print(f"Processando tweet {i+1} de {max_iteracoes}")
        iteracoes += 1
        verificar_e_clicar_retry(driver)
        verificar_link(driver, x_page_futebol)
        find_tweet(driver, count)
        
        df_tweets_futebol = extract_tweet(driver, df_tweets_futebol, iteracoes)
        
        fechar_aba_e_retornar_para_main(driver)
        verificar_e_clicar_retry(driver)

        print_dataframe(df_tweets_futebol, "df_tweets_futebol.csv")
        time.sleep(3)

    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 5000);")
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