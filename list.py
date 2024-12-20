class List:
    tasks = []

    def __init__(self, list_name):
        self.list_name = list_name

    def show_list(self):
        '''displays all list tasks'''

        for task in self.tasks:
            print(f'*{task.id} -{task.text} {task.priority} -{task.estimation}')
    
    def add_list(self, list_name):
        '''add new empty todo list'''

        try:
            pass
            #todo: add list to db
        except Exception as e:
            print(e)
        return List(list_name)
        
    
    def delete_list(self, list_id):
        '''delete todo list, list tasks delete cascade'''

        try:
            pass
            #todo: delete list and its tasks from db
        except Exception as e:
            print('list not exist')
            return False
        return True

    def update_list(self, new_name):
        '''updates list name'''

        try:
            pass
            #todo: update list in db
        except Exception as e:
            print(e)
            return False
        return True
    
    def show_progress(self, list_id):
        '''display amount of completed tasks in list'''

        completed = 0
        for task in self.tasks:
            if task.is_done:
                completed += 1
        progres = completed / len(self.tasks) * 100
        #todo: call draw_progress(progres)
        

#wraper fanctions
def add_new_list():
    list_name = input('enter list name: ')
    return  List(list_name)

def delete_list():
    while True:
        id = int(input('enter list id: '))
        if isinstance(id, int):
            break
    return List.delete_list(id)

def update_list():
    while True:
        new_name = input('enter new list name: ')
        if new_name != '':
            break
    List.update_list(new_name)    
    