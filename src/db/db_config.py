from sqlalchemy import create_engine, select, update, inspect, and_
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from data_transformer import DataTransformer
from sqlalchemy.exc import SQLAlchemyError
from colors import COLORS

Base = declarative_base()

class Database:
    def __init__(self, db_url):
        self.__engine = create_engine(db_url, echo=True)
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    @classmethod
    def psql_conn_string(self, host, username, password, port, db_name):
        conn_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}'
        return conn_string
    
    def create_tables(self):
        Base.metadata.create_all(self.__engine)
        
    def execute_stmt(self, stmt):
        data = self.__session.execute(stmt)
        self.__session.commit()
        return data
    
    def get_pks(self, Table):
        pks_cols = inspect(Table).primary_key
        pks = [pk.name for pk in pks_cols]
        return pks
    
    def insert_record(self, Table, record):
        pks = self.get_pks(Table)
        insert_stmt = insert(Table).values(record)
        insert_stmt = (
            insert_stmt.
            on_conflict_do_update(
				index_elements=pks,
				set_=dict(insert_stmt.excluded)
			)
        )
        try:
            self.execute_stmt(insert_stmt)
            return 1
        except SQLAlchemyError as e:
            print(f'SQLAlchemy error: {e}')
            print(f'Error inserting record: {record}')
            return 0
    
    def update_processed_at(self, Table, record):
        pks = self.get_pks(Table)
        condition = [getattr(Table, pk) == record[pk] for pk in pks]
        update_stmt = (
            update(Table)
            .where(and_(*condition))
            .values(processed_at = DataTransformer.get_current_time())
        )
        try:
            self.execute_stmt(update_stmt)
            return 1
        except SQLAlchemyError as e:
            print(f'{COLORS['RED']}SQLAlchemy error: {e}')
            print(f'Error inserting record: {record}{COLORS['WHITE']}')
            return 0

    def retrieve_not_processed_records(self, Table):
        select_stmt = select(Table).where(Table.processed_at == None)
        result = self.execute_stmt(select_stmt)

        result_scalar = result.scalars().all()
        result_dict_list = DataTransformer.models_to_dict_list(result_scalar)

        return result_dict_list