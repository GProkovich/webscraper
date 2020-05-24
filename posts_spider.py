import scrapy

class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = [
        #'https://gracespyware.wordpress.com/gallery/'
        'https://gracespyware.wordpress.com/'
    ]

    def parse(self, response):
        #page = response.url.split('/')[-1]
        #filename = 'posts-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        for post in response.css('div.post-item'):
            yield{
                'title': post.css('.post-header h2 a::text')[0].get(),
                'date': post.css('.post-header a::text')[1].get(),
                'author': post.css('.post-header a::text')[2].get(),
            }
        next_page = response.css('a.menu-item menu-item-type-post_type menu-item-object-page menu-item-341::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
