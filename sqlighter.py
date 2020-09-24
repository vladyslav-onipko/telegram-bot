import sqlalchemy
import os


class User:

    def __init__(self, db_name):
        if os.path.exists(db_name):
            os.remove(db_name)
        self.db = sqlalchemy.create_engine(f'sqlite:///{db_name}')
        self.db.execute("""
        create table users (
        id integer primary key,
        user_id integer not null,
        status integer not null default 1
        )
        """)

    def get_user(self, status=1):
        result = self.db.execute("select user_id from users where (:status)", status=status)
        return result.fetchone()

    def exist_user(self, user_id):
        result = self.db.execute("select user_id from users where (:user_id)", user_id=user_id)
        return bool(result.fetchone())

    def add_user(self, user_id, status=1):
        self.db.execute("""
        insert into users (user_id, status) values (:user_id, :status)
        """, user_id=user_id, status=status)

    def delete_user(self, user_id):
        self.db.execute("""
        delete from users where (:user_id)
        """, user_id=user_id)