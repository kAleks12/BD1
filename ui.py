from database_ops import *
from utils import cls


def admin_menu(sql_conn, cursor, curr_worker):
    while True:
        cls()
        action = input("(Admin menu)\n"
                       "Welcome! What would you like to do?\n"
                       "[0] add client\n"
                       "[1] delete client\n"
                       "[2] add video\n"
                       "[3] delete video\n"
                       "[4] add product\n"
                       "[5] delete product\n"
                       "[6] create order\n"
                       "[7] finalise order\n"
                       "[8] display client's orders\n"
                       "[9] display available products\n"
                       "[10] views\n"
                       "[11] add worker\n"
                       "[12] delete worker\n"
                       "[13] logout\n\n"
                       "Your choice: "
                       )
        cls()

        if action == '0':
            add_client(cursor)

        if action == '1':
            delete_client(sql_conn, cursor)

        if action == '2':
            add_video(cursor)

        if action == '3':
            delete_video(sql_conn, cursor)

        if action == '4':
            add_product(sql_conn, cursor)

        if action == '5':
            delete_product(sql_conn, cursor)

        if action == '6':
            create_order(sql_conn, cursor, curr_worker)

        if action == '7':
            finalise_order(sql_conn, cursor)

        if action == '8':
            view_client_orders(sql_conn)

        if action == '9':
            choose_view_products(sql_conn)

        if action == '10':
            views(sql_conn)

        if action == '11':
            add_worker(cursor)

        if action == '12':
            delete_worker(sql_conn, cursor, curr_worker)

        if action == '13':
            return


def worker_menu(sql_conn, cursor, curr_worker):
    while True:
        cls()
        action = input("(Worker menu)\n"
                       "Welcome! What would you like to do?\n"
                       "[0] add client\n"
                       "[1] delete client\n"
                       "[2] add video\n"
                       "[3] delete video\n"
                       "[4] add product\n"
                       "[5] delete product\n"
                       "[6] create order\n"
                       "[7] finalise order\n"
                       "[8] display client's orders\n"
                       "[9] display available products\n"
                       "[10] logout\n\n"
                       "Your choice: "
                       )
        cls()

        if int(action) == 0:
            add_client(cursor)

        if int(action) == 1:
            delete_client(sql_conn, cursor)

        if int(action) == 2:
            add_video(cursor)

        if int(action) == 3:
            delete_video(sql_conn, cursor)

        if int(action) == 4:
            add_product(sql_conn, cursor)

        if int(action) == 5:
            delete_product(sql_conn, cursor)

        if int(action) == 6:
            create_order(sql_conn, cursor, curr_worker)

        if int(action) == 7:
            finalise_order(sql_conn, cursor)

        if int(action) == 8:
            view_client_orders(sql_conn)

        if int(action) == 9:
            choose_view_products(sql_conn)

        if int(action) == 10:
            return


def start_menu(sql_conn, cursor):
    while True:
        name = input("Login to database\n\nEnter your name: ")
        last_name = input("Enter your last name: ")

        # name = 'Adam'
        # last_name = 'Nawałka'

        query = "SELECT * " \
                "FROM Workers " \
                "WHERE name = '" + name + "' and last_name = '" + last_name + "';"

        df = pd.read_sql(query, sql_conn)
        if df.empty:
            print("\nYou are not in the database and cannot modify data")
            sleep(2)
            cls()
            continue

        query = "SELECT position " \
                "FROM Workers " \
                "WHERE name = '" + name + "' " \
                "and " \
                "last_name = '" + last_name + "' " \
                "and " \
                "position = 'admin';"

        df = pd.read_sql(query, sql_conn)

        if df.empty:
            is_admin = False
        else:
            is_admin = True

        while True:
            id_to_check = input("Please enter your document's id [q to abort]: ")
            # id_to_check = 'DAJ123456'

            if id_to_check.lower() == 'q':
                cls()
                break

            query = "SELECT worker_id " \
                    "FROM Workers " \
                    "WHERE name = '" + name + "' " \
                    "AND last_name = '" + last_name + "'" \
                    "AND document_id = '" + id_to_check + "';"

            df = pd.read_sql(query, sql_conn)

            if df.empty:
                print("\nWrong document id!")
                sleep(2)
                cls()
                print("(", name, " ", last_name, ")")
                continue

            curr_worker = str(df.at[0, 'worker_id'])

            if is_admin:
                if df.empty is False:
                    admin_menu(sql_conn, cursor, curr_worker)
                    break

            else:
                if df.empty is False:
                    worker_menu(sql_conn, cursor, curr_worker)
                    break
