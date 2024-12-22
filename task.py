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


    def add_task(self, conn):
        with conn.cursor() as cursor:
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


