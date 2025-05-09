import pymysql
import functools
import datetime
import env

def DB(func):
    @functools.wraps(func)
    def dbConnection(*args, **kwargs):
        conn = pymysql.connect(
            host=env.host,
            user=env.user,
            password=env.password,
            database=env.database
        )

        kwargs["conn"] = conn
        kwargs["current_date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        result = func(*args, **kwargs)

        conn.close()
        return result

    return dbConnection
