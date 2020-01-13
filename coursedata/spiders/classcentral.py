# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from selenium import webdriver
from time import sleep
from coursedata.items import Course


class ClasscentralSpider(Spider):
	name = 'classcentral'
	allowed_domains = ['www.classcentral.com']
	start_urls = ['https://www.classcentral.com/subjects']

	def parse(self, response):
		subject_urls = response.xpath('//*[@class = "text--blue"]/@href').extract()
		
		#Crawl through all subjects
		for subject_url in subject_urls:
			absolute_subject_url = response.urljoin(subject_url)
			
			#Click on load courses
			driver = webdriver.Chrome('C:\ProgramData\Anaconda3\Lib\webdrivers\chromedriver')
			driver.get(absolute_subject_url)
			
			next_bttn = driver.find_element_by_xpath('//*[@id = "show-more-courses" and not(contains(@style, "none"))]')
			flag = True
			while(flag == True):
				if(driver.find_elements_by_xpath('//*[@class = "block icon--xsmall icon-x-charcoal"]')):
					err_bttn = driver.find_elements_by_xpath('//*[@class = "block icon--xsmall icon-x-charcoal"]')[0]
					try:
						err_bttn.click()
					except:
						pass
				try:
					next_bttn.click()
				except:
					flag = False
				try:
					next_bttn = driver.find_element_by_xpath('//*[@id = "show-more-courses" and not(contains(@style, "none"))]')
					sleep(1)
				except:
					flag = False
				if (next_bttn.get_attribute('style') == "display: none;"):
					flag = False
					
				
			#Get the urls of courses
			course_urls = []
			for course in driver.find_elements_by_xpath('//a[contains(@class, "course-name") and not(contains(@class, "ad-name"))]'):
				course_urls.append(course.get_attribute('href'))
			driver.close()
			
			#Crawl through courses
			for url in course_urls:
				yield Request(url = url, callback = self.parse_course, dont_filter = True)
	
	def parse_course(self, response):
		course = Course()
		################# DONE
		course['url'] = response.url
		################# DONE
		try:
			course['name'] = response.xpath('//*[@id = "course-title"]/text()').extract_first().strip()
		except:
			course['name'] = ""
		#################
		try:
			course['language'] = response.xpath('//strong[contains(text(), "Language")]/following-sibling::a/text()').extract_first().strip()
		except:
			course['language'] = ""
		################# DONE
		try:
			hpw = response.xpath('//*[contains(text(), "Effort")]/following-sibling::*/text()').extract_first()
			hpw = hpw.split()
			course['hours_per_week'] = hpw[hpw.index('hours') - 1]
		except:
			course['hours_per_week'] = ""
		###############DONE
		if(response.xpath('//strong[contains(text(), "Certificate")]')):
			course['has_certificates'] = 'TRUE'
		else:
			course['has_certificates'] = 'FALSE'
		################# DONE
		try:
			course['categories'] = response.xpath('//*[@itemprop = "title" and contains(@class, "text")]/text()').extract_first().strip()
		except:
			course['categories'] = ""
		################# DONE
		try:
			course['educator'] = response.xpath('//*[contains(text(),"Taught by")]/following-sibling::*/text()').extract_first().strip()
		except:
			course['educator'] = ""
		################# DONE
		try:
			course['organisation_name'] = response.xpath('//*[contains(@data-overlay-trigger, "institution")]/text()').extract_first().strip()
		except:
			course['organisation_name'] = ""
		################# DONE
		try:
			course['runs_start_date'] = response.xpath('//*[@id = "sessionOptions"]/option/@content').extract_first()
		except:
			course['runs_start_date'] = ""
		################# DONE
		try:
			duration = response.xpath('//*[contains(text(),"Duration")]/following-sibling::*/text()').extract_first().split()
			course['runs_duration_in_weeks'] = duration[duration.index('weeks') - 1]
		except:
			course['runs_duration_in_weeks'] = ""
		################# DONE
		try:
			enrol = response.xpath('//optgroup/@label').extract()
			if(enrol == ['Finished']):
				course['open_for_enrolment'] = 'FALSE'
			else:
				course['open_for_enrolment'] = 'TRUE'
		except:
			course['open_for_enrolment'] = ""
		################# DONE
		try:
			course['price'] = response.xpath('//*[contains(text(),"Cost")]/following-sibling::*/text()').extract_first().strip()
		except:
			course['price'] = ""
		################# DONE
		course['industry'] = ""
		################# DONE
		course['level'] = ""
		################# DONE
		try:
			course['provider'] = response.xpath('//*[contains(text(),"Provider")]/following-sibling::*/text()').extract_first().strip()
		except:
			course['provider'] = ""
		################# DONE
		course['skills'] = ""
		################# DONE
		try:
			course['syllabus'] = response.xpath('//*[@data-expand-article-target="syllabus"]//text()').extract()
		except:
			course['syllabus'] = ""
		################# DONE
		course['job_title'] = ""
		################# DONE
		try:
			subs = response.xpath('//*[@itemprop = "title" and not(contains(@class, "text"))]/text()').extract()
			if (len(subs) > 2 and subs[2] != "Home"):
				course['subject'] = subs[2]
			else:
				course['subject'] = course['categories']
		except:
			course['subject'] = ""
		################# DONE
		course['field_of_study'] = ""
		################# DONE
		try:
			course['about_the_course'] = response.xpath('//*[@data-expand-article-target="overview"]//text()').extract()
		except:
			course['about_the_course'] = ""
		################# DONE
		course['description'] = ""
		################# DONE
		try:
			course['certificate'] = response.xpath('//*[contains(text(),"Certificate")]/following-sibling::*/text()').extract_first().strip()
		except:
			course['certificate'] = ""
		################# DONE
		try:
			course['rating'] = response.xpath('//*[contains(@class, "course-all-reviews")]//*[contains(@class, "review-rating medium")]/span/text()').extract_first().strip()
		except:
			course['rating'] = ""
			
		yield course
