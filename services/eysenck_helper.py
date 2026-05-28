import json
from dataclasses import dataclass


@dataclass(slots=True)
class EysenckScores:
    extra_intro: int
    neuroticism: int
    lie: int

    @classmethod
    def from_raw(cls, raw_scores: str | dict) -> "EysenckScores":
        data = json.loads(raw_scores) if isinstance(raw_scores, str) else raw_scores
        return cls(
            extra_intro=int(data["extra_intro"]),
            neuroticism=int(data["neuroticism"]),
            lie=int(data["lie"]),
        )


class EysenckResultFormatter:
    def __init__(self, lang: dict):
        self.lang = lang

    def get_temperament_key(self, extra_intro: int, neuroticism: int) -> str:
        if extra_intro > 12 and neuroticism > 12:
            return "choleric"
        if extra_intro > 12 >= neuroticism:
            return "sanguine"
        if extra_intro <= 12 < neuroticism:
            return "melancholic"
        return "phlegmatic"

    def get_extra_intro_key(self, value: int) -> str:
        if value <= 8:
            return "introvert"
        if value >= 16:
            return "extravert"
        return "ambivert"

    def get_neuroticism_key(self, value: int) -> str:
        if value <= 8:
            return "level_low"
        if value <= 13:
            return "level_medium"
        return "level_high"

    def get_stability_key(self, value: int) -> str:
        return "stable" if value <= 12 else "unstable"

    def get_lie_key(self, value: int) -> str:
        return "lie_high" if value > 5 else "lie_low"

    def tr(self, key: str) -> str:
        return self.lang[key]

    def format_result(self, scores: EysenckScores) -> str:
        temp_key = self.get_temperament_key(scores.extra_intro, scores.neuroticism)
        extra_key = self.get_extra_intro_key(scores.extra_intro)
        neuro_key = self.get_neuroticism_key(scores.neuroticism)
        stability_key = self.get_stability_key(scores.neuroticism)
        lie_key = self.get_lie_key(scores.lie)

        return (
            # f"{self.tr('title')}"
            f"{self.tr('temperament_title')} {self.tr(temp_key)}\n\n"
            f"{self.tr('lie_title')} {self.tr(lie_key)} ({scores.lie} {self.tr('ball')})\n\n"
            f"{self.tr('stability_title')} {self.tr(stability_key)} ({scores.neuroticism} {self.tr('ball')})\n\n"
            f"{self.tr('extra_intro_title')} {self.tr(extra_key)} ({scores.extra_intro} {self.tr('ball')})\n\n"
            f"{self.tr('neuro_title')} {self.tr(neuro_key)} ({scores.neuroticism} {self.tr('ball')})"
        )

def build_eysenck_response(raw_scores: str | dict, lang: dict) -> str:
    scores = EysenckScores.from_raw(raw_scores)
    formatter = EysenckResultFormatter(lang)
    return formatter.format_result(scores)