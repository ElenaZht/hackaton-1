from task import Task


def create_task_table(conn):
    #table with task_id, description, priority, estimation, is_done, list_id as foreign key
    query = '''
    DO $$
        BEGIN
        IF NOT EXISTS (
            SELECT 1 
            FROM pg_type 
            WHERE typname = 'priority_level'
        ) THEN
            CREATE TYPE priority_level AS ENUM ('low', 'medium', 'high');
        END IF;
    END $$;

    CREATE TABLE IF NOT EXISTS task (
    task_id SERIAL PRIMARY KEY,
    description VARCHAR(100) NOT NULL,
    priority priority_level DEFAULT 'low',
    estimation INT DEFAULT 20,
    is_done BOOLEAN DEFAULT FALSE,
    list_id INT NOT NULL,
    FOREIGN KEY (list_id) REFERENCES list(list_id) ON DELETE CASCADE);'''

    with  conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def load_tasks(list_id, conn):
    list_tasks = []
    query = f'SELECT * FROM task WHERE list_id = {list_id}'
    with  conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        
        if rows:
            for row in rows:
                list_tasks.append(Task(task_id=row[0], task_desc=row[1], priority=row[2], estimation=row[3], is_done=row[4], list_id=row[5])) 
    
    return list_tasks
                

def show_task_menu(list_id, tasks, conn):
    # create dict for fast access
    tasks_dict = {t.task_id: t for t in tasks}
    for task in tasks:
        print(f"- {task.task_id} - {task.task_desc} - {task.estimation}")
    
    while True:
        task_id_option = input('enter task id or (x) exit: ')
        if task_id_option == 'x':
            break
        try:
            task_id_option = int(task_id_option)
        except Exception as e:
            print('enter valid id')
            continue
        if task_id_option in tasks_dict:
            print(f'task id {task_id_option}')
            while True:
                print('''
                    * (d) delete task
                    * (u) update task
                    * (s) start task
                    * (x) exit
                    ''')
                task_option = input('choose option: ')
                if task_option == 'd':
                    tasks_dict[task_id_option].delete_task(conn)

                elif task_option == 'u':
                    task_desc = input('enter task description: ')
                    priority = input('enter priority ("low", "medium", "high"): ')
                    estimation = int(input('enter estimation: '))
                    tasks_dict[task_id_option].update(task_desc, priority, estimation, conn)

                elif task_option == 's':
                    pass
                #todo start task func

                elif task_option == 'x':
                    break

                else:
                    print('enter valid option')
        else:
            print('enter valid id')
        
        

def create_task_prompt(list_id, conn):
    #todo: add input validation
    task_desc = input('enter task description: ')
    priority = input('enter priority ("low", "medium", "high"): ')
    estimation = int(input('enter estimation: '))
    t = Task(task_desc=task_desc, priority=priority, estimation=estimation, list_id=list_id)
    t.add_task(conn)
