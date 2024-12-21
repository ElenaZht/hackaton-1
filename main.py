from list import show_list_menu, add_new_list, show_all_lists, init_db
import psycopg2


def show_main_menu(conn):
    option = ''

    while option != 'x':
        print('''\n*** Just ToDo It ***\n 
            * (a)dd new list
            * (l) my lists
            * (x) exit \n''')
        
        option = input('chose option: ')
        if option == 'a':
            add_new_list(conn)

        elif option == 'l':
            print('** My lists **')
            lists_dict = show_all_lists(conn)
            list_id = int(input('enter list id or (x) exit: '))
            if list_id == 'x':
                return
            show_list_menu(lists_dict[list_id], conn)

        elif option == 'x':
            return
        
        else:
            print('chose valid option')
        


def main():
    conn = psycopg2.connect(
            dbname="todo",  # your DB name
            user="postgres",      # your username
            password="lena_postgres",  # your password
            host="localhost"      # your host (localhost for local machine)
        )
    init_db(conn)
    show_main_menu(conn)




if __name__ == '__main__':
    main()