import scrapy
from poliscraper.items import Poliprofessors

class PolispiderSpider(scrapy.Spider):
    name = "polispider"
    allowed_domains = ["polito.it"]
    start_urls = ["https://www.polito.it/en/research/ecosystem/departments"]
    def parse(self, response):
        departments = response.css('.btn-service')
        for each_department in departments:
            department_url =  each_department.attrib['href']
            yield response.follow(department_url, callback= self.parse_department_page)
            
    def parse_department_page(self, response):
        staff_page = response.xpath('//a[contains(text(), "Staff") or contains(text(), "Personale")]/@href').get()
        yield response.follow(staff_page, callback= self.parse_department_staff_page)
        
    def parse_department_staff_page(self, response):
        professors_page = response.css('a#professori::attr(href)').get()
        yield response.follow(professors_page, callback= self.parse_department_profesoors_page)
        
    def parse_department_profesoors_page(self, response):
        professors = response.css('table.duecolonne a')
        for each_proff in professors:
            professor_page = each_proff.attrib['href']
            yield response.follow(professor_page, callback= self.parse_proffesor_page)
            
    def parse_proffesor_page(self, response):
        name = response.css('h1.page-title::text').get()
        title = response.css('section.dettagli h2::text').get()
        department = response.css('section.dettagli h2 a::text').get()
        mail = response.xpath('//section[contains(@class, "dettagli")]//a[starts-with(@href, "mailto:")]/text()').get()

        prof_item = Poliprofessors()
        
        prof_item['name'] = name
        prof_item['title'] = title
        prof_item['department'] = department
        prof_item['email'] = mail
        yield prof_item