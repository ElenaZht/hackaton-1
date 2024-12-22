from list import ToDoList
from task_menu import show_task_menu, create_task_prompt
from task import Task


def change_list_name(todo_list, conn):
    new_name = input('enter new name: ')
    todo_list.update_list_name(new_name, conn)

def add_new_list(connection):
    list_name = input('enter list name: ')
    new_list = ToDoList(list_name)
    new_list.save(connection)

def create_list_table(conn):
    #table list with list_id, name, user_id
    query = '''CREATE TABLE IF NOT EXISTS list (
    list_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT);'''
    with  conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def show_all_lists(conn):
    #get all existing lists from db
    todos_dict = {}
    #todo select where user_id
    query = 'SELECT * FROM list'
    with  conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                #create list object from table row, using dict for fast access
                l = ToDoList(row[1], row[0])
                # display created list
                l.show_list(conn)
                todos_dict[l.list_id] = l
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
            todo_list.show_progress()
            show_task_menu(todo_list.list_id, todo_list.tasks, conn)

        elif option == 'x':
            return
        else:
            print('choose valid option')