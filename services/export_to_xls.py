import json
import os
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from loader import appdb

failed = "Ishlanmagan"


async def export_athletes_to_excel() -> str:
    # Postgres’dan ma’lumotlarni olamiz
    rows = await appdb.get_athlete_to_xlsx()

    wb = Workbook()
    ws = wb.active
    ws.title = "Athletes"

    # Excel ustunlari
    headers = [
        "Ism sharif",
        "Tel raqam",
        "Sport turi",
        "Tajriba",
        "Xobbi",

        # Eysenck
        "Ayzenk Samimiylik",
        "Ayzenk Extra_intro",
        "Ayzenk Neyrotizm",
        "Ayzenk Temperament",

        # Millman
        "Millman Emotsional reaksiyalar",
        "Millman O'zini boshqarish",
        "Millman Motivatsion quvvat",
        "Millman To'siqlarga bardoshlilik",
        "Millman Hissiy barqarorlik",

        # 4 savollar
        "4savollar_zarurat",
    ]

    ws.append(headers)

    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    for row in rows:
        # tests maydonini parse qilamiz
        tests_raw = row["tests"]
        try:
            tests = json.loads(tests_raw) if isinstance(tests_raw, str) else (tests_raw or {})
        except json.JSONDecodeError:
            tests = {}

        eysenc = tests.get("eysenc", {})
        millman = tests.get("millman", {})
        savol4 = tests.get("4savollar", {})

        ws.append([
            row["full_name"],
            row["phone_number"],
            row["sport_type"],
            row["sport_experience_years"],
            row["hobbies"],

            # Eysenck
            eysenc.get("lie", failed),
            eysenc.get("extra_intro", failed),
            eysenc.get("neuroticism", failed),
            eysenc.get("temperament", failed),

            # Millman
            millman.get("q17", failed),
            millman.get("self_regulation", failed),
            millman.get("scale_motivation", failed),
            millman.get("scale_resistance", failed),
            millman.get("emotional_resilience", failed),

            # 4 savollar
            savol4.get("zarurat", failed),
        ])

    # Ustun kengliklarini avtomatik sozlash
    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter

        for cell in column_cells:
            value = "" if cell.value is None else str(cell.value)
            if len(value) > max_length:
                max_length = len(value)

        ws.column_dimensions[column_letter].width = min(max_length + 2, 40)

    os.makedirs("exports", exist_ok=True)
    filename = f"exports/athletes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb.save(filename)

    return filename
