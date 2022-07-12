import pyodbc
from datetime import datetime
from time import sleep
from validators import *
from utils import cls


# adding and deleting data
def add_worker(cursor):
    document_id = add_document(cursor)

    name = input("Please enter worker's name: ")
    last_name = input("Please enter worker's last name: ")

    while True:
        u_input = input("Please enter worker's position [0] admin; [1] worker: ")

        if u_input.isnumeric():
            if 0 <= int(u_input) <= 1:
                break

    if int(u_input) == 0:
        position = "'admin'"

    if int(u_input) == 1:
        position = "'worker'"

    query = "INSERT INTO Workers " \
            "VALUES" \
            "(NEXT VALUE FOR Workers_ID, '" + name + "', '" + last_name + "', " + position + ", '" + document_id + "');"

    cursor.execute(query)
    cursor.commit()

    print("\nNew", position, " ", name, " ", last_name, " was successfully added to database")
    sleep(2)


def delete_worker(sql_conn, cursor, curr_worker):
    name = input("Enter name of the worker to delete: ")
    last_name = input("Enter last name of the worker to delete: ")

    query = "SELECT * " \
            "FROM Workers " \
            "WHERE name = '" + name + "' and last_name = '" + last_name + "';"
    df = pd.read_sql(query, sql_conn)

    if df.empty:
        print("\nThere is no such worker")
        sleep(2)
        return

    print(df.to_string(), "\n")

    id_to_delete = input("Enter id to delete: ")

    if id_to_delete == curr_worker:
        print("\nYou cannot delete yourself")
        sleep(2)
        return

    if id_to_delete.isnumeric() is False:
        print("\nBad id")
        sleep(2)
        return

    query = "SELECT position " \
            "FROM Workers " \
            "WHERE name = '" + name + "' and last_name = '" + last_name + "' and worker_id = " + id_to_delete + ";"
    df = pd.read_sql(query, sql_conn)

    if df.iat[0, 0] == 'admin':
        print("\nYou are about to delete an admin, make sure there is at least another one")

    query = "DELETE " \
            "FROM Workers " \
            "WHERE name = '" + name + "' and last_name = '" + last_name + "' and worker_id = " + id_to_delete + ";"
    cursor.execute(query)
    cursor.commit()

    print("\nWorker ", name, " ", last_name, " was successfully deleted from database")
    sleep(2)


def add_document(cursor):
    while True:
        u_input = input(
            "Please choose id document type [0] id card; [1] driver's license; [2] student id: ")

        if u_input.isnumeric():
            if 0 <= int(u_input) <= 2:
                break
        print("\nInvalid input")
        sleep(2)
        cls()

    document_id = input("Please enter document id: ")

    while True:
        expiration_date = input("Please enter id document expiration_date [yyyy-mm-dd] : ")
        if check_date(expiration_date, True):
            break

    document_type = ""
    if int(u_input) == 0:
        document_type = "'id card'"

    if int(u_input) == 1:
        document_type = "'driver''s license'"

    if int(u_input) == 2:
        document_type = "'student id'"

    query = "INSERT INTO Documents " \
            "VALUES('" + document_id + "', '" + expiration_date + "' , " + document_type + ");"

    cursor.execute(query)
    cursor.commit()

    return document_id


def add_client(cursor):
    document_id = add_document(cursor)

    name = input("Please enter client's name: ")
    last_name = input("Please enter client's last name: ")

    query = "INSERT INTO Clients  " \
            "VALUES" \
            "(NEXT VALUE FOR Clients_ID, '" + name + "', '" + last_name + "', '" + document_id + "' , GETDATE());"

    cursor.execute(query)
    cursor.commit()

    print("\nClient ", name, " ", last_name, " was successfully added to database")
    sleep(2)


def delete_client(sql_conn, cursor):
    name = input("Enter name of the client to delete: ")
    last_name = input("Enter last name of the client to delete: ")

    query = "SELECT * " \
            "FROM Clients " \
            "WHERE name = '" + name + "' and last_name = '" + last_name + "';"

    df = pd.read_sql(query, sql_conn)
    if df.empty:
        print("There is no such client")
        return

    cls()
    print("\nList of potential clients:\n", df.to_string(), "\n")

    id_to_delete = input("Enter id to delete: ")

    query = "DELETE " \
            "FROM Clients " \
            "WHERE name = '" + name + "' and last_name = '" + last_name + "' and client_id = " + id_to_delete + ";"

    cursor.execute(query)
    cursor.commit()

    print("\nClient ", name, " ", last_name, " was successfully deleted from database")
    sleep(2)


def add_video(cursor):
    title = input("Enter the title: ")

    while True:
        premiere_date = input("Enter the premiere date [YYYY-MM-DD]: ")
        if check_date(premiere_date, False):
            break

    genre = input("Enter genre: ")
    director = input("Enter director of the movie: ")

    while True:
        duration = input("Enter duration of the movie [HH:MM:SS]: ")
        duration = check_duration(duration)
        if duration != 'False':
            break

    query = "INSERT INTO Videos  " \
            "VALUES" \
            "('" + title + "', '" + premiere_date + "', '" + genre + "', '" + director + "', '" + duration + "');"

    cursor.execute(query)
    cursor.commit()

    print("\nVideo ", title, " was successfully added to database")
    sleep(2)


def delete_video(sql_conn, cursor):
    title = input("Enter title of the movie you would like to delete: ")

    query = "SELECT title " \
            "FROM Videos " \
            "WHERE title = '" + title + "';"

    df = pd.read_sql(query, sql_conn)

    if df.empty:
        print("\nThere is no such video")
        sleep(2)
        return

    query = "DELETE " \
            "FROM Videos " \
            "WHERE title = '" + title + "';"

    try:
        cursor.execute(query)
        cursor.commit()

    except pyodbc.IntegrityError:
        print("Firstly delete products associated with the video!")

    print("\nVideo ", title, " was successfully deleted from database")
    sleep(4)


def add_product(sql_conn, cursor):
    while True:
        video_name = input("Enter the title of the movie: ")
        if is_video_available(video_name, sql_conn):
            break
        print("\nThere is no such video!")
        sleep(2)
        cls()

    while True:
        price = input("Enter the price of the movie: ")
        if check_price(price):
            break

    while True:
        u_input = input("Please enter video's medium [0] Blu-ray; [1] DVD; [2] HD-DVD: ")
        if u_input.isnumeric():
            if 0 <= int(u_input) <= 2:
                break

    if int(u_input) == 0:
        medium = "'Blu-ray'"

    if int(u_input) == 1:
        medium = "'DVD'"

    if int(u_input) == 2:
        medium = "'HD-DVD'"

    query = "INSERT INTO Products(product_id, video_name, price, medium)" \
            "VALUES" \
            "(NEXT VALUE FOR products_ID, '" + video_name + "', '" + price + "', " + medium + ");"

    cursor.execute(query)
    cursor.commit()

    print("\nCopy of ", video_name, " was successfully added to database")
    sleep(2)


def delete_product(sql_conn, cursor):
    name = input("Enter title of the product [q to abort]: ")

    if name.lower() == 'q':
        return

    query = "SELECT * " \
            "FROM Products " \
            "WHERE video_name = '" + name + "';"
    df = pd.read_sql(query, sql_conn)

    if df.empty:
        print("\nThere is no such product")
        sleep(2)
        return

    print("\nList of copies:\n", df.to_string(), "\n")

    id_to_delete = input("Enter id to delete: ")

    if id_to_delete.isnumeric() is False:
        print("\nBad id")
        sleep(2)
        return

    query = "SELECT product_id " \
            "FROM Products " \
            "WHERE product_id = " + id_to_delete + " AND is_available = 1;"
    df = pd.read_sql(query, sql_conn)

    if df.empty:
        print("\nThis product is rented!")
        sleep(2)
        return

    query = "DELETE FROM Order_Items WHERE " \
            "product_id = " + id_to_delete
    cursor.execute(query)
    cursor.commit()

    query = "DELETE " \
            "FROM Products " \
            "WHERE product_id = " + id_to_delete + " AND video_name = '" + name + "';"
    cursor.execute(query)
    cursor.commit()

    print("\nCopy of ", name, " was successfully deleted from database")
    sleep(2)


# Creating order
def find_client(sql_conn):
    client_id = input("Provide client's id [ls to list all clients, q to abort]: ")

    if client_id.lower() == 'q':
        return -2
    if client_id.lower() == 'ls':
        return -3

    if client_id.isnumeric() is False:
        return -1

    query = "SELECT client_id " \
            "FROM Clients " \
            "WHERE client_id = " + client_id + ";"

    df = pd.read_sql(query, sql_conn)
    if df.empty:
        return -1

    return df.at[0, 'client_id']


def disp_clients(sql_conn):
    query = "SELECT * FROM v_all_clients"

    df = pd.read_sql(query, sql_conn)

    print("\nList of clients:\n", df.to_string())


def add_order_item(sql_con, cursor, curr_order, name, medium):
    query = "SELECT MIN(product_id) as min FROM Products " \
            "WHERE video_name = '" + name + "' AND medium = '" + medium + "' AND is_available = 1"

    df = pd.read_sql(query, sql_con)

    if df['min'].isnull().values.any():
        print("\nThis video is unavailable on this medium")
        sleep(2)
        return

    product_id = str(df.iat[0, 0])
    query = "INSERT INTO Order_items VALUES" \
            "(" + curr_order + "," + product_id + ")"

    cursor.execute(query)
    cursor.commit()

    print("\nCopy of ", name, " was successfully added to order")
    sleep(2)


def add_order_items(sql_con, cursor):
    query = "SELECT MAX(order_id) FROM Orders"
    df = pd.read_sql(query, sql_con)

    curr_order = str(df.iat[0, 0])

    while True:
        cls()
        name = input("Hello, please specify product name [Q to end]: ")
        if name.lower() == 'q':
            break

        while True:
            medium = input("Please enter video's medium [0] Blu-ray; [1] DVD; [2] HD-DVD: ")

            if medium.isnumeric():
                if 0 <= int(medium) <= 2:
                    break

        if medium == '0':
            medium = "Blu-ray"

        if medium == '1':
            medium = "DVD"

        if medium == '2':
            medium = "HD-DVD"

        add_order_item(sql_con, cursor, curr_order, name, medium)

    query = "SELECT SUM(price) FROM Products WHERE product_id " \
            "IN( SELECT product_id FROM Order_items WHERE order_id = " + curr_order + ")"

    df = pd.read_sql(query, sql_con)
    total_sum = str(df.iat[0, 0])

    query = "UPDATE Orders SET total_cost = " + total_sum + " WHERE order_id = " + curr_order

    cursor.execute(query)
    cursor.commit()

    cls()
    print("\nOrder created successfully; Total charge: ", total_sum)
    input("Press any key to continue...")


def create_order(sql_conn, cursor, curr_worker):
    while True:
        cls()
        client_id = find_client(sql_conn)

        if client_id == -2:
            return

        if client_id == -3:
            disp_clients(sql_conn)
            input("Press any key to continue...")
            continue

        if client_id != -1:
            break

        print("\nThere is no such document id!")
        sleep(2)

    cls()
    while True:
        rental_period = input("Enter rental period [>= 7]: ")
        if rental_period.isnumeric():
            if int(rental_period) >= 7:
                break

    if rental_period == '7':
        query = "INSERT INTO Orders(order_id, client_id, worker_id) VALUES " \
                "(NEXT VALUE FOR Order_ID, " + str(client_id) + ", " + curr_worker + ");"
    else:
        query = "INSERT INTO Orders(order_id, client_id, worker_id, rental_period) VALUES " \
                "(NEXT VALUE FOR Order_ID, " + str(client_id) + "," + curr_worker + ", " + rental_period + ");"

    cursor.execute(query)
    cursor.commit()

    add_order_items(sql_conn, cursor)


# Finalising order
def calc_penalty(creation_date, rental_period):
    tmp = date.today()
    tmp_str = tmp.strftime("%Y-%m-%d")
    creation_date = creation_date.strftime("%Y-%m-%d")

    arr_date = datetime.strptime(creation_date, "%Y-%m-%d")
    curr_date = datetime.strptime(tmp_str, "%Y-%m-%d")

    delta = curr_date - arr_date

    if delta.days <= rental_period:
        return 0
    else:
        return (delta.days - rental_period) * 5


def finalise_order(sql_conn, cursor):
    response = view_pending_orders(sql_conn)
    if response == -1:
        return

    order_id = input("\nChoose which order to finalise: ")

    if order_id.isnumeric() is False:
        print("\nBad order id")
        sleep(2)
        cls()
        return

    query = "SELECT created_at, rental_period FROM Orders WHERE order_id = " + order_id + "AND state = 'pending' "
    df = pd.read_sql(query, sql_conn)

    if df.empty:
        print("\nOrder is already finalised ||  Not exists!")
        sleep(2)
        cls()
        return

    creation_date = df.at[0, 'created_at']
    rental_period = df.at[0, 'rental_period']

    penalty = calc_penalty(creation_date, rental_period)
    penalty = str(penalty)

    cls()
    print("\nTotal penalty is :", penalty)

    query = "UPDATE Orders SET state = 'finalised', penalty = " + penalty + " WHERE order_id = " + order_id

    cursor.execute(query)
    cursor.commit()

    print("\nOrder was successfully finalised")
    input("\nPress any key to continue...")


def view_pending_orders(sql_conn):
    while True:
        cls()
        client_id = input("Enter client's id [ls for client list, q to abort]: ")

        if client_id == "ls":
            disp_clients(sql_conn)
            input("\nPress any key to continue...")
            continue

        if client_id.lower() == "q":
            return -1

        if client_id.isnumeric() is False:
            print("\nBad client id")
            sleep(2)
            return -1

        break

    query = "SELECT Orders.*, Workers.name as worker_name, Workers.last_name as worker_last_name " \
            "FROM Orders JOIN Workers ON Workers.worker_id = Orders.worker_id " \
            "WHERE client_id = " + client_id + "AND state = 'pending' "

    df = pd.read_sql(query, sql_conn)

    cls()
    if df.empty:
        print("\nThere are none orders to finalise")
        input("\nPress any key to continue...")
        return -1

    print("\nList of orders:\n", df.to_string())
    input("\nPress any key to continue...")


def view_client_orders(sql_conn):
    while True:
        cls()
        client_id = input("Enter client's id [ls for client list, q to abort]: ")

        if client_id == "ls":
            disp_clients(sql_conn)
            input("\nPress any key to continue...")
            continue

        if client_id.lower() == "q":
            return

        break

    query = "SELECT Orders.*, Workers.name as worker_name, Workers.last_name as worker_last_name " \
            "FROM Orders JOIN Workers ON Workers.worker_id = Orders.worker_id " \
            "WHERE client_id = " + client_id

    df = pd.read_sql(query, sql_conn)

    cls()
    if df.empty:
        print("\nClient has no orders")
        input("\nPress any key to continue...")

    print("\nList of orders:\n", df.to_string())
    input("\nPress any key to continue...")


def view_name_product(sql_conn):
    name = input("Enter name of the video: ")

    query = "SELECT Products.product_id, Products.price, Products.medium, Products.is_available, Videos.* " \
            "FROM Products JOIN Videos ON Products.video_name = Videos.title " \
            "WHERE video_name = '" + name + "';"

    df = pd.read_sql(query, sql_conn)
    cls()

    if df.empty:
        print("\nThere is no such product in base")
        input("\nPress any key to continue...")
        return

    print("\nList of products:\n", df.to_string())
    input("\nPress any key to continue...")


def view_medium_product(sql_conn):
    while True:
        medium = input("Please enter video's medium [0] Blu-ray; [1] DVD; [2] HD-DVD: ")

        if medium.isnumeric():
            if 0 <= int(medium) <= 2:
                break

        print("\nInvalid input")
        sleep(2)
        cls()

    if medium == '0':
        medium = "'Blu-ray'"

    if medium == '1':
        medium = "'DVD'"

    if medium == '2':
        medium = "'HD-DVD'"

    query = "SELECT Products.product_id, Products.price, Products.medium, Products.is_available, Videos.* " \
            "FROM Products JOIN Videos ON Products.video_name = Videos.title " \
            "WHERE medium = " + medium + ";"

    df = pd.read_sql(query, sql_conn)
    cls()

    if df.empty:
        print("\nThere is no products on such medium in base")
        input("\nPress any key to continue...")
        return

    print("\nList of products:\n" + df.to_string())
    input("\nPress any key to continue...")


def choose_view_products(sql_conn):
    while True:
        choice = input("Would you like to display products on certain medium[0] or by certain name[1]?: ")

        if choice.isnumeric():
            if 0 <= int(choice) <= 2:
                break

        print("\nInvalid input")
        sleep(2)
        cls()

    cls()
    if int(choice) == 0:
        view_medium_product(sql_conn)

    if int(choice) == 1:
        view_name_product(sql_conn)


def views(sql_conn):
    while True:
        while True:
            cls()
            choice = input("Choose data to display: \n"
                           "[0] all finlised orders\n"
                           "[1] all workers\n"
                           "[2] all clients\n"
                           "[3] all products\n"
                           "[q] abort\n\n"
                           "Your choice: ")

            if choice.isnumeric():
                if 0 <= int(choice) <= 3:
                    break

            if choice.lower() == 'q':
                cls()
                return

        if int(choice) == 0:
            query = "SELECT *" \
                    "FROM v_all_fin_orders"
            df = pd.read_sql(query, sql_conn)
            print("\n List of all orders:\n")

        if int(choice) == 1:
            query = "SELECT *" \
                    "FROM v_all_workers"
            df = pd.read_sql(query, sql_conn)
            print("\n List of all workers:\n")

        if int(choice) == 2:
            query = "SELECT *" \
                    "FROM v_all_clients"
            df = pd.read_sql(query, sql_conn)
            print("\n List of all clients:\n")

        if int(choice) == 3:
            query = "SELECT *" \
                    "FROM v_all_products"
            df = pd.read_sql(query, sql_conn)
            print("\n List of all products:\n")

        if df.empty:
            print("\nThere is no such data in base")
            sleep(2)
            cls()
            return

        print(df.to_string())
        input("\nPress any key to continue...")
        cls()
