import psycopg2
import os 

def register(username, password):

    conn = psycopg2.connect(
        host="localhost",
        database="crypto_tracker",
        user="postgres",
        password=os.getenv('CWT_DB_PASS'))
    
    cur = conn.cursor()

    try:
        cur.execute(f"""INSERT INTO users (username, user_pwd, creation_date)
        values ('{username}', '{password}', CURRENT_DATE)    
        """)
    except:
        print(f'Username {username} already exist.')
        return False
    conn.commit()


    cur.execute(f"""SELECT * FROM users where username='{username}' and user_pwd='{password}'    
    """)
    
    user_data = cur.fetchall()

    print(user_data)

    conn.commit()

    cur.close()
    conn.close()

    return True

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
            return True
        else:
            return False
        
def get_id(username):
    conn = psycopg2.connect(
        host="localhost",
        database="crypto_tracker",
        user="postgres",
        password=os.getenv('CWT_DB_PASS'))
    
    cur = conn.cursor()

    cur.execute(f"""SELECT * FROM users WHERE username='{username}'    
    """)

    db_record = cur.fetchall()
    user_id = db_record[0][0]

    conn.commit()

    cur.close()
    conn.close()

    return user_id

# print(register("Many", "PawelJumper203"))
# print(log_in("Many", "PawelJumper203"))
# get_id('Many')