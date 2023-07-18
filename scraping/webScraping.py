from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.selenium_manager import SeleniumManager
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#FIREFOX
#from selenium.webdriver.firefox.service import Service as FirefoxService
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.options import Options as FirefoxOptions
#OPERA
#from webdriver_manager.opera import OperaDriverManager
import os

class WebScraping():
    
	#Inicializo los atributos (constructor)
	def __init__(self,tipoNavegador):

		self.tipoNavegador=tipoNavegador
		options = Options()
		#options.add_argument('--headless=new')
		#options.add_argument('--disable-dev-shm-usage')
		#options.add_argument('user-data-dir=/C/driver_nav')

		#service = Service('./driver_nav/chromedriver')
		#service = Service('/app/.chromedriver/bin/chromedriver')
		
		#self.driver = webdriver.Chrome(service=service, options=options)

		#url = "https://admin.fazil.services/application/catalog/taxonomy/categories"
		#self.driver.get(url)
		#time.sleep(5)

		#service = Service(executable_path=os.path.dirname+'/driver_nav/chromedriver')
		#self.driver = webdriver.Chrome(service=service)
		#self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		
		#self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		#cPath = SeleniumManager.driver_location("/path/to/binary/chromedriver",options=options)
		#self.driver = webdriver.Chrome(cPath)
		self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
		time.sleep(5)
		#driver = webdriver.Chrome('C:\driver_nav\chromedriver')

	def execute(self, categoriasLista=[]):
		#try:
			#PRIMERA FORMA
			#options = Options()
			#options.add_argument('--headless=new')
			#options.add_argument('user-data-dir=/C/driver_nav')
			#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
			#SEGUNDA FORMA MOODO
			#	No se puede obtener chromedriver usando Selenium Manager;
			#driver = webdriver.Chrome(options=options)
			#TERCERA FORMA
			#webdriver.Chrome('C:\driver_nav\chromedriver.exe')
			#CUARTA FORMA
			#webdriver.Chrome('.\chromedriver.exe')
			#QUINTA FORMA
			#driver_path = '.\chromedriver'
			
			#service = ChromeService(executable_path=driver_path)
			#service = Service()
			#options = webdriver.ChromeOptions()
			#driver = webdriver.Chrome(service=service, options=options)

			#SEXTA FORMA
			#driver = webdriver.Chrome()
			url = "https://admin.fazil.services/application/catalog/taxonomy/categories"
			self.driver.get(url)

			#Concatenamos los valores rescatados
			categoriasOK = []
			categoriasNOEX = []
			deeplinkCat = "CATEGORIA: "
			deeplinkId = "ID: "
			deeplinkEstado = "Estado: "
			deeplinkUrl = "DL: https://api.test.tottus.cl/categories?name=&id=&landingtonewPLP=true&defaultSelectParentId=&defaultSortBy=Recomendados"

			deeplink = deeplinkCat+'\n'+deeplinkId+'\n'+deeplinkEstado+'\n'+deeplinkUrl+'\n \n'
			categoriasOK.append(deeplink)
			
			"""
			url = "https://admin.fazil.services/application/catalog/taxonomy/categories"
			#driver = self.driver
			driver.maximize_window()
			driver.get(url)
			time.sleep(5)

			#Hacemos click al boton para ingresar a la plataforma y nos ubicamos en la ventana Catálogo
			button = driver.find_element(By.CLASS_NAME, 'nice-button')
			button.click()
			time.sleep(7)

			#Ingresamos al iframe de la pestaña Catálogo
			driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))

			i = 0
			categoriasOK = []
			categoriasNOEX = []
			for item in categoriasLista:
				#Ingresamos el valor a buscar en el input
				inputsearch = driver.find_element(By.ID, 'search-category')
				inputsearch.send_keys(item)
				time.sleep(5)

				if i == 0:
					#Seleccionamos del select las categorias a buscar el campo ingresado
					driver.find_element(By.XPATH, "//div[text()='Ver nivel por nivel']").click()
					driver.find_element(By.XPATH, "//div[text()='Ver todas las categorías']").click()
					i += 1
					time.sleep(5)

				#Ubicamos dentro de la tabla los elementos que se necesitan
				catIdHijo = item
				try:
					categoria = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[2]').text
				except NoSuchElementException:
					categoriasNOEX.append(catIdHijo)
					inputsearch.send_keys(Keys.BACK_SPACE)
					inputsearch.send_keys(Keys.CONTROL + Keys.BACKSPACE)
					pass
				else:	
					catIdEstado = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[3]/div').text
					catIdPadre = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[5]').text
					idPadrePosInicial = catIdPadre.find("(") + 1
					idPadrePosFinal = catIdPadre.find(")")
					categoriaClear = categoria.replace(' ','')

					#Concatenamos los valores rescatados
					deeplinkCat = "Categoría: " + categoria
					deeplinkId = "ID: " + catIdHijo
					deeplinkEstado = "Estado: " + catIdEstado
					deeplinkUrl = "DL: https://api.test.tottus.cl/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]+"&defaultSortBy=Recomendados"

					inputsearch.send_keys(Keys.BACK_SPACE)
					inputsearch.send_keys(Keys.CONTROL + Keys.BACKSPACE)
					deeplink = deeplinkCat+'\n'+deeplinkId+'\n'+deeplinkEstado+'\n'+deeplinkUrl+'\n \n'
					categoriasOK.append(deeplink)
					time.sleep(5)
			"""
			return (categoriasOK,categoriasNOEX)

		#except KeyboardInterrupt:
		#	print("*** Stop web scraping ***")
		#	exit(1)