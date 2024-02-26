import math
from ..util import get_direction
from game.models import Board, GameObject

class AutowinLogic(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        # Analyze new state
        if props.diamonds == 5:
            # Move to base if we are full of diamonds
            base = props.base
            self.goal_position = base
        else:
            # Move towards first diamond on board

            # ALGORITMA YANG DIUBAH DISINI AJA YAK
            ## algoritma yg baru gw tambahin masih penghitung jarak diamond terdekat
            ### masih belum konsiderasi diamond merah atau biru (todo) (dan kayanya gabisa)
            ### dan belum konsiderasi penggunaan portal (todo)

            ## perhitungkan diamond kotak merah
            ### kalo diamond merah dan biru kejauhan, incar diamond kotak

            for i in range (len(board.game_objects)):
                print(board.game_objects[i].type)

            min = int(0)
            homeDistanceToNearestDiamond = float(0)
            diamondButton = int()
            home = int()
            for i in range(len(board.game_objects)):
                if (board.game_objects[i].type == "BaseGameObject"):
                    home = i
                    continue
                elif (board.game_objects[i].type == "DiamondButtonGameObject"):
                    diamondButton = i
                    diamondButtonDistanceToHome = math.sqrt(math.pow(board.game_objects[home].position.x - board.game_objects[i].position.x, 2) + math.pow(board.game_objects[home].position.y - board.game_objects[i].position.y, 2))
                    continue
                elif (board.game_objects[i].type == "BotGameObject" and board_bot.position.x == board.game_objects[i].position.x and board_bot.position.y == board.game_objects[i].position.y):
                    continue
                elif (board.game_objects[i].type == "DiamondGameObject"):
                    if (board_bot.properties.diamonds + board.game_objects[i].properties.points > 5):
                        continue
                    xMinDist = (abs(board_bot.position.x - board.game_objects[min].position.x)) 
                    yMinDist = (abs(board_bot.position.y - board.game_objects[min].position.y)) 
                    xNewDist = (abs(board_bot.position.x - board.game_objects[i].position.x)) 
                    yNewDist = (abs(board_bot.position.y - board.game_objects[i].position.y)) 
                    minDist = math.sqrt(xMinDist * xMinDist + yMinDist * yMinDist)
                    newDist = math.sqrt(xNewDist * xNewDist + yNewDist + yNewDist)

                    if (newDist < minDist):
                        min = i
                        homeDistanceToNearestDiamond = math.sqrt(math.pow(board.game_objects[home].position.x - board.game_objects[min].position.x, 2) + math.pow(board.game_objects[home].position.y - board.game_objects[min].position.y, 2))
                # elif (board.game_objects[i].type == "TeleportGameObject"):




            # if (homeDistanceToNearestDiamond > math.sqrt(72) or homeDistanceToNearestDiamond > diamondButtonDistanceToHome):
            if (homeDistanceToNearestDiamond > math.sqrt(72)):
                self.goal_position = board.game_objects[diamondButton].position
            else:
                self.goal_position = board.game_objects[min].position

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
