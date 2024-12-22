from list_menu import show_list_menu, add_new_list, show_all_lists, create_list_table
import psycopg2
from task_menu import create_task_table
from user_menu import show_user_menu


def show_main_menu(conn, curr_user):
    option = ''

    while option != 'x':
        print('''\n*** Just ToDo It ***\n 
            * (a)dd new list
            * (l) my lists
            * (x) exit \n''')
        
        option = input('choose option: ')
        if option == 'a':
            add_new_list(conn, curr_user)

        elif option == 'l':
            print('** My lists **')
            lists_dict = show_all_lists(conn, curr_user)
            while option != 'x':
                list_id = input('enter list id or (x) exit: ')
                if list_id == 'x':
                    break
                show_list_menu(lists_dict[int(list_id)], conn)
                
        elif option == 'x':
            return
        
        else:
            print('choose valid option')
        


def main():
    with  psycopg2.connect(
            dbname="todo",  # your DB name
            user="postgres",      # your username
            password="lena_postgres",  # your password
            host="localhost"      # your host (localhost for local machine)
        ) as conn:

        result = show_user_menu(conn)
        if result != None:
            create_list_table(conn)
            create_task_table(conn)
            show_main_menu(conn, result)




if __name__ == '__main__':
    main()