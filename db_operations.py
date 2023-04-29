import psycopg2
from user_class import User
import os 

def register(username, password):
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_tracker",
        user="postgres",
        password=os.getenv('CWT_DB_PASS'))
    
    cur = conn.cursor()

    cur.execute(f"""INSERT INTO users (username, user_pwd, creation_date)
    values ("{username}", "{password}", CURRENT_DATE)    
    """)

    conn.commit()

    
    cur.execute(f"""SELECT * FROM users where username='{username}' and password='{password}'    
    """)
    
    user_data = cur.fetchall()

    print(user_data)

    conn.commit()

    cur.close()
    conn.close()


def log_in(username, password):
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_tracker",
        user="postgres",
        password=os.getenv('CWT_DB_PASS'))
    
    cur = conn.cursor()
    try:
        cur.execute(f"""SELECT * FROM users WHERE username='{username}' and user_pwd='{password}'    
        """)
    except:
        return 'something went wrong, try again'     
    
    else:
        db_record = cur.fetchall()

        print(db_record)    

        conn.commit()

        cur.close()
        conn.close()

        if len(db_record) > 0:
            return f'{username} logged succesfully'
        else:
            return 'there is no such user, please try once again'

register("mariusz", "PawelJumper203")
