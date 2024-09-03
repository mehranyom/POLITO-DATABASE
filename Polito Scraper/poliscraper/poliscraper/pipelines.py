from itemadapter import ItemAdapter
import mysql.connector as dbconnector
from poliscraper.items import Professors, Teach, Course

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
            host='localhost',
            user='root',
            password='Qwertyuiop123@',
        )
        self.curr = self.connection.cursor()

    def create_database(self):
        self.curr.execute('CREATE DATABASE IF NOT EXISTS polito')
        self.connection.database = 'polito'

    def create_table(self):
        create_professors_table = (
            "CREATE TABLE IF NOT EXISTS professors ("
            "PID CHAR(6) PRIMARY KEY, "
            "Name VARCHAR(255), "
            "Title VARCHAR(255), "
            "Department VARCHAR(255), "
            "Email VARCHAR(255))"
        )
        create_teaches_table = (
            "CREATE TABLE IF NOT EXISTS teaches ("
            "PID CHAR(6), "
            "CID CHAR(7), "
            "PRIMARY KEY (PID, CID))"
        )
        create_course_table = (
            "CREATE TABLE IF NOT EXISTS course ("
            "CID CHAR(7) PRIMARY KEY, "
            "CName VARCHAR(255), "
            "Language VARCHAR(50), "
            "Credits INT, "
            "ExType VARCHAR(255))"
        )

        self.curr.execute(create_professors_table)
        self.curr.execute(create_teaches_table)
        self.curr.execute(create_course_table)

    def process_item(self, item, spider):
        try:
            self.store_db(item)
            self.connection.commit()  # Commit after each item is processed
        except Exception as e:
            self.connection.rollback()  # Rollback in case of error
            spider.logger.error(f"Error processing item {item}: {e}")
        return item

    def store_db(self, item):
        # Check if the item is of type Professors
        if isinstance(item, Professors):
            add_professor = (
                "INSERT INTO professors (PID, Name, Title, Department, Email) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            data_professor = (
                item.get("pid"), 
                item.get("name"), 
                item.get("title"), 
                item.get("department"), 
                item.get("email")
            )
            self.curr.execute(add_professor, data_professor)

        # Check if the item is of type Teach
        elif isinstance(item, Teach):
            add_teaching = (
                "INSERT INTO teaches (PID, CID) "
                "VALUES (%s, %s)"
            )
            data_teaching = (
                item.get("professor_id"), 
                item.get("course_id")
            )
            self.curr.execute(add_teaching, data_teaching)

        # Check if the item is of type Course
        elif isinstance(item, Course):
            add_course = (
                "INSERT INTO course (CID, CName, Language, Credits, ExType) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            data_course = (
                item.get("cid"), 
                item.get("cname"), 
                item.get("lang"), 
                item.get("credit"), 
                item.get("etype")
            )
            self.curr.execute(add_course, data_course)
