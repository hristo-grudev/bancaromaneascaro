import scrapy

from scrapy.loader import ItemLoader
from ..items import BancaromaneascaroItem
from itemloaders.processors import TakeFirst


class BancaromaneascaroSpider(scrapy.Spider):
	name = 'bancaromaneascaro'
	start_urls = ['https://www.banca-romaneasca.ro/despre-noi/noutati/']

	def parse(self, response):
		post_links = response.xpath('//div[@id="primarylinks"]//div[@class="boxPresentation"]')
		for post in post_links:
			date = post.xpath('./p[@class="subtitle"]/text()').get()
			title = post.xpath('./h2/a/text()').get()
			url = post.xpath('./h2/a/@href').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//div[@class="articleBody"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BancaromaneascaroItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
