# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from myteck_scraping.items import MyteckScrapingItem
from scrapy.conf import settings




class WikibeerSpider(CrawlSpider):

    name = "teck"
    allowed_domains = ["mytek.tn"]
    start_urls = [
        "http://www.mytek.tn/3-informatique",
        "http://www.mytek.tn/104-telephonie-tunisie",
        "http://www.mytek.tn/7-impression",
        "http://www.mytek.tn/39-image-son",
        "http://www.mytek.tn/57-reseaux-securite-tunisie",
        "http://www.mytek.tn/5-gaming",

    ]
    rules = (
    Rule(LinkExtractor(
    			allow = r'html$',
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"),
    )
    
    
    def __init__(self, *a, **kw):
        super(WikibeerSpider, self).__init__(*a, **kw)
        settings.overrides['DEPTH_LIMIT'] = 2

    def parse_items(self, response):
        items =[]
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # site = response.xpath('//div[contains(@class, "right-block")]')
        # for sel in site:

        #     # On vérifie qu'il ne s'agit pas du header du tableau
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
            	item = MyteckScrapingItem()
            	item['name'] = response.xpath('//h1[contains(@itemprop, "name")]/text()').extract()
            	item['price'] = response.xpath('//span[contains(@id, "our_price_display")]/text()').extract()
                item['image_url'] = response.xpath('//span[contains(@id, "view_full_size")]/img/@src').extract()
                item['category'] = response.xpath('//span[contains(@itemprop, "title")]/text()').extract_first()# response.xpath('//span[contains(@class, "navigation_page")][0]/a/text()').extract()
                item['sub_category'] = response.xpath('//span[contains(@itemprop, "title")]/text()')[1].extract()
                item['addr_pr'] = response.xpath('//link[contains(@rel, "canonical")]/@href').extract()
                item['store'] = "My Teck"
                if not item in items:
                    items.append(item)
		        # item['price'] = response.xpath('//span[contains(@id, "our_price_display")]/text()').extract()
		        # items.append(item)
        return items