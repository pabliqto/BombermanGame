from dynaconf import Dynaconf

settings = Dynaconf(settings_files=['settings.toml'])


class Scoreboard:
    def __init__(self):
        self._score = {i: 0 for i in range(1, settings.players + 1)}

    def box_destroyed(self, player_id):
        self._score[player_id] += 10

    def kill_player(self, player_id):
        self._score[player_id] += 50

    @property
    def score(self):
        return self._score

    def get_top_scorer(self):
        top_score = None
        top_scorer = None
        multiple_top_scorers = False

        for player_id, score in self.score.items():
            if top_score is None or score > top_score:
                top_score = score
                top_scorer = player_id
                multiple_top_scorers = False
            elif score == top_score:
                multiple_top_scorers = True

        if multiple_top_scorers:
            return None

        return top_scorer
