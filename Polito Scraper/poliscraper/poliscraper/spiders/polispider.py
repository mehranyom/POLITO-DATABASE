import scrapy
from poliscraper.items import Professors, Teach, Course

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
        pid = response.xpath('//section/@data-matricola').get()
        name = response.css('h1.page-title::text').get()
        title = response.css('section.dettagli h2::text').get()
        department = response.css('section.dettagli h2 a::text').get()
        mail = response.xpath('//section[contains(@class, "dettagli")]//a[starts-with(@href, "mailto:")]/text()').get()
        image_src = response.xpath('//section[contains(@class, "foto")]//img/@src').get()
        
        prof_item = Professors()
        
        prof_item['pid'] = pid
        prof_item['name'] = name
        prof_item['title'] = title
        prof_item['department'] = department
        prof_item['email'] = mail
        prof_item['image'] = image_src
        yield prof_item
        
        course_check_list = list()
        courses_name = response.xpath('//li[contains(@class, "corrente")]//a/text()').getall()
        courses_url = response.xpath('//li[contains(@class, "corrente")]//a/@href').getall()
        if courses_url:
            for i in range(len(courses_url)):
                if courses_name[i] in course_check_list:
                    pass
                else:
                    cname = courses_name[i]
                    curl = courses_url[i]
                    course_check_list.append(cname)
                    yield response.follow(curl, callback= self.parse_course_page, cb_kwargs= {'pid': pid, 'cname': cname})
                    
    def parse_course_page(self, response, pid, cname):
        course_ids = response.css('p.policorpo::text').get()
        course_ids_list = course_ids.split(', ')
        course_language = response.xpath('//div[contains(@class, "row paragraph")]//p/text()').get()    
        credits = response.xpath('//table[contains(@class, "table table-bordered")][.//th[text() = "CFU"]]//td/text()').getall()
        exam_type = response.xpath('//div[contains(@class, "col-sm-10 formattata")][.//strong[text() = "Exam:"]]/text()').getall()
        
        course_exam_type = exam_type[1].strip() if exam_type else 'NULL'
        
        course_credits = -1
        for context in credits:
            if context.isdigit():
                course_credits = int(context)
        
        teachs_item = Teach()
        course_item = Course()
        
        for cid in course_ids_list:
            teachs_item['professor_id'] = pid
            teachs_item['course_id'] = cid
            course_item['cid'] = cid
            course_item['cname'] = cname
            course_item['lang'] = course_language
            course_item['credit'] = course_credits
            course_item['etype'] = course_exam_type
            yield teachs_item
            yield course_item