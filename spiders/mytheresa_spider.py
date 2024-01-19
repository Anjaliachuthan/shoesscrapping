import time
import scrapy




class MytheresaSpiderSpider(scrapy.Spider):
    name = "mytheresa_spider"
    allowed_domains = ["mytheresa.com"]
    start_urls = ["https://www.mytheresa.com/int_en/men/shoes.html"]
    custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
   
    def parse(self, response):
    
    
        print(f"Processing page: {response.url}")

        for product_url in response.css('a.item__link::attr(href)').extract():

            yield scrapy.Request(url=response.urljoin(product_url), callback=self.parse_product)

        
        next_page = response.css('a[data-label="next"]::attr(href)').get()
        print("next_____page", response.urljoin(next_page))

        if next_page:
            yield response.follow(response.urljoin(next_page), callback=self.parse)


    def parse_product(self, response):
        bread_crumbs = response.css('div.breadcrumb__item')
        bread_crumbs_list = []
        for bread_crumb in bread_crumbs:
            bread_crumb_text = bread_crumb.css('a.breadcrumb__item__link::text').get()
            bread_crumbs_list.append(bread_crumb_text)
        index_0_items = ""
        other_index_items = []
        swiper_slide_divs = response.css('div.swiper-slide')
        for swiper_slide_div in swiper_slide_divs:
            slide_index = swiper_slide_div.css('::attr(data-swiper-slide-index)').get()
            if slide_index == "0":
                index_0_items=swiper_slide_div.css('img::attr(src)').get()
            else:
     
                other_index_items.append(swiper_slide_div.css('img::attr(src)').get() )
        def get_first_or_not_blank(li):
            for item in li:
                if item !=" ":
                    return item
        
        discountList = response.css('span.pricing__info__percentage::text').extract()
        listing_price_list=response.css("span.pricing__prices__price::text").extract()
        offer_price_list = response.css("span.pricing__prices__discount span.pricing__prices__price::text").extract()
        discount = get_first_or_not_blank(discountList)
        off_price = get_first_or_not_blank(offer_price_list)
        list_price = get_first_or_not_blank(listing_price_list)
        product_info={
            "breadcrumbs": bread_crumbs_list,
            # "image": index_0_items,
            'image' : response.css('img::attr(src)').extract_first(),
            'brand': response.css('a.product__area__branding__designer__link::text').extract_first(),
            "product_name": response.css('div.product__area__branding__name::text').extract_first(),
            "listing__price":list_price,
            "offer_price":off_price,
            "discount":discount,
            "other_images":other_index_items[1:7],
            
         
        }
        yield product_info
