# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item
from scrapy import Field

class Course(Item):
	
	url = Field()
	name = Field()
	language = Field()
	hours_per_week = Field()
	has_certificates = Field()
	categories = Field()
	educator = Field()
	organisation_name = Field()
	runs_start_date = Field()
	runs_duration_in_weeks = Field()
	open_for_enrolment = Field()
	price = Field()
	industry = Field()
	level = Field()
	provider = Field()
	skills = Field()
	syllabus = Field()
	job_title = Field()
	subject = Field()
	field_of_study = Field()
	about_the_course = Field()
	description = Field()
	certificate = Field()
	rating = Field()
	runs_duration = Field()

