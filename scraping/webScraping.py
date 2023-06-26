from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#FIREFOX
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
#OPERA
from webdriver_manager.opera import OperaDriverManager

class WebScraping():
    
	#Inicializo los atributos (constructor)
	def __init__(self,tipoNavegador):

		self.tipoNavegador=tipoNavegador

		options = Options()
		#options.add_argument('--headless=new')
		options.add_argument('user-data-dir=/C/driver_nav')
		print('aaaaaaaaaaaaaaaaa')
		#self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		self.driver = webdriver.Chrome()
		print('bbbbbbbbbbbbbbb')
		#if tipoNavegador == 'chrome':
		#	options = Options()
		#	options.add_argument('--headless=new')
		#	options.add_argument('user-data-dir=/C/driver_nav')
		#	self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		#if tipoNavegador == 'firefox':
		#	options = FirefoxOptions()
		#	#options.add_argument("--headless")
		#	driver = webdriver.Firefox(options=options)
		#	#self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
		#if tipoNavegador == 'opera':
		#	self.driver = webdriver.Chrome(service=Service(OperaDriverManager().install()), options=options)
		
		#options = FirefoxOptions()
		#options.add_argument("--headless")
		#driver = webdriver.Firefox(options=options)
		#self.driver = driver

	def execute(self, categoriasLista=[]):
		#try:
			#Abrimos el navegador seleccionado y lo maximizamos
			print('ccccccccccccccccc')
			url = "https://admin.fazil.services/application/catalog/taxonomy/categories"
			driver = self.driver
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

			return (categoriasOK,categoriasNOEX)

		#except KeyboardInterrupt:
		#	print("*** Stop web scraping ***")
		#	exit(1)