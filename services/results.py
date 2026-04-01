import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from aiogram.types import InputFile
import io
from loader import bot, adldb


# -----------------------------
# Yordamchi funksiyalar
# -----------------------------
def draw_points_and_labels(ax, before_vals, after_vals, questionnaire=None):
    """Nuqtalarni va ularning qiymatlarini chizish."""
    n = len(before_vals)
    offset = 0.02 if n <= 4 else 0.03 + 0.09 * (n - 4) / 10
    offset_y = 0.12 if questionnaire else 0.45

    for i, (b, a) in enumerate(zip(before_vals, after_vals)):
        # Nuqtalarni chizish
        if b == a:
            ax.scatter(i, b, s=360, marker='o', facecolors='white', edgecolors='none', zorder=3)
            ax.scatter(i, b, s=160, marker='o', facecolors='#1f77b4', edgecolors='black', linewidths=1.2, zorder=4)
            ax.scatter(i, a, s=120, marker='D', facecolors='#ff7f0e', edgecolors='black', linewidths=1.2, zorder=5)
        else:
            ax.scatter(i, b, s=140, marker='o', facecolors='#1f77b4', edgecolors='#1f77b4', linewidths=1.0, zorder=4)
            ax.scatter(i, a, s=140, marker='o', facecolors='#ff7f0e', edgecolors='#ff7f0e', linewidths=1.0, zorder=5)

        # Qiymatlarni yozish
        ax.text(i - offset, b + offset_y, str(b), ha='center', va='bottom', fontsize=9, color="black",
                bbox=dict(facecolor='white', alpha=0.75, boxstyle='round,pad=0.2'), zorder=6)
        ax.text(i + offset, a + offset_y, str(a), ha='center', va='bottom', fontsize=9, color="black",
                bbox=dict(facecolor='white', alpha=0.75, boxstyle='round,pad=0.2'), zorder=6)


async def send_figure(telegram_id, buf, caption, filename="figure.png"):
    """Matplotlib figure-ni Telegramga yuborish."""
    buf.seek(0)
    await bot.send_photo(chat_id=telegram_id, photo=InputFile(buf, filename=filename), caption=caption)


# -----------------------------
# Asosiy funksiya
# -----------------------------
async def generate_test_results(
        telegram_id,
        test_name: str,
        result: dict,
        labels: list,
        before_keys: list,
        after_keys: list,
        extra_info: dict = None,
        full_caption: str = None,
        questionnaire: bool = False
):
    """Universal funksiya turli test natijalarini grafik qilib yuboradi."""

    await bot.send_chat_action(chat_id=telegram_id, action="upload_photo")

    if not result.get('before_date'):
        return await bot.send_message(
            chat_id=telegram_id,
            text=f"Xatolik!\n\nTest nomi: {test_name}\n\nTest to'liq ishlanmagan!"
        )

    fullname = result['patient_name']
    before_date = result['before_date']
    after_date = result['after_date']

    before_vals = [result.get(k) or 0 for k in before_keys]
    after_vals = [result.get(k) or 0 for k in after_keys]

    # Labels uzunligini moslash
    if len(labels) != len(before_vals):
        if len(labels) < len(before_vals):
            labels += [""] * (len(before_vals) - len(labels))
        else:
            labels = labels[:len(before_vals)]

    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        x = list(range(len(before_vals)))

        # Chiziqlar
        ax.plot(x, before_vals, linestyle='-', color="#1f77b4", linewidth=2.5,
                label=f'Oldin ({before_date})', zorder=1)
        ax.plot(x, after_vals, linestyle='-', color="#ff7f0e", linewidth=2.5,
                label=f'Keyin ({after_date})', zorder=1)

        # Nuqtalar va qiymatlar
        draw_points_and_labels(ax, before_vals, after_vals, questionnaire=questionnaire)

        # Y-oy chizig'i
        all_vals = before_vals + after_vals
        y_min = min(all_vals) - 1 if all_vals else 0
        y_max = max(all_vals) + 1 if all_vals else 10
        ax.set_ylim(y_min, y_max)

        # X-oylar
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_title(f"{test_name} - {fullname}", pad=20)

        # Legend
        handles = [
            Line2D([0], [0], color="#1f77b4", lw=2.5, marker='o', markerfacecolor='#1f77b4',
                   markeredgecolor='#1f77b4', markersize=8, label='Oldin'),
            Line2D([0], [0], color="#ff7f0e", lw=2.5, marker='o', markerfacecolor='#ff7f0e',
                   markeredgecolor='#ff7f0e', markersize=8, label='Keyin'),
            Line2D([0], [0], color="#ff7f0e", lw=2.5, marker='D', markerfacecolor='#ff7f0e',
                   markeredgecolor='#1f77b4', markersize=8, label='Teng natija')
        ]
        if extra_info:
            for key, val in extra_info.items():
                handles.append(Line2D([], [], color="none", label=f"{key}: {val}"))

        ax.legend(handles=handles)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Rasmni yuborish
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        caption_text = (f"<b>Test nomi:</b> {test_name}\n"
                        f"<b>Oldingi sana:</b> {before_date}\n"
                        f"<b>Keyingi sana:</b> {after_date}\n")
        if full_caption:
            caption_text += f"\n{full_caption}"

        await send_figure(telegram_id=telegram_id, buf=buf, caption=caption_text, filename=f"{test_name}.png")

    finally:
        plt.close('all')


# -----------------------------
# Optimallashtirilgan view_test_results
# -----------------------------
async def view_test_results(telegram_id):
    tests = [
        {
            "getter": adldb.get_result_yakhin,
            "test_name": "Yaxin, Mendelevich | Nevrotik holatni aniqlash testi",
            "labels": ["Xavotir", "Nevrotik-depressiya", "Asteniya", "Isterik",
                       "Obsessiv-fobiya", "Vegetativ buzilishlar"],
            "before_keys": ["before_anxiety", "before_depression", "before_asthenia", "before_hysteroid_response",
                            "before_obsessive_phobic", "before_vegetative"],
            "after_keys": ["after_anxiety", "after_depression", "after_asthenia", "after_hysteroid_response",
                           "after_obsessive_phobic", "after_vegetative"],
            "extra_info": lambda r: {
                "Nevrotik holat (Oldin)": "Bor" if r['before_detect'] else "Yo‘q",
                "Nevrotik holat (Keyin)": "Bor" if r['after_detect'] else "Yo‘q"
            }
        },
        {
            "getter": adldb.get_result_leonhard,
            "test_name": "Leongard | Xarakterologik so'rovnoma",
            "labels": ["Isteroid", "Pedantik", "Rigid", "Epileptoid", "Gipertim", "Distimik",
                       "Xavotirli va qo'rquvli", "Siklotim", "Affektiv-ekzaltir", "Emotiv"],
            "before_keys": ["before_hysteroid", "before_pedantic", "before_rigid", "before_epileptoid",
                            "before_hyperthymic", "before_dysthymic", "before_anxious", "before_cyclothymic",
                            "before_affective", "before_emotive"],
            "after_keys": ["after_hysteroid", "after_pedantic", "after_rigid", "after_epileptoid",
                           "after_hyperthymic", "after_dysthymic", "after_anxious", "after_cyclothymic",
                           "after_affective", "after_emotive"],
            "full_caption": "So'rovnoma va shakalalarga ta'rif quyidagi havolada:\n\n"
                            "https://telegra.ph/K-Leongardning-harakterologik-s%D1%9Erovnomasi-07-25"
        },
        {
            "getter": adldb.get_result_eysenc,
            "test_name": "Ayzenk | Shaxsiyat so'rovnomasi",
            "labels": ["Ekstraversiya", "Nevrotizm"],
            "before_keys": ["before_extraversion", "before_neuroticism"],
            "after_keys": ["after_extraversion", "after_neuroticism"],
            "extra_info": lambda r: {
                "Temperament (Oldin)": r['before_temperament'],
                "Temperament (Keyin)": r['after_temperament']
            },
            "full_caption": "<a href='https://telegra.ph/Ajzenk-SHahsiyat-s%D1%9Erovnomasiga-izo%D2%B3-07-20'>Ko'rsatmalar</a>"
        },
        {
            "getter": adldb.get_result_questionnaire,
            "test_name": "Savolnoma",
            "labels": ["Bosh og'rig'i", "Bosh aylanishi", "Ko'ngil aynishi", "Qorin og'rishi",
                       "Tomoqda bo'g'ilish hissi", "Yurak urib ketishi", "Uyqu buzilishi",
                       "Kayfiyatsizlik", "Yig'lash", "Befarqlik"],
            "before_keys": ["before_headache", "before_dizziness", "before_nausea", "before_abdominal_pain",
                            "before_feeling_choking", "before_heart_palpitations", "before_sleep_disturbance",
                            "before_low_mood", "before_crying", "before_indifference"],
            "after_keys": ["after_headache", "after_dizziness", "after_nausea", "after_abdominal_pain",
                           "after_feeling_choking", "after_heart_palpitations", "after_sleep_disturbance",
                           "after_low_mood", "after_crying", "after_indifference"],
            "extra_info": {"0": "Yo'q", "1": "Bor"},
            "questionnaire": True
        }
    ]

    # Har bir testni yuborish
    for test in tests:
        result = await test["getter"](telegram_id=telegram_id)

        extra_info = test.get("extra_info")
        if callable(extra_info):
            extra_info = extra_info(result)

        await generate_test_results(
            telegram_id=telegram_id,
            test_name=test["test_name"],
            result=result,
            labels=test["labels"],
            before_keys=test["before_keys"],
            after_keys=test["after_keys"],
            extra_info=extra_info,
            full_caption=test.get("full_caption"),
            questionnaire=test.get("questionnaire", None)
        )
