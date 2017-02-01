from charitybot2.paths import production_repository_db_path
from charitybot2.persistence.sqlite_repository import SQLiteRepository
from tests.paths_for_tests import test_repository_db_path


class EventAlreadyRegisteredException(Exception):
    pass


class EventNotRegisteredException(Exception):
    pass


class EventRepository(SQLiteRepository):
    def __init__(self, debug=False):
        self._db_path = production_repository_db_path if not debug else test_repository_db_path
        super().__init__(db_path=self._db_path)
        self.__validate_repository()

    @property
    def db_path(self):
        return self._db_path

    def __validate_repository(self):
        event_table_create_query = 'CREATE TABLE IF NOT EXISTS `events` (' \
                                   '`eventId`          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,' \
                                   '`identifier`       TEXT NOT NULL,' \
                                   '`title`            TEXT NOT NULL,' \
                                   '`startTime`        INTEGER NOT NULL,' \
                                   '`endTime`          INTEGER NOT NULL,' \
                                   '`currencyKey`      TEXT NOT NULL,' \
                                   '`startingAmount`   REAL,' \
                                   '`targetAmount`     REAL NOT NULL,' \
                                   '`sourceUrl`        TEXT NOT NULL,' \
                                   '`updateDelay`      INTEGER);'
        self.open_connection()
        self.execute_query(query=event_table_create_query, commit=True)
        self.close_connection()

    def event_already_registered(self, identifier):
        query = 'SELECT COUNT(*) FROM `events` WHERE identifier = ?'
        data = (identifier, )
        self.open_connection()
        count = self.execute_query(query=query, data=data).fetchall()
        self.close_connection()
        return count[0][0] > 1

    def get_event_configuration(self, identifier):
        pass

    def register_event(self, event_configuration):
        pass

    def update_event(self, new_event_configuration):
        pass
