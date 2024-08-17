# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector as dbconnector

class PoliscraperPipeline:
    def process_item(self, item, spider):
        return item
class SavingToMysqlPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_database()
        self.create_table()

        
    def create_connection(self):
        self.connection = dbconnector.connect(
            host= 'localhost',
            user= 'root',
            password = '1234',
        )
        self.curr = self.connection.cursor()
        
    def create_database(self):
        self.curr.execute('CREATE DATABASE IF NOT EXISTS polito')
        self.connection.database = 'polito'
        
    def create_table(self):
        table_creation_query = ("CREATE TABLE IF NOT EXISTS professors ("
                                "Name VARCHAR(255),"
                                "Title VARCHAR(255),"
                                "Department VARCHAR(255),"
                                "Email VARCHAR(255))")
        
        self.curr.execute(table_creation_query)
        
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        add_professor = ("INSERT INTO professors"
                         "(Name, Title, Department, Email)"
                         "VALUES (%s, %s, %s, %s)")
        data_professor = (item["name"], item["title"], item["department"], item["email"])
        self.curr.execute(add_professor, data_professor)
        self.connection.commit()