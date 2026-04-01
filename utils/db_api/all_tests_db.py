from utils.db_api.create_db_tables import Database


class AllTestsDB:
    def __init__(self, db: Database):
        self.db = db

    # ======================= TABLE | EYSENC =======================
    async def add_eysencquestion(self, question_number, question):
        sql = "INSERT INTO eysenc_questions (question_number, question) VALUES ($1, $2)"
        return await self.db.execute(sql, question_number, question, execute=True)

    async def add_eysencscale(self, scale_type, question_number, yes, no_):
        sql = "INSERT INTO eysenc_scales (scale_type, question_number, yes, no) VALUES ($1, $2, $3, $4)"
        return await self.db.execute(sql, scale_type, question_number, yes, no_, fetchrow=True)

    async def get_status_eysenc(self, tg_id):
        sql = "SELECT EXISTS (SELECT 1 FROM eysencapp_eysencanswer WHERE telegram_id = $1)"
        return await self.db.execute(sql, tg_id, fetchval=True)

    # ======================= TABLE | LEONHARD =======================
    async def add_leoquestions(self, question_number, question):
        sql = "INSERT INTO leonhard_questions (question_number, question) VALUES ($1, $2)"
        return await self.db.execute(sql, question_number, question, fetchrow=True)

    async def add_leoscales(self, question_number, yes, no_, scale_type):
        sql = "INSERT INTO leonhard_scales (question_number, yes, no, scale_type) VALUES ($1, $2, $3, $4)"
        await self.db.execute(sql, question_number, yes, no_, scale_type, execute=True)

    async def get_status_leonhard(self, tg_id):
        sql = "SELECT EXISTS (SELECT 1 FROM leonhardapp_leonhardanswers WHERE telegram_id = $1)"
        return await self.db.execute(sql, tg_id, fetchval=True)

    # ======================= TABLE | QUESTIONNAIRE =======================
    async def add_questionnaires(self, question_number, question):
        sql = "INSERT INTO questionnaire_questions (question_number, question) VALUES ($1, $2)"
        return await self.db.execute(sql, question_number, question, fetchrow=True)

    async def get_status_questionnaire(self, tg_id):
        sql = "SELECT EXISTS (SELECT 1 FROM questionnaireapp_questionnaireanswers WHERE telegram_id = $1)"
        return await self.db.execute(sql, tg_id, fetchval=True)

    # ======================= TABLE | YAKHIN =======================
    async def add_yakhinquestion(self, scale_type, question_number, question):
        sql = """
        INSERT INTO yakhin_questions (scale_type, question_number, question) 
        VALUES ($1, $2, $3)
        """
        return await self.db.execute(sql, scale_type, question_number, question, execute=True)

    async def add_yakhinscale(self, scale_type, question_number, point_one, point_two, point_three, point_four,
                              point_five):
        sql = """
        INSERT INTO yakhinscales (scale_type, question_number, point_one, point_two, point_three, point_four, point_five) 
        VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *;
        """
        return await self.db.execute(sql, scale_type, question_number, point_one, point_two, point_three, point_four,
                                     point_five, fetchrow=True)

    async def get_status_yakhin(self, tg_id):
        sql = "SELECT EXISTS (SELECT 1 FROM yakhinapp_yakhinanswers WHERE telegram_id = $1)"
        return await self.db.execute(sql, tg_id, fetchval=True)
