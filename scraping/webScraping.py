from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.selenium_manager import SeleniumManager
#Require installar: > pip3 install webdriver_manager
#Descargamos el chromedriver (con la version del chrome actual de la web driver) y la enviamos a la ruta  --->  $ cp chromedriver /usr/local/bin
from webdriver_manager.chrome import ChromeDriverManager   
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time
import os
#En la consola  : python3 manage.py runserver 
#En el navegador: http://127.0.0.1:8000
#Web driver     : https://googlechromelabs.github.io/chrome-for-testing/
#                 chromedriver	   mac-x64	       https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/mac-x64/chromedriver-mac-x64.zip	     200 (descargamos)
#                 >cd /usr/local/bin    luego   > sudo mv chromedriver /usr/local/bin/
#Version navegador: Version 127.0.6533.120 (Official Build) (x86_64)
#En el input    : CATG10197,CATG24316,CATG20279,CATG20268,CATG24462

class WebScraping():
    
	#Inicializo los atributos (constructor)
	def __init__(self,tipoNavegador):

		try:
			self.tipoNavegador=tipoNavegador
			options = webdriver.ChromeOptions()
			#Inicialice el navegador chrome Maximize
			options.add_argument("--start-maximized")
			options.add_argument("--disable-extensions")
			#Con esto se habilita en el chrome el history (podemos ir a validar ingresando nexflit la proxima ingresa directo) - https://www.youtube.com/watch?v=A3C39PRfV2I
			options.add_argument('user-data-dir=/Applications/MAMP/htdocs/djangoScrapingIds/djangoScrapingIds/driver_nav/')
			#No veríamos cómo se abre un navegador y empieza a iterar por las páginas. Se ejecutaría en segundo plano
			#options.add_argument('--headless=new')
			#Le enviamos directo el options y ya no la ruta del driver ya que lo lee desde el bin directo sin necesidad de indicar lo
			self.driver = webdriver.Chrome(options=options)
		except Exception as error:
			print("Ha ocurrido un error con el driver del navegador:", type(error).__name__, "–", error)

	def execute(self, categoriasLista=[],tipoUrl=''):
		try:

			url = "https://admin.fazil.services/application/catalog/taxonomy/categories"
			driver = self.driver
			driver.get(url)
			#self.driver.get(url)
			#time --> Tiempo de espera antes de cerrar navegador
			#time.sleep(5)

			#Hacemos click al boton para ingresar a la plataforma y nos ubicamos en la ventana Catálogo
			button = WebDriverWait(driver, 5).until(
				EC.element_to_be_clickable((By.CLASS_NAME, "nice-button"))
			)
			#button = driver.find_element(By.CLASS_NAME, 'nice-button')
			button.click()
			time.sleep(3)

			#Ingresamos al iframe de la pestaña Catálogo
			#print('111111')
			WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"extension-iframe")))
			#driver.switch_to.frame(driver.find_element(By.ID, "extension-iframe"))
			#driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
			#switch = WebDriverWait(driver, 5).until(
			#	EC.presence_of_element_located((By.ID,"extension-iframe"))
			#)
			#driver.switch_to.frame(switch)
			#print('2222222')
			#Remover sleep al final
			#time.sleep(55)

			print("aaaaa")
			print(tipoUrl)
			print("bbbbb")
			
			i = 0
			categoriasOK = []
			categoriasNOEX = []
			deeplink = ''
			deeplinkUrl = ''
			for item in categoriasLista:

				if i == 0:
					#Seleccionamos del select las categorias a buscar el campo ingresado
					#driver.find_element(By.XPATH, "//div[text()='Ver nivel por nivel']").click()
					#driver.find_element(By.XPATH, "//div[text()='Ver todas las categorías']").click()
					selectOption = WebDriverWait(driver, 5).until(
						EC.element_to_be_clickable((By.XPATH, "//div[text()='Ver nivel por nivel']"))
					)
					selectOption.click()
					driver.find_element(By.XPATH, "//div[text()='Ver todas las categorías']").click()
					i += 1
					#time.sleep(3)
				else:
					for j in range(1, 10):
						driver.find_element(By.ID, 'search-category').send_keys(Keys.LEFT)
						driver.find_element(By.ID, 'search-category').send_keys(Keys.DELETE)

				#Ingresamos el valor a buscar en el input
				#print(item)
				inputsearch = WebDriverWait(driver, 5).until(
					EC.presence_of_element_located((By.ID, "search-category"))
				)
				inputsearch.click()
				inputsearch.send_keys(item)
				#time.sleep(2)
				#driver.find_element(By.ID, 'search-category').send_keys(item)
				time.sleep(2)
				
				#Ubicamos dentro de la tabla los elementos que se necesitan
				catIdHijo = item
				try:
					categoria = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[2]').text
				except NoSuchElementException:
					categoriasNOEX.append(catIdHijo)
					#inputsearch.send_keys(Keys.BACK_SPACE)
					#inputsearch.send_keys(Keys.CONTROL + Keys.BACKSPACE)
					pass
				else:	
					catIdEstado = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[3]/div').text
					catIdPadre = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div/div/div[4]/div[2]/table/tbody/tr[1]/td[5]').text
					idPadrePosInicial = catIdPadre.find("(") + 1
					idPadrePosFinal = catIdPadre.find(")")
					categoriaClear = categoria.replace(' ','')
					#time.sleep(5)
					#Concatenamos los valores rescatados

					if (tipoUrl == 'api'):
						deeplinkUrl = "https://api.test.tottus.cl/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]+"&defaultSortBy=Recomendados"
						#deeplinkUrl = "https://api.test.tottus.cl/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]
						deeplink = deeplinkUrl+'\n'
					elif (tipoUrl == 'excel'):
						#deeplinkCat = "Nombre: " + categoria
						deeplinkCat = categoria
						#print(deeplinkCat)
						deeplinkUrl = deeplinkCat+'\n'+"https://www.tottus.com/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]+"&defaultSortBy=Recomendados"
						#deeplink = deeplinkUrl+'\n \n'
						deeplink = deeplinkUrl+'\n'
					elif (tipoUrl == 'deeplink'):
						deeplinkCat = "Categoría: " + categoria
						deeplinkId = "ID: " + catIdHijo
						#deeplinkEstado = "Estado: " + catIdEstado
						deeplinkUrl = "https://www.tottus.com/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]+"&defaultSortBy=Recomendados"
						#deeplink = deeplinkCat+'\n'+deeplinkId+'\n'+deeplinkEstado+'\n'+deeplinkUrl+'\n \n'
						deeplink = deeplinkCat+'\n'+deeplinkId+'\n'+deeplinkUrl+'\n \n'
					elif (tipoUrl == 'web'):
						deeplinkId = "ID: " + catIdHijo
						deeplinkUrl = "https://www.tottus.cl/tottus-cl/lista/"+catIdHijo+"/"+categoria.replace(' ','-')
						deeplink = deeplinkId+'\n'+deeplinkUrl+'\n \n'
					else:
						#deeplinkCat = "Nombre: " + categoria
						#deeplinkUrl = deeplinkCat+'\n'+"https://www.tottus.com/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]+"&defaultSortBy=Recomendados"
						#deeplink = deeplinkUrl+'\n \n'
						deeplinkUrl = "https://api.test.tottus.cl/categories?name="+categoriaClear.replace(',','')+"&id="+catIdHijo+"&landingtonewPLP=true&defaultSelectParentId="+catIdPadre[idPadrePosInicial:idPadrePosFinal]+"&defaultSortBy=Recomendados"
						deeplink = deeplinkUrl+'\n'
					
					categoriasOK.append(deeplink)
					#print(categoriasOK)
					time.sleep(2)
			
			return (categoriasOK,categoriasNOEX)

		except KeyboardInterrupt:
			print("*** Stop web scraping ***")
			exit(1)