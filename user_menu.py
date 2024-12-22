def create_users_table(conn):
    query = '''CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL);'''

    with  conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def log_in(user_name, password, conn):
    if user_name == '' or password == '':
        return False
    try:
        query = '''
            SELECT * FROM users
            WHERE user_name = %s AND password = %s;
            '''
        with conn.cursor() as cur:
                cur.execute(query, (user_name, password)) 
                result = cur.fetchone()  # None if no match

        if result:  # If result is not None, login is successful
            return result
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def sign_in(user_name, password, conn):
    try:
        # Check if the username already exists
        query_check = '''
        SELECT * FROM users WHERE user_name = %s;
        '''
        with conn.cursor() as cur:
            cur.execute(query_check, (user_name,))
            result = cur.fetchone()
            if result:
                print("Username already exists. Please choose a different username.")
                return False

        # Insert the new user into the database
        query_insert = '''
        INSERT INTO users (user_name, password)
        VALUES (%s, %s);
        '''
        with conn.cursor() as cur:
            cur.execute(query_insert, (user_name, password))
            result = cur.fetchone()
            if result:
                return result
            conn.commit()

        print("Sign-up successful! You can now log in.")
        return True
    except Exception as e:
        print(f"An error occurred during sign-up: {e}")
        return False

def show_user_menu(conn):
    #create users table if not exist
    create_users_table(conn)
    user_option = ''
    result = None

    while True:
        print(''' **Hello! This is Just ToDo It!***
                * (s) sing up
                * (l) log in
                * (x) exit
            ''')
        user_option = input('choose option: ')
        if user_option == 'x':
            print('Goodbuy! See you soon.')
            return False

        elif user_option == 'l':
            user_name = input('enter user name or (x) exit: ')
            if user_name == 'x':
                continue

            password = input('enter your password or (x) exit: ')
            if password == 'x':
                continue

            result = log_in(user_name, password, conn)
            if result:
                print('you logged in successfuly')
                return result
            else:
                print('user name or password is incorrect, if you have no account, please, sign in')
        elif user_option == 's':
            user_name = input('enter user name or (x) exit: ')
            if user_name == 'x':
                continue

            password = input('enter your password or (x) exit: ')
            if password == 'x':
                continue

            result = sign_in(user_name, password, conn)
            if result:
                print('you signed in successfuly')
                return result
