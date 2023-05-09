import json

import scrapy

from ..items import CreatorItem, ModelItem


class CivitaiSpider(scrapy.Spider):
    name = 'civitai'
    allowed_domains = ['civitai.com']
    start_urls = ['https://civitai.com/api/v1/creators?page=1']
    proxy = "http://127.0.0.1:4780" # proxy setting, You can change to your own proxy

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={'proxy': self.proxy})

    def parse(self, response):
        data = json.loads(response.body.decode())

        for user in data['items']:
            if "modelCount" not in user: continue
            item = CreatorItem()
            item['name'] = user['username']
            item['model_num'] = user['modelCount']
            item['link'] = user['link']
            yield item
            yield scrapy.Request(url=item['link'], callback=self.parse_model, meta={'proxy': self.proxy})

        total_page = data['metadata']['totalPages']
        cur_page = data['metadata']['currentPage']
        if cur_page != total_page:
            yield scrapy.Request(url=data['metadata']['nextPage'], callback=self.parse, meta={'proxy': self.proxy})

    def parse_model(self, response):
        data = json.loads(response.body.decode())
        for model in data['items']:
            item = ModelItem()
            item['id'] = model['id']
            item['type'] = model['type']
            item['downloadCount'] = model['stats']['downloadCount']
            item['ratingCount'] = model['stats']['ratingCount']
            item['rating'] = model['stats']['rating']

            if (item['downloadCount']) < 1000 or item['rating'] < 4: continue # avoid low quality model

            item['base_model'] = model['modelVersions'][0]['baseModel']
            item['images_link'] = model['modelVersions'][0]['images'][0]['url']
            if model['modelVersions'][0]['images'][0]['meta']:
                item['images_prompt'] = model['modelVersions'][0]['images'][0]['meta']['prompt']
            else:
                item['images_prompt'] = None
            item['download_link'] = model['modelVersions'][0]['downloadUrl']
            yield item
