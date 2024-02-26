import math
from ..util import get_direction
from game.models import Board, GameObject

class Uzi(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            base = props.base
            self.goal_position = base
            
        else:
            diamond_buttons = [go for go in board.game_objects if go.type == "DiamondButtonGameObject"]
            diamonds = [go for go in board.game_objects if go.type == "DiamondGameObject"]
            if diamond_buttons and (not diamonds or len(diamonds) < 3):
                self.goal_position = diamond_buttons[0].position
            else:
                max_ratio = -1
                for i, diamond in enumerate (diamonds):
                    bot_diamonds = board_bot.properties.diamonds
                    diamond_points = diamond.properties.points

                    if (bot_diamonds + diamond_points > 5):
                        continue
                    x_dist = (board_bot.position.x - diamond.position.x) ** 2
                    y_dist = (board_bot.position.y - diamond.position.y) ** 2
                    dist_squared = x_dist + y_dist

                    if dist_squared == 0: 
                        continue

                    ratio = (diamond_points ** 2) / dist_squared

                    if ratio > max_ratio:
                        max_ratio = ratio
                        min_index = i

                if min_index is not None:
                    self.goal_position = board.diamonds[min_index].position

        if self.goal_position:
            # Calculate move according to goal position
            current_position = board_bot.position
            cur_x = current_position.x
            cur_y = current_position.y
            delta_x, delta_y = get_direction(
                cur_x,
                cur_y,
                self.goal_position.x,
                self.goal_position.y,
            )

            if (cur_x, cur_y) == self.previous_position:
                # We did not manage to move, lets take a turn to hopefully get out stuck position
                if delta_x != 0:
                    delta_y = delta_x * self.turn_direction
                    delta_x = 0
                elif delta_y != 0:
                    delta_x = delta_y * self.turn_direction
                    delta_y = 0
                # Switch turn direction for next time
                self.turn_direction = -self.turn_direction
            self.previous_position = (cur_x, cur_y)

            return delta_x, delta_y

        return 0, 0