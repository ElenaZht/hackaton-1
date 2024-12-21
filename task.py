import psycopg2
from datetime import datetime

#connection is created in main and pass to list and task as argument in order to use one connection
# def get_db_connection():             
#     connection = psycopg2.connect(
#         dbname="JustToDoIt",
#         user="postgres",
#         password="bob",
#         host="localhost",
#         port="5432"
#     )
#     return connection


class Task:
    def __init__(self, task_id=None, task_desc="", priority="low", estimation=20, is_done=False, list_id=None):
        self.task_id = task_id
        self.task_desc = task_desc
        self.priority = priority
        # self.time = time if time else datetime.now()
        self.estimation = estimation
        self.is_done = is_done
        self.list_id = list_id

    def task_status(self):
        return "Done" if self.is_done else "Not Done"

    # def update_task(self, task_desc=None, priority=None, time=None):

    #     try:
    #         if not self.task_id:
    #             print("Error: Task ID is not set. Can't update task.")
    #             return

    #         connection = psycopg2.connect(
    #             dbname="JustToDoIt",
    #             user="postgress",
    #             password="bob",
    #             host="localhost",
    #             port="5432"
    #         )
    #         cursor = connection.cursor()

    #         query = "UPDATE \"Task\" SET "
    #         params = []
    #         if task_desc:
    #             query += "task_desc = %s, "
    #             params.append(task_desc)
    #         if priority:
    #             query += "priority = %s, "
    #             params.append(priority)
    #         if time:
    #             query += "time = %s, "
    #             params.append(time)

    #         query = query.rstrip(", ")
    #         query += " WHERE task_id = %s"
    #         params.append(self.task_id)

    #         cursor.execute(query, tuple(params))
    #         connection.commit()

    def add_task(self, conn):

        # connection = get_db_connection()  pass connection as argument
        with conn.cursor() as cursor:

        # no descriptin uniqueness defined, every task id is unique
        # cursor.execute("""
        #     SELECT task_id FROM "Task" WHERE task_desc = %s AND time = %s AND list_id = %s
        # """, (self.task_desc, self.time, self.list_id))

        # existing_task = cursor.fetchone()

        # if existing_task:
        #     self.task_id = existing_task[0]
        #     print(
        #         f"Task with description '{self.task_desc}' and time '{self.time}' already exists with ID {self.task_id}.")
        # else:


            # INSERT INTO "Task" (description, priority, estimation, is_done, list_id) not valit table name syntax
            cursor.execute("""
                INSERT INTO task (description, priority, estimation, is_done, list_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING task_id
            """, (self.task_desc, self.priority, self.estimation, self.is_done, self.list_id))
            self.task_id = cursor.fetchone()[0]
            print(f"Task added with ID {self.task_id}")

        conn.commit()

    def delete_task(self, conn):
        if not self.task_id:
            print("Task ID is not set. Cannot delete.")
            return

        # connection = get_db_connection()
        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM task WHERE task_id = %s
            """, (self.task_id,))
            conn.commit()

            print(f"Task with ID {self.task_id} has been deleted.")

            # cursor.close()        no need with 'with' statement
            # connection.close()    connection handaled by main

    def show_task(self):
        return {
            "task_id": self.task_id,
            "task_desc": self.task_desc,
            "priority": self.priority,
            "time": self.time,
            "is_done": self.task_status()
        }
    
    def update(self, task_desc, priority, estimation, conn):
        query = f'''
            UPDATE task
            SET description = '{task_desc}', priority = '{priority}', estimation = {estimation}
            WHERE task_id = {self.task_id};
            '''
        try:
            with  conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
        except Exception as e:
            print(e)
            raise e
        return True


# todo_list = List(list_name="My ToDo List")
# todo_list.add_list()

# task1 = Task(task_desc="Finish anything", priority="middle", time=datetime(2024, 12, 31, 23, 59), list_id=todo_list.list_id)

# task2 = Task(task_desc="Eat pasta", priority="low", time=datetime(2024, 12, 31, 23, 59), list_id=todo_list.list_id)

# task3 = Task(task_desc="play with fish", priority="high", time=datetime(2024, 12, 31, 23, 59), list_id=todo_list.list_id)


