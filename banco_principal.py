class Database:

    def __init__(self, host: str, user: str, database: str, table_name: str):
        self.host: str = host
        self.user: str = user
        self.database: str = database
        self.table_name: str = table_name
        self.details:dict = {
            "Host": self.host,
            "User": self.user,
            "Database": self.database,
            "Table name": self.table_name
        }
        self.data:dict = {}
        self.state:bool = False

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> dict:
        return self.data.keys()

    def connect(self) -> bool:
        from pymysql import connect
        from streamlit import text_input
        self.__password: str = text_input("Enter your password: ", type='password')
        self.connection = connect(
            host=self.host,
            password=self.__password,
            user=self.user,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        if self.connection:
            self.state = True
            return True
        return False

    def input_data(self) -> None:
        from streamlit import (write, text_input, number_input)
        if self.state == True:
            query:str = f"DESCRIBE {self.table_name}"
            self.cursor.execute(query)
            columns_describe:list = [column for column in self.cursor.fetchall()]
            write("Columns")
            for i in columns_describe:
                write(f"Column: {i[0]} // Type: {i[1]}")
            for column in columns_describe:
                if column[0].lower() == 'id':
                    pass
                elif 'int' in column[1].lower():
                    data = int(number_input(f"Enter data for {column[0]}, Type: {column[1]}: "))
                    self.data.update({column[0]: data})
                elif column[1].lower() in ['decimal','numeric','float','double']:
                    data = float(number_input(f"Enter data for {column[0]}, Type: {column[1]}: "))
                    self.data.update({column[0]: data})
                elif 'date' in column[1].lower():
                    from datetime import datetime
                    data = text_input(f"Enter {column[0]} (year-month-day), Type: {column[1]}: ")
                    date_object = datetime.strptime(data, '%d/%m/%Y')
                    formatted_date = date_object.strftime('%Y-%m-%d')
                    self.data.update({column[0]: formatted_date})
                elif 'time' in column[1].lower():
                    hour = text_input(f"Enter {column[0]} (hours:minutes:seconds), Type: {column[1]}: ")
                    self.data.update({column[0]:hour})
                elif column[1].lower() in ['datetime','timestamp']:
                    from datetime import datetime
                    date_time = text_input(f"Enter {column[0]} (year-month-day hours:minutes:seconds), Type: {column[1]}: ")
                    format:str = '%Y-%m-%d %H:%M:%S'
                    formated_datetime =  date_time.strftime(format)
                    self.data.update({column[0]:formated_datetime})
                else:
                    data = text_input(f"Enter data for {column[0]}, Type: {column[1]}: ")
                    self.data.update({column[0]: data})
        else:
            write("Database not connected.")

    def show_data(self) -> None:
        from streamlit import write
        if self.state == True:
            from streamlit import write
            for key, value in self.data.items():
                write(f"{key}: {value}")
        else:
            write("Database not connected.")


    def insert_data(self) -> bool:
        from streamlit import write
        if self.state == True:
            columns:str = ', '.join(self.data.keys())
            values:str = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in self.data.values()])
            query:str = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"
            write(f"SQL Query: {query}")
            self.cursor.execute(query)
            self.connection.commit()
            write("Data inserted successfully!")
            return True
        else:
            write("Database not connected.")
        return False

    def show_table(self) -> None:
        from streamlit import subheader, write
        if self.state == True: 
            from pandas import read_sql_query
            query:str = f"SELECT * FROM {self.table_name}"
            df = read_sql_query(query, self.connection)
            subheader(f"Table: {self.table_name}")
            write(df)
        else:
            write("Database not connected.")

    def disconnect(self) -> bool:
        self.connection.close()
        self.state = False
        return True
