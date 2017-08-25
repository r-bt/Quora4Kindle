#Import dependencies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import sys, time, glob, pdb

#Load our template files
pageTemplate = open("templates/page.html", "r").read()
contentsTemplate = open("templates/contents.html", "r").read()

class Quora4Kindle():
	
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument("user-data-dir={0}/selenium".format(os.getcwd()))
		self.driver = webdriver.Chrome(chrome_options=options)
		self.driver.get("http://www.quora.com")
		
	def createPage(self, title, content, username, pageName):
		questionPage = pageTemplate
		questionPage = questionPage.replace("{{ TITLE }}", title)
		questionPage = questionPage.replace("{{ CONTENT }}", content)
		questionPage = questionPage.replace("{{ AUTHOR }}", username)
		ebookPage = open(str(pageName) + ".html", "a")
		ebookPage.write(questionPage.encode("utf8"))
		ebookPage.close()
		
	def createContentsPage(self, contents):
		contentsPage = contentsTemplate
		contentsPage = contentsPage.replace("{{ CONTENTS }}", contents)
		ebookPage = open("contents.html", "a")
		ebookPage.write(contentsPage.encode("utf-8"))
		ebookPage.close()
	
	def getFeed(self, numOfQuestions):
		#Setup varibles
		links = ""
		i = 0
		#Scroll down the page until the numOfQuestions is exceded
		questions = self.driver.find_elements_by_class_name("AnswerFeedStory")
		while len(questions) < numOfQuestions:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			questions = self.driver.find_elements_by_class_name("AnswerFeedStory")
		#Extract the necessary information from each question
		for question in questions:
			titleSpan = question.find_elements_by_class_name("question_text")[0]
			title = titleSpan.find_elements_by_class_name("rendered_qtext")[0].text
			#Click the more link to expand the answer fully
			moreLink = question.find_elements_by_class_name("more_link")[0]
			self.driver.execute_script("return arguments[0].scrollIntoView();", moreLink)
			while not moreLink.is_displayed():
				pass
			self.driver.execute_script("window.scrollBy(0, -70);")
			moreLink.click()
			#Get the content of the answer
			answerTextDiv = question.find_elements_by_class_name("ExpandedAnswer")
			while answerTextDiv == []:
				time.sleep(0.5)
				answerTextDiv = question.find_elements_by_class_name("ExpandedAnswer")
			answerText = answerTextDiv[0].find_elements_by_class_name("rendered_qtext")[0].text
			#Get the username
			username = question.find_elements_by_class_name("feed_item_answer_user")[0].text
			#Create a page
			self.createPage(title, answerText, username, str(i))
 			#Add contents link
 			link = "<li><a href='" + str(i) + ".html'>" + title + "</a></li>"
			links += link
			i = i + 1
 		self.createContentsPage(links)	
 		#Create the ebook
 		date = time.strftime("%d-%m-%Y")
		os.system('ebook-convert contents.html "Quora:' + str(date) + '.mobi"')
		os.system('ebook-meta --authors Quora4Kindle --title "Quora:' + str(date) +  '" "Quora:' + str(date) + '.mobi"')
		files = glob.glob("*.html")
		for file in files:
			os.remove(file)

scraper = Quora4Kindle()
scraper.getFeed(17)

pdb.set_trace()
		