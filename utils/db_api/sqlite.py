import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL UNIQUE,
            name varchar(255) NOT NULL,
            phone_number varchar(255),
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    # @staticmethod
    # def format_args(sql, parameters: dict):
    #     sql += " AND ".join([
    #         f"{item} = ?" for item in parameters
    #     ])
    #     return sql, tuple(parameters.values())
    
    @staticmethod
    def format_args(sql, parameters: dict):
        conditions = []
        for item, in parameters.keys():
            conditions.append(f"{item} = ?")
        sql += " AND ".join(conditions)
        return sql, tuple(parameters.values())

    def add_user(self, id: int, name: str, phone_number: str = None, language: str = 'uz'):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, phone_number) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(id, name, phone_number, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, phone_number, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_phone_number (self, phone_number, id):
        # SQL_EXAMPLE = "UPDATE Users SET phone_number=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone_number=? WHERE id=?
        """
        return self.execute(sql, parameters=(phone_number, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
