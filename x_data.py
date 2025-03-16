from imports import *
from config import *
from functions import *

open_page(x_page_futebol)
# click_element(driver, locator="/html/body/div/div[1]/div/div[1]/div[2]/svg", locator_type=By.XPATH)
# # click_element(driver, locator="/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div", locator_type=By.XPATH)

# Email
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input", data=username, locator_type=By.XPATH)
# Avançar 
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]", locator_type=By.XPATH)
# Password
write_data(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input", data=password, locator_type=By.XPATH)
# Entrar
click_element(driver, locator="/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button", locator_type=By.XPATH)