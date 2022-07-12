import pyodbc
from ui import start_menu


def main():
    sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                                SERVER=KACPEREK_PC\KACPERSQL;\
                                DATABASE=VideoStoreScript;\
                                Trusted_Connection=yes')

    cursor = sql_conn.cursor()

    start_menu(sql_conn, cursor)


"""
        query = "SELECT * FROM v_all_clients"
        df = pd.read_sql(query, sql_conn)
        print(df.head(3).to_string(), "\n")

        cursor.execute("DELETE FROM Clients WHERE name = 'Adam' and last_name = 'Szapkowski'")
        cursor.commit()

        df = pd.read_sql(query, sql_conn)
        print(df.head(3).to_string(), "\n")

        df = pd.read_sql("SELECT * FROM Documents", sql_conn)
        print(df.head(3).to_string(), "\n")
    """

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
