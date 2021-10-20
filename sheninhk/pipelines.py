# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


#yield一次执行一次，不适合在此做文本记录
class FilePipeline(object):
    def process_item(self, item, spider):
        detail_url = item["detail_url"]
        image_urls=item["image_urls"]
        if image_urls:
            with open('shein_ssnz.csv', 'a+', newline='') as f:
                f.write('%s,'%detail_url+",".join(image_urls)+'\n')
        return item

class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={"item": item})  # 传参

    def file_path(self, request, response=None, info=None):
        load_path = request.meta["item"].get("load_path")
        print("file_path *****", load_path)
        image_guid = request.url.split('?')[0]
        image_guid = image_guid.split('/')[-1]
        return '%s/%s' % (load_path, image_guid)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no files")
        item['image_paths'] = image_paths
        return item
