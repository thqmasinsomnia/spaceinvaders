class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        # Start game in an inactive state.
        self.game_active = False
        # High score should never be reset.
        self.high_score = 0
        self.level = 100
        self.kill_count = 0
        self.fastmusic1 = False
        self.fastmusic2 = False

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
