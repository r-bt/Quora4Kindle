from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import sys, time, glob


#Ebook pages
contentsPage = '<html><body><h1>Table of Contents</h1><p style="text-indent:0pt"><ol>{{ Contents }}</ol></p></body></html>'
ebookPage = "<html><head></head><body><h1>{{ TITLE }}</h1><p>{{ CONTENT }}</p><p>By {{ AUTHOR }}</p></body></html>"

#Varibles
QuoraAnswers = []
i = 0
links = ""
questionsNum = 50

#Selenium
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/richard/Google\ Drive/Programming/Programing/Launguages/Python/QuoraKindle")
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://www.quora.com")

time.sleep(5)
#Get all the answers
while len(driver.find_elements_by_class_name("feed_type_answer")) < questionsNum:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

answers = driver.find_elements_by_class_name("feed_type_answer")

for answer in answers:
	#Get the question title
	titleDiv = answer.find_elements_by_class_name("question_text")[0]
	title = titleDiv.find_elements_by_class_name("rendered_qtext")[0].get_attribute("innerHTML")
	print(title)
	#Click more link
	moreLink = answer.find_elements_by_class_name("more_link")[0]
	driver.execute_script("return arguments[0].scrollIntoView();", moreLink)
	time.sleep(0.5)
	driver.execute_script("window.scrollBy(0, -70);")
	clicked = False
	while clicked == False:
		try:
			moreLink.click()
			clicked = True
		except:
			pass
	time.sleep(3)
	#Get the answer
	displayedAnswer = driver.find_element_by_css_selector(".feed_desktop_modal:not(.hidden)")
	#Close 
	closeLink = displayedAnswer.find_elements_by_class_name("modal_fixed_close")
	closeLink[0].click()
	#Get the answers content
	expandedQ = displayedAnswer.find_elements_by_class_name("ExpandedAnswerInFeed")
	questionHTML = expandedQ[0].find_elements_by_class_name("rendered_qtext")[0].text
	#Get the author
	author = displayedAnswer.find_elements_by_class_name("user")
	time.sleep(0.5)
	#Print details
	content = ebookPage
	content = content.replace("{{ TITLE }}", title)
	content = content.replace("{{ CONTENT }}", questionHTML)
	try:
		writer = author[0].get_attribute("innerHTML")
	except:
		write = "Anoanonymous"
	content = content.replace("{{ AUTHOR }}", writer)
	link = "<li><a href='" + str(i) + ".html'>" 	+ title + "</a></li>"
	links += link
	page = open(str(i) + ".html", "a")
	page.write(content.encode("utf8"))
	page.close()
	i = i + 1
	print("---------------------------------------------------------------------------")
	
contentsPage = contentsPage.replace("{{ Contents }}", links)
page = open("contents.html", "w")
page.write(contentsPage.encode("utf8"))
page.close()

date = time.strftime("%d-%m-%Y")
os.system('ebook-convert contents.html "Quora:' + str(date) + '.mobi"')
os.system('ebook-meta --authors Quora4Ebook --title "Quora:' + str(date) +  '" "Quora:' + str(date) + '.mobi"')
files = glob.glob("*.html")
for file in files:
	os.remove(file)

	
