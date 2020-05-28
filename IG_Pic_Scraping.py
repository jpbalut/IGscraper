from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil

class App:
	def __init__(self, username='johnghost33', password='elver123', target_username='dataminer2060', path='/Users/jpbalut/Desktop/web_scrapping_tutorials/instapics', chrome_driver_path='/Users/jpbalut/Desktop/web_scrapping_tutorials/chromedriver'):
		#nacimiento 12 de mayo del 91 y mail yeipi_b1@hotmail.com

		self.username=username
		self.password=password
		self.target_username=target_username
		self.path=path
		self.driver = webdriver.Chrome(chrome_driver_path)
		self.error = False
		self.main_url='https://www.instagram.com'
		sleep(3)
		self.driver.maximize_window()
		self.driver.get(self.main_url)
		self.login()
		if self.error is False:
			self.search_user()
		if self.error is False:
			self.scroll_down()
		if not os.path.exists(path):
			os.mkdir(path)
		self.dl_img()
		sleep(3)
		self.driver.close()

	def write_caption_excel(self, images, caption_path):
		workbook = Workbook(os.path.join(caption_path, 'captions.xlsx'))
		worksheet = workbook.add_worksheet()
		row=0
		worksheet.write(row, 0, 'image_name')
		worksheet.write(row, 1, 'caption')
		row+=1
		for index, image in enumerate(images):
			filename = 'image_' + str(index) +'.jpg'
			try:
				caption = image['alt']
			except KeyError:
				caption = 'No caption found'
			worksheet.write(row, 0, filename)
			worksheet.write(row, 1, caption)
			row+=1


		workbook.close()

	def dl_caption(self, images):
		print('writing on excel...')
		caption_folder_path = os.path.join(self.path, 'captions')
		if not os.path.exists(caption_folder_path):
			os.mkdir(caption_folder_path)
		self.write_caption_excel(images, caption_folder_path)
		"""for index, image in enumerate(images):
			try:
				caption=image['alt']
			except:
				caption='No Caption Exists'
			file_name = 'caption_'+str(index)+'.txt'
			file_path = os.path.join(caption_folder_path, file_name)
			link = image['src']
			with open(file_path, 'wb') as file:
				file.write(str('link: ' + str(link) + '\n' + 'caption: ' + caption).encode())"""


	def dl_img(self):
		soup = BeautifulSoup(self.driver.page_source, 'lxml')
		all_images=soup.find_all('img')
		print(all_images)
		self.dl_caption(all_images)
		print('length of all images', len(all_images))
		for index, image in enumerate(all_images):
			filename = 'image_' + str(index) +'.jpg'
			#imagepath = self.path+'/'+filename
			image_path=os.path.join(self.path, filename)
			link=image['src']
			print('Downloading Image ', index, image)
			try:
				response = requests.get(link, stream=True)
			except Exception:
				print('cant download', index, image)
			try:
				with open(image_path, 'wb') as file:
					shutil.copyfileobj(response.raw, file)
			except Exception as e:
				print(e)
				print('Could not download image ', index)
				print('Image Link: ', link)


	def scroll_down(self):
		try:
			n_of_posts = self.driver.find_element_by_xpath("//span[@class='g47SY ']")
			n_of_posts = str(n_of_posts.text).replace(',','')
			self.n_of_posts = int(n_of_posts)
			if self.n_of_posts>12:
				n_of_scrolls = int(self.n_of_posts/12) + 3
				try:
					for value in range(n_of_scrolls):
						self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
						sleep(3)
				except Exception as e:
					self.error = True
					print(e)
					print('Error while scrolling down')
		except Exception:
			self.error = True
			print('Unable to find number of post while scrolling down')

	def search_user(self,):
		sleep(5)
		try:
			self.driver.find_element_by_xpath("//input[contains(@class,'XTCLo')]").send_keys(self.target_username)
			target_profile_url = self.main_url + '/' + self.target_username + '/'
			self.driver.get(target_profile_url)
			sleep(3)
		except Exception as e:
			self.error = True
			print(e)
			print('Unable to find Searchbox')
		sleep(3)

	def login(self,):
		sleep(2)
		try:
			self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(self.username)
			self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(self.password)
			self.driver.find_element_by_xpath("//button[@type=\"submit\"]").click()
		except Exception as e:
			self.error = True
			print(e)
			print('Unable to find Log In button or Username/password input bar')
		try:
			sleep(2)
			self.driver.find_element_by_xpath("//button[text()='Not Now']").click()
		except Exception:
			pass

if __name__ == '__main__':
	app=App()