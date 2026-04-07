from utils.db_api.create_db_tables import Database


class AdditionalDB:
    def __init__(self, db: Database):
        self.db = db

    # =========================== PATIENT DATAS ===========================
    async def get_patient(self, telegram_id):
        sql = """SELECT * FROM clinic_patient WHERE tg_id = $1"""
        return await self.db.execute(sql, telegram_id, fetchrow=True)

    async def get_patient_telegram_by_id(self, patient_id):
        sql = """
            SELECT tg_id FROM clinic_patient WHERE id = $1
            """
        return await self.db.execute(sql, patient_id, fetchval=True)

    async def get_patient_by_id(self, row_id):
        sql = """
            SELECT * FROM clinic_patient WHERE id = $1
            """
        return await self.db.execute(sql, row_id, fetchrow=True)

    async def check_patient(self, telegram_id):
        sql = """
                SELECT EXISTS (SELECT 1 FROM clinic_patient WHERE tg_id=$1)
                """
        return await self.db.execute(sql, telegram_id, fetchval=True)

    # async def get_patient_by_id(self, patient_id):
    #     sql = """SELECT tg_id, name FROM clinic_patient WHERE id = $1"""
    #     return await self.db.execute(sql, patient_id, fetchrow=True)

    async def add_patient(self, telegram_id, name, phone, marital_status, absence_children, work, result_eeg):
        tg = str(telegram_id)

        existing_sql = "SELECT id FROM clinic_patient WHERE tg_id = $1"

        existing_id = await self.db.execute(existing_sql, tg, fetchval=True)

        if existing_id:
            return existing_id

        insert_sql = """
            INSERT INTO clinic_patient (
                tg_id, name, phone, gender, age, marital_status, absence_children, work, result_eeg
            )
            SELECT 
                $1::VARCHAR, $2::VARCHAR, $3::VARCHAR, gender, age,
                $4::VARCHAR, $5::VARCHAR, $6::VARCHAR, $7::VARCHAR
            FROM bot_users
            WHERE telegram_id = $1::VARCHAR
            RETURNING id;
        """

        patient_id = await self.db.execute(
            insert_sql,
            tg,  # $1
            name,  # $2
            phone,  # $3
            marital_status,  # $4
            absence_children,  # $5
            work,  # $6
            result_eeg,  # $7
            fetchval=True
        )

        return patient_id

    async def cancel_appointment(self, appointment_id):
        sql = """
                DELETE FROM clinic_appointment WHERE id = $1
            """
        await self.db.execute(sql, appointment_id, execute=True)

    async def delete_patient_datas(self, patient_id):
        await self.db.execute("""DELETE FROM clinic_patient WHERE id = $1""", patient_id, execute=True)

    # =========================== DOCTOR DATAS ===========================
    async def get_doctor_id(self):
        sql = """ SELECT id FROM clinic_doctor WHERE name = 'Gavhar Darvish' """
        return await self.db.execute(sql, fetchval=True)

    async def get_doctor_work_days(self):
        sql = """SELECT wd.id, wd.code, wd.name, wd.start_hour, wd.end_hour FROM clinic_workday wd 
            JOIN clinic_doctor d ON wd.doctor_id = d.id WHERE d.name = 'Gavhar Darvish' ORDER BY wd.start_hour"""
        return await self.db.execute(sql, fetch=True)

    async def get_doctor_time(self, formatted_date: str):
        sql = """
            SELECT
                TO_CHAR(
                    a.appointment_date AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tashkent',
                    'HH24:MI'
                ) AS appointment_time
            FROM clinic_appointment a
            JOIN clinic_doctor d ON a.doctor_id = d.id
            WHERE (a.appointment_date AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tashkent')::date = $1
              AND d.name = 'Gavhar Darvish'
            ORDER BY a.appointment_date
        """
        return await self.db.execute(sql, formatted_date, fetch=True)

    # =========================== APPOINTMENTS ===========================
    async def add_to_appointments(self, patient_id, consultation_duration, age_group, appointment_date):
        sql = """INSERT INTO clinic_appointment 
                 (patient_id, doctor_id, company_id, service_type_id, consultation_duration, age_group, appointment_date) 
                 VALUES ($1, 1, 1, 1, $2, $3, $4) 
                 RETURNING id"""
        return await self.db.execute(sql, patient_id, consultation_duration, age_group, appointment_date, fetchval=True)

    async def get_patient_treatment_stage(self, patient_id):
        sql = """
            SELECT 
                TO_CHAR(appointment_date AT TIME ZONE 'Asia/Tashkent', 'HH24:MI | DD.MM.YYYY') AS appointment_date, 
                CASE treatment_stage 
                    WHEN 'before' THEN 'Oldin' 
                    WHEN 'after' THEN 'Keyin' 
                    ELSE 'Birinchi qabul' 
                END AS treatment_stage 
            FROM clinic_appointment 
            WHERE patient_id = $1
        """
        return await self.db.execute(sql, patient_id, fetch=True)

    async def get_appointment_datas(self):
        sql = """
                    SELECT patient_id, consultation_duration, appointment_date
                        FROM clinic_appointment
                        WHERE appointment_date::date = CURRENT_DATE + INTERVAL '1 day'
                        ORDER BY appointment_date;
                    """
        return await self.db.execute(sql, fetch=True)

    async def set_appointment(self, treatment_stage, appointment_id):
        sql = """
            UPDATE clinic_appointment
            SET treatment_stage = $1,
                display_name = 'Konsultasiya | Gavhar Darvish | ' 
                               || TO_CHAR(appointment_date, 'DD.MM.YYYY')
            WHERE id = $2
            RETURNING appointment_date AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tashkent'
        """
        return await self.db.execute(sql, treatment_stage, appointment_id, fetchval=True)

    # ==================== CLINIC_PATIENT ====================
    async def set_patient_fullname(self, fullname, telegram_id):
        sql = """
            UPDATE clinic_patient SET name = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, fullname, telegram_id, execute=True)

    async def set_patient_gender(self, gender, telegram_id):
        sql = """
            UPDATE clinic_patient SET gender = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, gender, telegram_id, execute=True)

    async def set_patient_age(self, age, telegram_id):
        sql = """
            UPDATE clinic_patient SET age = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, age, telegram_id, execute=True)

    async def set_patient_phone(self, phone, telegram_id):
        sql = """
            UPDATE clinic_patient SET phone = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, phone, telegram_id, execute=True)

    async def set_patient_marital_status(self, marital_status, telegram_id):
        sql = """
            UPDATE clinic_patient SET marital_status = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, marital_status, telegram_id, execute=True)

    async def set_patient_absence_children(self, absence_children, telegram_id):
        sql = """
            UPDATE clinic_patient SET absence_children = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, absence_children, telegram_id, execute=True)

    async def set_patient_work(self, work, telegram_id):
        sql = """
            UPDATE clinic_patient SET work = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, work, telegram_id, execute=True)

    async def set_patient_result_eeg(self, result_eeg, telegram_id):
        sql = """
            UPDATE clinic_patient SET result_eeg = $1 WHERE tg_id = $2
            """
        await self.db.execute(sql, result_eeg, telegram_id, execute=True)
