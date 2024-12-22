from list import ToDoList
from task_menu import show_task_menu, create_task_prompt


def change_list_name(todo_list, conn):
    while True:
        new_name = input('enter new name: ')
        if new_name != '':
            todo_list.update_list_name(new_name, conn)
        else:
            print('invalid name, try again')

def add_new_list(connection, curr_user):
    while True:
        list_name = input('enter list name: ')
        if list_name != '':
            new_list = ToDoList(list_name, curr_user[0])
            new_list.save(connection)
            break
        else:
            print('invalid name, try again')

def create_list_table(conn):
    query = '''CREATE TABLE IF NOT EXISTS list (
    list_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT);'''
    with  conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def show_all_lists(conn, curr_user):
    todos_dict = {}
    query = f'SELECT * FROM list WHERE user_id = {curr_user[0]}'
    with  conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                l = ToDoList(row[1], row[2],row[0])
                print(f'{row[0]} - {row[1]}')
                todos_dict[l.list_id] = l
        else:
            print('you have no lists yet')
    return todos_dict   
    
#list menu
def show_list_menu(todo_list, conn):
    option = ''
    while True:
        print('''
            * (a) add new task
            * (u) update list name
            * (d) delete list
            * (s) show tasks
            * (x) exit
            ''')
        option = input('choose option: ')

        if option == 'a':
            create_task_prompt(todo_list.list_id, conn)

        elif option == 'u':
            change_list_name(todo_list, conn)
        
        elif option == 'd':
            todo_list.delete_list(conn)
            return

        elif option == 's':
            todo_list.show_list(conn)
            show_task_menu(todo_list.list_id, todo_list.tasks, conn)
            todo_list.show_progress()

        elif option == 'x':
            return
        else:
            print('choose valid option')