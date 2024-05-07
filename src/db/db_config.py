from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import insert

Base = declarative_base()

class DatabaseInteractor:
    def __init__(self, logger, db_url):
        self.__logger = logger
        self.__engine = create_engine(db_url, echo=True)
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    @classmethod
    def psql_conn_string(self, host, username, password, port, db_name):
        conn_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
        return conn_string
    
    def create_tables(self):
        # self.__logger("creating all tables")
        Base.metadata.create_all(self.__engine)

    def __execute_stmt(self, stmt):
        data = self.__session.execute(stmt)
        self.__session.commit()
        return data
    
    def __get_primary_keys(self, Table):
        primary_keys = [key.name for key in inspect(Table).primary_key]
        return primary_keys
    
    def insert_data_to_rdbms(self, table, values_to_insert, conflict_mode='upsert'):
        self.__logger.info(f"Building insert statement to table {table}. {len(values_to_insert)} rows")
        primary_keys = self.__get_primary_keys(table)
        insert_stmt = insert(table).values(values_to_insert)

        if conflict_mode == 'upsert':
            conflict_stmt = insert_stmt.on_conflict_do_update(
                index_elements=primary_keys,
                set_={col: getattr(insert_stmt.excluded, col) for col in values_to_insert[0]}
                # grabbing the schema from the first value: this demands that we declare null values explicitly
            )

        elif conflict_mode == 'do_nothing':
            conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=primary_keys)

        else:
            raise ValueError(conflict_mode)    
        self.__execute_stmt(insert_stmt)
        self.__logger.info("Commited changes to database.")
