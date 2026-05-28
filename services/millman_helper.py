import json
from dataclasses import dataclass

from locales.ru_locale import Q17_RU
from locales.uz_locale import Q17_UZ


@dataclass(slots=True)
class MillmanScores:
    emotional_resilience: int
    self_regulation: int
    scale_motivation: int
    scale_resistance: int
    q17: str | None

    @classmethod
    def from_raw(cls, raw_scores: str | dict) -> "MillmanScores":
        data = json.loads(raw_scores) if isinstance(raw_scores, str) else raw_scores
        return cls(
            emotional_resilience=int(data.get("emotional_resilience", 0)),
            self_regulation=int(data.get("self_regulation", 0)),
            scale_motivation=int(data.get("scale_motivation", 0)),
            scale_resistance=int(data.get("scale_resistance", 0)),
            q17=data.get("q17"),
        )


class MillmanResultFormatter:
    def __init__(self, lang: dict, lang_code: str):
        self.lang = lang
        self.lang_code = lang_code

    def get_ball_word(self) -> str:
        return "балл" if self.lang_code == "ru" else "ball"

    def get_level_label(self, value: int) -> str:
        if self.lang_code == "ru":
            if value < 0:
                return "Низкий"
            if value == 0:
                return "Средний"
            return "Высокий"

        if value < 0:
            return "Past"
        if value == 0:
            return "O'rta"
        return "Yuqori"

    def normalize_q17(self, value: str | None) -> str:
        if not value:
            return "-"

        if self.lang_code == "ru":
            value = Q17_RU[value]
            return value
        return Q17_UZ[value]

    def format_scale(self, title_key: str, desc_key: str, value: int) -> str:
        return (
            f"{self.lang[title_key]} {self.get_level_label(value)}\n"
            f"({self.lang[desc_key]}) ({value} {self.get_ball_word()})"
        )

    def format_result(self, scores: MillmanScores) -> str:
        return (
            f"\n\n"
            f"{self.format_scale('emotional_resilience', 'emotional_resilience_desc', scores.emotional_resilience)}\n\n"
            f"{self.format_scale('self_regulation', 'self_regulation_desc', scores.self_regulation)}\n\n"
            f"{self.format_scale('scale_motivation', 'scale_motivation_desc', scores.scale_motivation)}\n\n"
            f"{self.format_scale('scale_resistance', 'scale_resistance_desc', scores.scale_resistance)}\n\n"
            f"{self.lang['q17']} {self.normalize_q17(scores.q17)}"
        )


def build_millman_response(raw_scores: str | dict, lang: dict, lang_code: str) -> str:
    scores = MillmanScores.from_raw(raw_scores)
    formatter = MillmanResultFormatter(lang=lang, lang_code=lang_code)
    return formatter.format_result(scores)
