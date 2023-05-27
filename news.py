from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import json
from time import sleep

class Scraping:
    
    def __init__(self):
        self.browser_configuring ()
        self.start()
        self.pagination()
        self.create_file()
        self.close_Driver()

    def browser_configuring(self):
        self.option = Options()
        self.option.add_argument('-headless')
        self.driver = webdriver.Firefox(options=self.option)

    def start(self):
        self.top10ranking = {}
        self.lisTranking = []
        self.rankings = {
            '3points': {'label': '3PM'},
            'points': {'label': 'PTS'},
            'assistants': {'label': 'AST'},
            'rebounds': {'label': 'REB'},
            'steals': {'label': 'STL'},
            'blocks': {'label': 'BLK'},
        }
        
        # Grab content from URL (Pegar conteúdo HTML a partir da URL)
        self.url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10) # in seconds

        cookie = self.wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        if cookie:
            cookie.click()   
            sleep(2) 

    def field_scraping(self, type):
        label = self.rankings[type]['label']
        
        # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table = soup.find('table', attrs={'class': 'Crom_table__p1iZz'})
    
        # Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
        df_full = pd.read_html(str(table))[0].head(10)
        df = df_full[['Unnamed: 0', 'Player', 'Team', label]]
        df.columns = ['pos', 'player', 'team', label]

        # Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)
        return df.to_dict('records')

    def pagination(self):   
        btn_next = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]')))    
                        
        while True:
            for k in self.rankings:
                self.top10ranking[k] = self.field_scraping(k) 
            self.lisTranking.append([self.top10ranking.copy()])   
        
            if btn_next.get_attribute("disabled") == "true":           
                break
            btn_next.click()                     

    def create_file(self):
        # Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
        with open('ranking.json', 'w', encoding='utf-8') as jp:
            js = json.dumps(self.lisTranking, indent=4)
            jp.write(js)
   
    def close_Driver(self):         
        self.driver.quit()

scraping = Scraping()
