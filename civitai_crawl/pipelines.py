# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import json

class CivitaiCrawlPipeline:
    def open_spider(self,spider):
        self.file_creator=open(spider.name+'_creator.jsonl','a+')
        self.file_model=open(spider.name+'_model.jsonl','a+')

    def process_item(self, item, spider):
        adapter=ItemAdapter(item)
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        if adapter.get('name'):
            self.file_creator.write(line)
        if adapter.get('id'):
            self.file_model.write(line)
        return item

    def closs_spider(self,spider):
        self.file_creator.close()
        self.file_model.close()

class Image_down(ImagesPipeline):
    # def file_path(self, request, response=None, info=None, *, item=None):
    #     print(request)
    #     image_guid = request.url.split('/')[-1]  # 取原url的图片命名
    #     return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        if "images_link" in item:
            yield scrapy.Request(url=item['images_link'])

    def item_completed(self, results, item, info):
        pass
        # print(results)