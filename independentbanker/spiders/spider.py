import datetime

import scrapy

from scrapy.loader import ItemLoader

from ..items import IndependentbankerItem
from itemloaders.processors import TakeFirst

base = 'https://independentbanker.org/{}/'

class IndependentbankerSpider(scrapy.Spider):
	name = 'independentbanker'
	year = 2011
	start_urls = [base.format(year)]

	def parse(self, response):
		post_links = response.xpath('//div[@class="post-inner"]//h2[@class="entry-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

		if self.year < datetime.datetime.now().year:
			self.year += 1
			yield response.follow(base.format(self.year), self.parse)

	def parse_post(self, response):
		title = response.xpath('//header[@class="entry-header"]//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="entry-meta"]/text()').get()

		item = ItemLoader(item=IndependentbankerItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
