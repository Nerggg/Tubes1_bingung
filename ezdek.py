import math
from ..util import get_direction
from game.models import Board, GameObject

class EzDek(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties

        if props.diamonds == 5:
            base = props.base
            self.goal_position = base
        elif (props.milliseconds_left < 10000):
            if (board_bot.position.x == props.base.x and board_bot.position.y == props.base.y):
                self.goal_position = board.diamonds[0].position
            else:
                base = props.base
                self.goal_position = base
        else:
            min = int(0)
            print("ezdek")
            for i in range (len(board.diamonds)):
                cek1 = 0
                cek2 = 0
                if ((board.diamonds[i].properties.points + props.diamonds <=5)):
                    xMinDist = (abs(board_bot.position.x - board.diamonds[min].position.x)) 
                    yMinDist = (abs(board_bot.position.y - board.diamonds[min].position.y)) 
                    xNewDist = (abs(board_bot.position.x - board.diamonds[i].position.x)) 
                    yNewDist = (abs(board_bot.position.y - board.diamonds[i].position.y)) 
                    minDist = xMinDist + yMinDist 
                    newDist = xNewDist + yNewDist 

                    for j in range(len(board.bots)):
                        if(board_bot.position.x != board.bots[j].position.x or board_bot.position.y != board.bots[j].position.y):
                            xbotDist = (abs(board.bots[j].position.x - board.diamonds[i].position.x)) 
                            ybotDist = (abs(board.bots[j].position.y - board.diamonds[i].position.y)) 
                            botDist = xbotDist + ybotDist

                            if (minDist >= botDist):
                                cek1 = 1
            
                            if (newDist >= botDist):
                                cek2 = 1

                    if (cek1 == 1 and cek2 == 2):
                        if (newDist < minDist):
                            min = i
                    elif (cek1 == 1):
                            min = i
            if((board.diamonds[min].properties.points + props.diamonds >5)):
                self.goal_position = props.base
            else:
                self.goal_position = board.diamonds[min].position

        if self.goal_position:
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
                if delta_x != 0:
                    delta_y = delta_x * self.turn_direction
                    delta_x = 0
                elif delta_y != 0:
                    delta_x = delta_y * self.turn_direction
                    delta_y = 0
                self.turn_direction = -self.turn_direction
            self.previous_position = (cur_x, cur_y)

            return delta_x, delta_y

        return 0, 0
