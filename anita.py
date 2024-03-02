import math
from ..util import get_direction
from game.models import Board, GameObject

# Ez win dek Uzi
class Anita(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1

    def purge(self, board_bot: GameObject, board: Board):
        diamond_buttons = [go for go in board.game_objects if go.type == "DiamondButtonGameObject"]
        diamonds = [go for go in board.game_objects if go.type == "DiamondGameObject"]
        teleporters = [go for go in board.game_objects if go.type == "TeleporterGameObject"]
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
            else:
                for teleporter in teleporters:
                    for diamond in diamonds:
                        x_dist = abs(teleporter.position.x - diamond.position.x)
                        y_dist = abs(teleporter.position.y - diamond.position.y)
                        if x_dist <= 1 and y_dist <= 1:
                            self.goal_position = teleporter.position
                            return
    
    def avoid_obstacle(self, board_bot: GameObject, board: Board):
        teleporters = [go for go in board.game_objects if go.type == "TeleporterGameObject"]
        if not teleporters:
            return

        for teleporter in teleporters:
            if self.is_in_line(board_bot.position, teleporter.position, self.goal_position):
                # Adjust goal position to avoid teleporter
                if teleporter.position.x != board_bot.position.x:
                    self.goal_position.x = teleporter.position.x - 1 if teleporter.position.x > board_bot.position.x else teleporter.position.x + 1
                if teleporter.position.y != board_bot.position.y:
                    self.goal_position.y = teleporter.position.y - 1 if teleporter.position.y > board_bot.position.y else teleporter.position.y + 1

    def is_in_line(self, pos1, pos2, pos3):
        # Check if all positions are in a straight line
        dx1 = pos2.x - pos1.x
        dy1 = pos2.y - pos1.y
        dx2 = pos3.x - pos2.x
        dy2 = pos3.y - pos2.y
        if dx1*dy2 == dy1*dx2:
            return True
        return False

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            base = props.base
            self.goal_position = base
            
        else:
            self.purge(board_bot,board)
    

        if self.goal_position:
            self.avoid_obstacle(board_bot, board)
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
    