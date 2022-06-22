
from selenium import webdriver
from time import sleep
import os

idx = 0

directoryPath = os.getcwd()
f = open("images/input.txt","w")

driver = webdriver.Firefox(executable_path=directoryPath + "/geckodriver")

while(os.path.exists('htmls/map' + str(idx) + '.html')):
	print("image number", idx)
	filePath = 'file://' + directoryPath + '/htmls/map' + str(idx) + '.html'
	driver.get(filePath)
	if idx == 0:
		sleep(1)
	sleep(1)
	driver.get_screenshot_as_file('images/out' + str(idx) + '.png')
	f.write("file 'out'" + str(idx) + "'.png'\nduration 0.2\n")
	idx += 1

f.close()
driver.quit()
# print("images generated...")