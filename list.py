class List:
    tasks = []

    def __init__(self, list_name):
        self.list_name = list_name
        #list id

    def show_list(self):
        '''displays all list tasks'''

        print(f'List {self.list_id} - {self.list_name}')
        for task in self.tasks:
            print(f'*{task.id} -{task.text} {task.priority} -{task.estimation}')
        
        self.show_progress()
    
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

    def update_list_name(self, new_name):
        '''updates list name'''
        self.list_name = new_name
        try:
            pass
            #todo: update list in db
        except Exception as e:
            print(e)
            return False
        return True
    
    def show_progress(self):
        '''display amount of completed tasks in list'''

        completed = 0
        for task in self.tasks:
            if task.is_done:
                completed += 1
        progres = completed / len(self.tasks) * 100
        #todo: call draw_progress(progres)
        

#other fanctions
def add_new_list():
    list_name = input('enter list name: ')
    return  List(list_name)

def delete_list():
    while True:
        id = int(input('enter list id: '))
        if isinstance(id, int):
            break
    return List.delete_list(id)
def change_list_name():
    id = int(input('enter list id: '))
    #todo: get list by id from db
    curr_list = {}
    new_name = input('enter new name: ')
    curr_list.update_list_name(new_name)

def show_list():
    id = int(input('enter list id: '))
    if isinstance(id, int):
        #list = get from db
        curr_list = {}
        curr_list.show_list()
    
    
#list menu
def show_list_menu():
    option = ''
    while True:
        print('''
            * (u) update list
            * (a) add new list
            * (d) delete list
            * (s) show list
            * (x) exit
            ''')
        option = input('chose option: ')
        if option == 'u':
            change_list_name()

        if option == 'a':
            add_new_list()
        
        if option == 'd':
            delete_list()

        if option == 's':
            show_list()
        
        if option == 'x':
            return
        else:
            print('chose valid option')