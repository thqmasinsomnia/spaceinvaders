class Settings:
    def __init__(self):
        self.alien_points = 50
        self.alienb_points = 75
        self.alienc_points = 100
        self.screen_width = 600
        self.screen_height = 750
        self.bg_color = (0, 0, 0)
        # Bullet settings
        self.bullet_speed_factor = 1
        self.alien_bullet_speed_factor = .5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 255, 255
        self.bullets_allowed = 3

        # Ship settings
        self.ship_speed_factor = 1.1
        self.ship_limit = 3

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.1
        self.initialize_dynamic_settings()

        self.bunker_size = 10

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.1
        self.bullet_speed_factor = 3
        self.alien_speed_factor = .5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
