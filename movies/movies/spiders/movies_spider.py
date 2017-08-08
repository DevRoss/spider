# coding: utf-8
import scrapy
import json
import re
from movies.items import MoviesItem, MoviesNetItem, MoviesCategoriesItem, MoviesStarringItem
import threading
from movies.tool.get_ip_pools import run_get_proxy
import time

re_movies_link = re.compile('https://movie.douban.com/subject/(\d+)/')


class MoviesSpider(scrapy.Spider):
    name = "movies"

    # counter = 1
    def start_requests(self):
        # self.job = threading.Thread(target=run_get_proxy)
        # self.job.start()
        # self.job.join()
        urls = [
            'https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=500',
            # 'https://movie.douban.com/subject/1305487/'
            # 'https://movie.douban.com/subject/1826201/',  # 无编剧
            # 'https://movie.douban.com/subject/1470591/',  # 无主演
            # 'https://movie.douban.com/subject/3578943/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # yield scrapy.Request(url=url, callback=self.parse_movies)

    def parse(self, response):
        movies_list = json.loads(response.text)
        for movie in movies_list['subjects']:
            url = movie.get('url')
            yield scrapy.Request(url=url, callback=self.parse_movies)

    def parse_movies(self, response):
        # if self.counter % 1000 == 0:
        #     self.job.start()
        # self.counter += 1
        name = response.css('#content > h1 > span::text').extract_first()

        # 制作组
        movie_team = response.css('#info span')
        director = movie_team.css('.attrs a[rel*=directedBy]::text').extract_first()
        # print(movie_team[3].extract())
        if '编剧' in movie_team[3].extract():
            movie_team_ = response.css('#info span .attrs')
            screenwriter = movie_team_[1].css('a ::text').extract()
        else:
            screenwriter = None
        starrings = movie_team.css('.attrs a[rel*=starring]::text').extract()
        if not starrings:
            starrings = None

        categories = response.css('#info span[property*=genre]::text').extract()

        info_extract = response.css('#info').extract()[0]
        re_country_or_region = re.search(r'<span class="pl">制片国家/地区:</span>(.*)<br>', info_extract)
        country_or_region = re_country_or_region.group(1).strip().split(' / ')
        # 电影语言，None 为无声电影
        try:
            re_languages = re.search(r'<span class="pl">语言:</span>(.*)<br>', info_extract)
            languages = re_languages.group(1).strip().split(' / ')
        except AttributeError:
            languages = None
        release_date = response.css('#info span[property*=initialReleaseDate]::text').extract()
        runtime = response.css('#info span[property*=runtime]::text').extract_first()
        # 其他名字
        try:
            re_other_names = re.search(r'<span class="pl">又名:</span>(.*)<br>', info_extract)
            other_names = re_other_names.group(1).strip().split(' / ')
        except AttributeError:
            other_names = None
        rate = response.css(
            '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong::text').extract_first()

        instance = MoviesItem()
        instance['name'] = name
        instance['director'] = director
        instance['screenwriter'] = screenwriter
        instance['starrings'] = starrings
        instance['categories'] = categories
        instance['country_or_region'] = country_or_region
        instance['languages'] = languages
        instance['release_date'] = release_date
        instance['runtime'] = runtime
        instance['other_names'] = other_names
        instance['rate'] = rate
        instance['id'] = re.match(re_movies_link, response.url).group(1)
        yield instance
        # 分类
        for category in categories:
            cate = MoviesCategoriesItem()
            cate['category_and_movies'] = (category, name)
            yield cate

        # 演员
        if starrings:
            for starring in starrings:
                star = MoviesStarringItem()
                star['starring_and_movies'] = (starring, name)

        # 推荐
        recommended = response.css('#recommendations > div > dl > dd > a::attr(href)').extract()
        for movie in recommended:
            # 电影关系
            net = MoviesNetItem()
            movie_url = re.match(re_movies_link, movie)
            net['has_relation'] = (instance['id'], movie_url.group(1))
            yield net
            yield scrapy.Request(url=movie_url.group(), callback=self.parse_movies)
