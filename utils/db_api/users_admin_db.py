from utils.db_api.create_db_tables import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== TABLE | USERS ==========================
    async def add_user(self, telegram_id, fullname, username):
        sql = "INSERT INTO bot_users (telegram_id, fullname, username) VALUES($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING"
        return await self.db.execute(sql, telegram_id, fullname, username, execute=True)

    async def add_user_json(self, telegram_id, fio, phone):
        sql = "INSERT INTO bot_users (telegram_id, fio, phone) VALUES($1, $2, $3)"
        return await self.db.execute(sql, telegram_id, fio, phone, execute=True)

    async def update_user_info(self, telegram_id, age, gender):
        sql = """
        INSERT INTO bot_users (telegram_id, age, gender)
        VALUES ($1, $2, $3)
        ON CONFLICT (telegram_id)
        DO UPDATE SET age = EXCLUDED.age, gender = EXCLUDED.gender;
        """
        return await self.db.execute(sql, telegram_id, age, gender, execute=True)

    async def set_fullname(self, fullname, telegram_id):
        sql = """UPDATE clinic_patient SET name = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, fullname, telegram_id, execute=True)

    async def set_gender(self, gender, telegram_id):
        sql = """UPDATE bot_users SET gender = $1 WHERE telegram_id = $2"""
        return await self.db.execute(sql, gender, telegram_id, execute=True)

    async def set_age(self, age, telegram_id):
        sql = """UPDATE bot_users SET age = $1 WHERE telegram_id = $2"""
        return await self.db.execute(sql, age, telegram_id, execute=True)

    async def set_phone(self, phone, telegram_id):
        sql = """UPDATE clinic_patient SET phone = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, phone, telegram_id, execute=True)

    async def set_marital_status(self, marital_status, telegram_id):
        sql = """UPDATE clinic_patient SET marital_status = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, marital_status, telegram_id, execute=True)

    async def set_absence_children(self, absence_children, telegram_id):
        sql = """UPDATE clinic_patient SET absence_children = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, absence_children, telegram_id, execute=True)

    async def set_work(self, work, telegram_id):
        sql = """UPDATE clinic_patient SET work = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, work, telegram_id, execute=True)

    async def set_result_eeg(self, result_eeg, telegram_id):
        sql = """UPDATE clinic_patient SET result_eeg = $1 WHERE tg_id = $2"""
        return await self.db.execute(sql, result_eeg, telegram_id, execute=True)

    async def set_full_name(self, full_name, telegram_id):
        sql = """
            UPDATE bot_users SET fullname = $1 WHERE telegram_id = $2
            """
        await self.db.execute(sql, full_name, telegram_id, execute=True)

    async def set_username(self, username, telegram_id):
        sql = """
            UPDATE bot_users SET username = $1 WHERE telegram_id = $2
            """
        await self.db.execute(sql, username, telegram_id, execute=True)

    async def select_all_users(self):
        sql = "SELECT * FROM bot_users"
        return await self.db.execute(sql, fetch=True)

    async def select_user(self, telegram_id):
        sql = f"SELECT * FROM bot_users WHERE telegram_id='{telegram_id}'"
        return await self.db.execute(sql, fetchrow=True)

    async def get_user_gender_age(self, telegram_id):
        sql = f"SELECT gender, age FROM bot_users WHERE telegram_id=$1"
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def check_user(self, telegram_id):
        sql = f"""
            SELECT EXISTS (
                SELECT 1 FROM bot_users 
                WHERE telegram_id = $1 
                AND gender IS NOT NULL 
                AND age IS NOT NULL
            )
        """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM bot_users"
        return await self.db.execute(sql, fetchval=True)

    async def delete_user(self, telegram_id):
        await self.db.execute(f"DELETE FROM bot_users WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_users(self):
        await self.db.execute("DROP TABLE bot_users", execute=True)
