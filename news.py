from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import json
from time import sleep

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"

top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}

def buildrank(type):

    field = rankings[type]['field']
    label = rankings[type]['label']
    
    #btn_element = driver.find_element(By.XPATH, f"//div[@class='Crom_container__C45Ti crom-container']//table//thead//tr//th[@field='{field}']")
    btn_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@class='Crom_container__C45Ti crom-container']//table//thead//tr//th[@field='{field}']")))
    wait.until(EC.invisibility_of_element_located((By.ID, "onetrust-group-container")))
    btn_element.click()

    # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', attrs={'class': 'Crom_table__p1iZz'})
   
    # Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'Player', 'Team', label]]
    df.columns = ['pos', 'player', 'team', 'TOTAL']

    # Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)
    return df.to_dict('records')


option = Options()
option.headless = True
driver = webdriver.Firefox(options=option)

driver.get(url)
wait = WebDriverWait(driver, 10) # in seconds

cookie = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
if cookie:
    cookie.click()
    sleep(3)

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)