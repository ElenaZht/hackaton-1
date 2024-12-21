class ToDoList:
    tasks = []

    def __init__(self, list_name, list_id=None):
        self.list_name = list_name
        self.list_id = list_id
        

    def show_list(self):
        '''displays all list tasks'''

        print(f'List {self.list_id} - {self.list_name}')
        for task in self.tasks:
            print(f'*{task.id} -{task.text} {task.priority} -{task.estimation}')
        
        self.show_progress()
    
    def save(self, conn):
        query = f"INSERT INTO list (name) VALUES ('{self.list_name}') returning *"
        with  conn.cursor() as cur:
            # execute the INSERT statement
            cur.execute(query)
            # get the generated id back
            row = cur.fetchone()
            if row:
                self.list_id = row[1]
                print(f'list {self.list_name} added successfuly')
            conn.commit()

    
    def delete_list(self, conn):
        '''delete todo list, list tasks delete cascade'''
        query = f"DELETE FROM list WHERE list_id = {self.list_id};"

        try:
            with  conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

        except Exception as e:
            raise e
            return False
        return True

    def update_list_name(self, new_name, conn):
        '''updates list name'''
        
        query = f'''
            UPDATE list
            SET name = '{new_name}'
            WHERE list_id = {self.list_id};
            '''
        try:
            with  conn.cursor() as cur:
                cur.execute(query)
                self.list_name = new_name
                conn.commit()
        except Exception as e:
            print(e)
            raise e
            # return False
        return True
    
    def show_progress(self):
        '''display amount of completed tasks in list'''
        if len(self.tasks) > 0:
            completed = 0
            for task in self.tasks:
                if task.is_done:
                    completed += 1
            progres = completed / len(self.tasks) * 100
        #todo: call draw_progress(progres)
        

def change_list_name(todo_list, conn):
    new_name = input('enter new name: ')
    todo_list.update_list_name(new_name, conn)

def add_new_list(connection):
    list_name = input('enter list name: ')
    new_list = ToDoList(list_name)
    new_list.save(connection)

def init_db(conn):
    query = '''CREATE TABLE IF NOT EXISTS list (
    name VARCHAR(100) NOT NULL,
    list_id SERIAL,
    user_id INT);'''
    with  conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def show_all_lists(conn):
    todos_dict = {}
    query = 'SELECT * FROM list'
    with  conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                l = ToDoList(row[0], row[1])
                l.show_list()
                todos_dict[l.list_id] = l
        conn.commit()
    return todos_dict   
    
#list menu
def show_list_menu(todo_list, conn):
    option = ''
    while True:
        print('''
            * (u) update list
            * (d) delete list
            * (s) show list
            * (x) exit
            ''')
        option = input('chose option: ')
        if option == 'u':
            change_list_name(todo_list, conn)
        
        if option == 'd':
            todo_list.delete_list(conn)
            return

        if option == 's':
            todo_list.show_list()
        
        if option == 'x':
            return
        else:
            print('chose valid option')