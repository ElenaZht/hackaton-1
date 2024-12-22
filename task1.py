from task import Task

def create_task_table(conn):
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

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def load_tasks(list_id, conn):
    list_tasks = []
    query = f'SELECT * FROM task WHERE list_id = {list_id}'
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                list_tasks.append(Task(task_id=row[0], task_desc=row[1], priority=row[2], estimation=row[3], is_done=row[4], list_id=row[5]))

    return list_tasks

def validate_description():
    while True:
        task_desc = input('Enter description of the task ').strip()
        if not task_desc:
            print('Not empty description')
        elif len(task_desc) > 100:
            print('Max 100 simbols')
        else:
            return task_desc

def validate_priority():
    while True:
        priority = input('Введите приоритет ("low", "medium", "high"): ').strip().lower()
        if priority not in ('low', 'medium', 'high'):
            print('Wrong priority. Input "low", "medium" or "high".')
        else:
            return priority

def validate_estimation():
    while True:
        try:
            estimation = int(input('Time from task ').strip())
            if estimation <= 0:
                print('Whole time')
            else:
                return estimation
        except ValueError:
            print('Input integer')

def show_task_menu(list_id, tasks, conn):
    tasks_dict = {t.task_id: t for t in tasks}
    priority_sigh = {'high': '🚨', 'medium': '❕', 'low': '✅'}
    for task in tasks:
        print(f"- {task.task_id} - {task.task_desc} - {task.estimation} {priority_sigh[task.priority]}")

    while True:
        task_id_option = input('Input ID of task or (X) for exit ').strip()
        if task_id_option == 'x':
            break
        if not task_id_option.isdigit():
            print('Wrong ID of task.')
            continue

        task_id_option = int(task_id_option)
        if task_id_option in tasks_dict:
            print(f'Задача с id {task_id_option}')
            while True:
                print('''
                    * (d) Delete task
                    * (u) Update task
                    * (s) Start task
                    * (x) Exit
                ''')
                task_option = input('Chose option ').strip().lower()
                if task_option == 'd':
                    tasks_dict[task_id_option].delete_task(conn)
                elif task_option == 'u':
                    task_desc = validate_description()
                    priority = validate_priority()
                    estimation = validate_estimation()
                    tasks_dict[task_id_option].update(task_desc, priority, estimation, conn)
                elif task_option == 's':
                    pass
                elif task_option == 'x':
                    break
                else:
                    print('Input correct option.')
        else:
            print('Input correct ID.')

def create_task_prompt(list_id, conn):
    task_desc = validate_description()
    priority = validate_priority()
    estimation = validate_estimation()
    t = Task(task_desc=task_desc, priority=priority, estimation=estimation, list_id=list_id)
    t.add_task(conn)