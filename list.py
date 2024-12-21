from task_menu import load_tasks


class ToDoList:
    tasks = []

    def __init__(self, list_name, list_id=None):
        self.list_name = list_name
        self.list_id = list_id
        

    def show_list(self, conn):
        '''displays all list tasks'''
        self.tasks = load_tasks(self.list_id, conn)

        print(f'List {self.list_id} - {self.list_name} {len(self.tasks)}')
            
    def save(self, conn):
        query = f"INSERT INTO list (name) VALUES ('{self.list_name}') returning *"
        with  conn.cursor() as cur:
            # execute the INSERT statement
            cur.execute(query)
            # get the generated id back
            row = cur.fetchone()
            if row:
                self.list_id = row[0]
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
            print(f"{progres}% is ready")
        #todo: call draw_progress(progres)
        
