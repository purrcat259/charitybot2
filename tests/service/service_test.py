import sys

import subprocess
from time import sleep

from neopysqlite.neopysqlite import Neopysqlite


class ServiceTest:
    def __init__(self, db_path, sql_reset_file_path, service_path):
        self.db_path = db_path
        self.sql_reset_file_path = sql_reset_file_path
        self.service_path = service_path
        self.service = None
        self.reset_db()

    def get_reset_sql_script(self):
        sql_string = ''
        with open(self.sql_reset_file_path, 'r') as sql_file:
            for line in sql_file.readlines():
                sql_string += line.strip()
        print(sql_string)
        return sql_string

    def reset_db(self):
        db = Neopysqlite(database_name='Service Test DB', db_path=self.db_path, verbose=True)
        db.execute_sql(self.get_reset_sql_script())

    def start_service(self):
        print('Starting Microservice')
        args = [sys.executable, self.service_path]
        self.service = subprocess.Popen(args)
        sleep(2)

    def stop_service(self):
        print('Stopping Microservice')
        self.service.terminate()
