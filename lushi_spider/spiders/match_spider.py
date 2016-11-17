import exceptions
from scrapy import Request
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider

from lushi_spider.items import MatchItem, CompeteItem

total_page = 212


class MatchSpider(CrawlSpider):
    name = "match"
    allowed_domains = ["gosugamers.net"]
    start_urls = [
        "http://www.gosugamers.net/hearthstone/gosubet"
    ]

    current_page = 1

    def parse(self, response):
        global match_href
        try:
            for match in Selector(response).xpath('//div[@id="col1"]//div[@class="content"]')[2].xpath('table/tbody/tr'):
                item = MatchItem()
                match_href = match.xpath('td/a[@class="match hover-background"]/@href').extract()[0]
                match_href_arr = match_href.split("/")
                race_name = match_href_arr[3]
                if 7 in match_href_arr:
                    match_name = match_href_arr[7]
                else:
                    match_name = match_href_arr[5]
                item['race_name'] = race_name
                item['match_name'] = match_name
                item['left_player'] = match.xpath('td/a/span[@class="opp opp1"]/span[1]/text()').extract()[0]
                item['right_player'] = match.xpath('td/a/span[@class="opp opp2"]/span[2]/text()').extract()[0]
                yield item

                yield Request("http://www.gosugamers.net" + match_href,
                              callback=self.parse_match)
            if self.current_page < total_page:
                self.current_page += 1
                yield Request("http://www.gosugamers.net/hearthstone/gosubet?r-page=" + str(self.current_page),
                              callback=self.parse)
        except exceptions.IndexError:
            print 'match_href == ' + match_href

    def parse_match(self, response):
        match_href_arr = response.url.split("/")
        if 9 in match_href_arr:
            match_name = match_href_arr[9]
        else:
            match_name = match_href_arr[7]
        for compete in Selector(response).xpath('//span[contains(@class,"match-game-tab")]'):
            if compete.xpath("input[@class='btn-winner']").__len__() > 0:
                winner_text_field = compete.xpath("input[@class='btn-winner']/@value").extract()[0]
                winner = winner_text_field[8:]

                compete_id = compete.xpath("@id").extract()[0]

                for lineup in Selector(response).xpath('//div[contains(@class,"lineups")]'):
                    lineup_ele = lineup.xpath('div[contains(@class, "' + compete_id + '")]')
                    item = CompeteItem()
                    if lineup_ele.xpath('//div[contains(@class, "opponent1Deck")]').__len__() > 0:
                        job1 = lineup_ele.xpath('//div[contains(@class, "opponent1Deck")]//img/@alt').extract()[0]
                        item['left_job'] = job1
                    if lineup_ele.xpath('//div[contains(@class, "opponent2Deck")]').__len__() > 0:
                        job2 = lineup_ele.xpath('//div[contains(@class, "opponent2Deck")]//img/@alt').extract()[0]
                        item['right_job'] = job2

                    item['winner'] = winner
                    item['match_name'] = str(match_name)
                    item['compete_id'] = str(compete_id)
                    return item
