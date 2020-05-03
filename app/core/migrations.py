from __future__ import print_function

from mysql.connector import errorcode
from app.core.database import Database
from app.core.debug_handler import DebugHandler
from app.config.database import db_config
import os

class Migrations(object):
    db_instance = None
    db_connection = None
    mysql_instance = None
    mysql_connection = None
    mysql_ctx = None
    config = {}

    DB_NAME = None
    TABLES = {}

    def __init__(self, config = dict()):
        super(Migrations, self).__init__()
        
        # Set config
        self.config = db_config()

        # Override DB_NAME
        self.config['database'] = config.get('database')
        
        # Connect Database
        self.connect_database()

        # Prepare Tables
        # self.prepare_tables()

        # Create or Use database
        # self.create_database()

        # Create Tables
        # self.create_table()

        # Close Connection
        # self.close_connection()

        # print('here migration \n')

    def connect_database(self):
        # DB instance
        self.db_instance = Database(self.config)
        # Connect to database
        self.db_connection = self.db_instance.connect()

        self.mysql_instance = self.db_connection.get('mysql_instance')
        self.mysql_connection = self.db_connection.get('mysql_connection')
        self.mysql_ctx = self.db_connection.get('mysql_ctx')

    def close_connection(self):
        self.db_instance.close_connection(self.mysql_connection, self.mysql_ctx)

    def create_database(self, db_name):
        # Create database
        self.db_instance.create_database(self, db_name)

    def drop_database(self, db_name):
        # Drop database
        self.db_instance.drop_database(self, db_name)

    def create_table(self):
        # Create table
        for table_name in self.TABLES:
            action_raw = self.TABLES.get(table_name)
            action_name = action_raw.get('action')
            action_command = action_raw.get('command')

            self.db_instance.execute_command(self, table_name, action_name, action_command)

    def create_begin_process(self, title):
        print("/******** Begin {} ********/".format(title))

    def create_end_process(self, title):
        print("/******** End {} ********/\n".format(title))
    
    def rename_table(self, before_name, after_name):
        # Rename Table
        self.db_instance.rename_table(self, before_name, after_name)

    def execute_command(self, commands):
        # Execute Command
        for table_name in commands:
            action_raw = commands.get(table_name)
            action_name = action_raw.get('action')
            action_command = action_raw.get('command')

            self.db_instance.execute_command(self, table_name, action_name, action_command)

    def prepare_tables(self, tables):
        if not tables:
            self.TABLES = self.example_tables()
        
        self.TABLES = tables

    def example_tables(self):
        example_tables = {}

        example_tables['employees'] = (
            "CREATE TABLE `employees` ("
            "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
            "  `birth_date` date NOT NULL,"
            "  `first_name` varchar(14) NOT NULL,"
            "  `last_name` varchar(16) NOT NULL,"
            "  `gender` enum('M','F') NOT NULL,"
            "  `hire_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`)"
            ") ENGINE=InnoDB")

        example_tables['departments'] = (
            "CREATE TABLE `departments` ("
            "  `dept_no` char(4) NOT NULL,"
            "  `dept_name` varchar(40) NOT NULL,"
            "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
            ") ENGINE=InnoDB")

        example_tables['salaries'] = (
            "CREATE TABLE `salaries` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `salary` int(11) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
            "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        example_tables['dept_emp'] = (
            "CREATE TABLE `dept_emp` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `dept_no` char(4) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
            "  KEY `dept_no` (`dept_no`),"
            "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
            "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        example_tables['dept_manager'] = (
            "  CREATE TABLE `dept_manager` ("
            "  `dept_no` char(4) NOT NULL,"
            "  `emp_no` int(11) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date NOT NULL,"
            "  PRIMARY KEY (`emp_no`,`dept_no`),"
            "  KEY `emp_no` (`emp_no`),"
            "  KEY `dept_no` (`dept_no`),"
            "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
            "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
            "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        example_tables['titles'] = (
            "CREATE TABLE `titles` ("
            "  `emp_no` int(11) NOT NULL,"
            "  `title` varchar(50) NOT NULL,"
            "  `from_date` date NOT NULL,"
            "  `to_date` date DEFAULT NULL,"
            "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
            "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
            "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
            ") ENGINE=InnoDB")

        return example_tables