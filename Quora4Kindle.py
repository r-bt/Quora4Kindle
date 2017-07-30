from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import sys, time, glob, pdb

#Get templates
page = open("templates/page.html", "r").read()
contents = open("templates/contents.html", "r").read()

#Setup chrome web browser
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=" + os.getcwd() + "/selenium")
driver = webdriver.Chrome(chrome_options=options)

driver.get("http://www.quora.com")

time.sleep(5)

i = 0
links = ""
questionsNum = 30

if(len(driver.find_elements_by_class_name("logged_out")) == 0):
	currentQs = driver.find_elements_by_class_name("AnswerStoryBundle")
	
	while len(currentQs) < questionsNum:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		currentQs = driver.find_elements_by_class_name("AnswerStoryBundle")
		print(len(currentQs))
	
	for answer in currentQs:
		titleSpan = answer.find_elements_by_class_name("question_text")[0]
		time.sleep(0.5)
		title = titleSpan.find_elements_by_class_name("rendered_qtext")[0].get_attribute("innerHTML")
		#Click more link
		moreLink = answer.find_elements_by_class_name("more_link")[0]
		driver.execute_script("return arguments[0].scrollIntoView();", moreLink)
		time.sleep(0.5)
		driver.execute_script("window.scrollBy(0, -70);")
		moreLink.click()
		time.sleep(2.25)
		#Get answer content
		answerTextDiv = answer.find_elements_by_class_name("ExpandedAnswer")
		while answerTextDiv == []:
			time.sleep(0.5)
			answerTextDiv = answer.find_elements_by_class_name("ExpandedAnswer")
		answerText = answerTextDiv[0].find_elements_by_class_name("rendered_qtext")[0].text
		#Get the author
		username = answer.find_elements_by_class_name("feed_item_answer_user")[0].text
		#Create a page
		questionPage = page
		questionPage = questionPage.replace("{{ TITLE }}", title)
		questionPage = questionPage.replace("{{ CONTENT }}", answerText)
		questionPage = questionPage.replace("{{ AUTHOR }}", username)
		ebookPage = open(str(i) + ".html", "a")
		ebookPage.write(questionPage.encode("utf8"))
 		ebookPage.close()
		#Create contents link
		link = "<li><a href='" + str(i) + ".html'>" + title + "</a></li>"
		links += link
		i = i + 1
	#Create contents page
	contentsPage = contents
	contentsPage = contentsPage.replace("{{ CONTENTS }}", links)
	ebookPage = open("contents.html", "a")
	ebookPage.write(contentsPage.encode("utf-8"))
	ebookPage.close()
	#Create the ebook
	date = time.strftime("%d-%m-%Y")
	os.system('ebook-convert contents.html "Quora:' + str(date) + '.mobi"')
	os.system('ebook-meta --authors Quora4Kindle --title "Quora:' + str(date) +  '" "Quora:' + str(date) + '.mobi"')
	files = glob.glob("*.html")
	for file in files:
		os.remove(file)
	
		
		
		