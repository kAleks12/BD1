from datetime import date
import time
import pandas as pd


def check_date(date_to_check: str, check_curr: bool = False):
    split_date = date_to_check.split('-')

    if len(split_date) < 3:
        return False

    day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if int(split_date[0]) % 4 == 0 and (int(split_date[0]) % 100 != 0 or int(split_date[0]) % 400 == 0):
        day_count_for_month[2] = 29

    if 1 <= int(split_date[1]) <= 12 and 1 <= int(split_date[2]) <= day_count_for_month[int(split_date[1])]:
        # Checking whether the date is older than current
        if check_curr:
            curr_date = date.today()
            curr_date_str = curr_date.strftime("%Y-%m-%d")

            for_curr_date = time.strptime(curr_date_str, "%Y-%m-%d")
            for_arr_date = time.strptime(date_to_check, "%Y-%m-%d")

            return for_arr_date > for_curr_date
        return True

    return False


def check_duration(duration: str):
    split_duration = duration.split(':')

    for part in split_duration:
        if part.isnumeric() is False:
            return 'False'

    if len(split_duration) == 2:
        if int(split_duration[0]) > 24 or int(split_duration[1]) > 59:
            return 'False'

        if int(split_duration[0]) == 24 and int(split_duration[1]) > 0:
            return 'False'

        split_duration.append('00')

        return ':'.join(split_duration)

    if len(split_duration) == 1:
        if int(split_duration[0]) > 23:
            return 'False'

        split_duration.append('00:00')

        return ':'.join(split_duration)

    if int(split_duration[0]) > 24 or int(split_duration[1]) > 59 or int(split_duration[2]) > 59:
        return 'False'

    if int(split_duration[0]) == 24 and int(split_duration[1]) > 0 and int(split_duration[2]) > 0:
        return 'False'

    return ':'.join(split_duration)


def is_video_available(video_name: str, sql_conn):
    query = "SELECT title " \
            "FROM Videos " \
            "WHERE title = '" + video_name + "';"

    df = pd.read_sql(query, sql_conn)

    if df.empty:
        return False

    return True


def check_price(price: str):
    if price.isnumeric():
        if int(price) > 0:
            return True

    return False
