import scrapy
from scrapy.http import Request
from ..items import SheninhkItem
import re
import json

class SheinSpider(scrapy.Spider):
    name = 'shein'
    allowed_domains = ['shein.com.hk']
    # start_urls = ['http://shein.com.hk/Women-Bikini-Sets-c-1866.html?page=1']

    def start_requests(self):
        for i in range(1,2):
            yield Request(url='http://shein.com.hk/Women-Bikini-Sets-c-1866.html?page=%d'% i,callback=self.parse_goodsurl)
            # yield Request(url='https://www.shein.com.hk/3pack-Ring-Linked-Bikini-Swimsuit-Beach-Skirt-p-3418501-cat-1866.html',callback=self.parse_imgurls)

    def parse_goodsurl(self, response):
        """
        :param response:
        :yield: 页面中每个产品的详情页的url
        """
        # print(response)
        # print(response.text)
        goods=re.findall(r'var gbProductListSsrData =.*}', response.text)
        res=json.loads(goods[0].split('=',1)[-1])
        goods_list=res.get('results').get('goods')
        goods_urls = []
        for good in goods_list:
            good_ids=set()
            good_url_str = good.get('goods_url_name')
            good_url_name = re.sub(' ', '-', good_url_str)
            good_ids.add(str(good.get('goods_id')))
            good_relate=good.get('relatedColor')
            if len(good_relate) > 0:
                for g in good_relate:
                    good_ids.add(str(g.get('goods_id')))
            # print(good_ids)
            for good_id in good_ids:
                url='https://www.shein.com.hk/%s-p-%s-cat-1866.html' % (good_url_name, good_id)
                goods_urls.append(url)
                htmlRequest=Request(url=url, callback=self.parse_imgurls)
                # htmlRequest.meta["item"] = item  # 传参
                yield htmlRequest

        # with open('goods_urls.csv','a',encoding='utf-8',newline='') as f_w:
        #     f_w.write(",".join(goods_urls)+'\n')

    def parse_imgurls(self,response):
        """
        :param response:
        :yield: 图片地址列表到pipelines
        """
        # print(response.text)
        # print(response.url)
        detail_page=response.url
        good_id=response.url.split('-p-',1)[-1].split('-',1)[0]
        item=SheninhkItem()
        item['detail_url']=detail_page
        item['load_path'] = good_id
        # item = response.meta["item"]
        images_set=set()
        image_urls=[]
        detail_js = re.findall(r'productIntroData: .*},', response.text)
        res=detail_js[0].split(': ', 1)[-1]
        detail_res = json.loads(res.rsplit(',', 1)[0])
        goods_images = detail_res.get('goods_imgs')
        main_imgurl=goods_images.get('main_image').get('origin_image')
        if main_imgurl: images_set.add(main_imgurl)
        detail_imgurls = goods_images.get('detail_image')
        if len(detail_imgurls) > 0:
            for detail_imgurl in detail_imgurls:
                images_set.add(detail_imgurl.get('origin_image'))
        if len(images_set) >0:
            for img_url in images_set:
                image_urls.append('https:%s'%img_url)
        item['image_urls']=image_urls
        print('#######',detail_page)
        # with open('shein_ssnz.csv','a',encoding='utf-8',newline='') as f_w:
        #     f_w.write('%s,'%detail_page+",".join(image_urls)+'\n')
        yield item










