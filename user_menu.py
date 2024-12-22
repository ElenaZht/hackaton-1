def log_in(user_name, password, conn):
    pass
    return True

def sign_in(user_name, password, conn):
    pass



def show_user_menu(conn):
    user_option = ''
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
                print('you logged is successfuly')
                return True
            else:
                print('user name or password is incorrect, if you have no account, please, sign in')