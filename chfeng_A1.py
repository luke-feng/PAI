"""
Kingsheep Agent Template

This template is provided for the course 'Practical Artificial Intelligence' of the University of Zürich. 

Please edit the following things before you upload your agent:
	- change the name of your file to '[uzhshortname]_A1.py', where [uzhshortname] needs to be your uzh shortname
	- change the name of the class to a name of your choosing
	- change the def 'get_class_name()' to return the new name of your class
	- change the init of your class:
		- self.name can be an (anonymous) name of your choosing
		- self.uzh_shortname needs to be your UZH shortname

The results and rankings of the agents will be published on OLAT using your 'name', not 'uzh_shortname', 
so they are anonymous (and your 'name' is expected to be funny, no pressure).

"""

from config import *
import random


def get_class_name():
    return 'chfeng_A1'


class chfeng_A1:
    """Example class for a Kingsheep player"""
    def __init__(self):
        self.name = "chfeng_A1"
        self.uzh_shortname = "chfeng"
        self.beam_deep = 2
        self.beam_k = 2

        
    def get_player_position(self,figure,field):
        #get the current position
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))
    
    def food_present(self,field):
        food_present = False

        for line in field: 
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    food_present = True
                    break
        return food_present

    def sheep_score(self, current_position, player_number, figure, field):
        '''
        @param current_position
        @param player_number
        @param figure
        @param field
        return score of current position
        
        '''
        if player_number == 1:
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
        else:
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
        
        x = current_position[0]
        y = current_position[1]
        if field[x][y] == CELL_RHUBARB:
            return 5
        elif field[x][y] == CELL_GRASS:
            return 1
        elif self.valid_move(figure, x, y, field) == False:
            return -100
        elif (abs(x-wolf_position[0]) < 2 and abs(y-wolf_position[1]) < 2):
            return -100
        else:
            return 0


    def possible_nextstep_sheep(self, sheep_position, player_number, figure, field):
        next_step = []
        socre = 0

        x = sheep_position[0]-1
        y = sheep_position[1]
        score = self.sheep_score([x,y], player_number, figure, field)
        next_step.append(([x,y], socre))

        x = sheep_position[0]+1
        y = sheep_position[1]
        score = self.sheep_score([x,y], player_number, figure, field)
        next_step.append(([x,y], socre))

        x = sheep_position[0]
        y = sheep_position[1]-1
        score = self.sheep_score([x,y], player_number, figure, field)
        next_step.append(([x,y], socre))

        x = sheep_position[0]
        y = sheep_position[1]+1
        score = self.sheep_score([x,y], player_number, figure, field)
        next_step.append(([x,y], socre))

        x = sheep_position[0]
        y = sheep_position[1]
        score = self.sheep_score([x,y], player_number, figure, field)
        next_step.append(([x,y], socre))
        return next_step

    
    def beam_search1(self, player_number, field):
        '''
        beam search for a possible goal
        @param player_number: the number of current player
        @parpm k: parameter for beam search
        @param field
        @return the best result of beam search
        '''
        # get current position
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            figure = CELL_SHEEP_1
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            figure = CELL_SHEEP_2
        
        max_len = self.beam_deep
        num_beams = self.beam_k  
        
        sequences = [[[],0]]

        for i in range(max_len):
            all_candidates = []
            for j in range(len(sequences)):
                seq, score = sequences[j]
                for m in range(5):
                    #print(sheep_position)
                    possible_nextsteps = self.possible_nextstep_sheep(sheep_position, player_number, figure, field)
                    sheep_position = possible_nextsteps[m][0]
                    for goal in possible_nextsteps:
                        candidate = [seq + goal[0], score + goal[1]]
                        all_candidates.append(candidate)
        
            ordered = sorted(all_candidates, key= lambda top: top[1], reverse= True)
            sequences = ordered[:num_beams]
        return sequences[0][0]


    def possible_goals(self, sheep_position, field):
        '''
        @param sheep_position: current sheep position
        @param field field
        @return all possible goals with distance and score
        '''
        # return all possible foe current situation
        possible_goals = []
    
        #make list of possible goals

        y_position = 0
        for line in field:
            x_position = 0
            possible_goal = [y_position, x_position]
            for item in line:
                if item == CELL_RHUBARB:
                    distance = abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])
                    point = 1.5/(distance+1)
                    possible_goals.append((y_position, x_position, 1.5, distance, point))
                elif item == CELL_GRASS:
                    distance = abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])
                    point = 1 / (distance+1)
                    possible_goals.append((y_position, x_position, 1, distance, point))
                x_position += 1
            y_position += 1
        
        return possible_goals
    
    
    def k_best(self, possible_goals, k):
        '''
        @param possible_goals: all possible goals
        @param k: k best
        @return return k best possible goals
        '''
        counts = len(possible_goals)
        orderd = sorted(possible_goals, key= lambda top: top[4], reverse= True)
        if k > counts:
            for i in range( k - counts):
                orderd.append((0,0,0,0,0))
            return orderd
        else:
            return orderd[:k]

        
    def beam_search(self, player_number, field):
        '''
        beam search for a possible goal
        @param player_number: the number of current player
        @parpm k: parameter for beam search
        @param field
        @return the best result of beam search
        '''
        # get current position
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
        
        max_len = self.beam_deep
        num_beams = self.beam_k  
        possible_goals = self.possible_goals(sheep_position, field)
        topk_goals = self.k_best(possible_goals, num_beams)
        sequences = [[[],0]]

        for i in range(max_len):
            all_candidates = []
            for i in range(len(sequences)):
                seq, score = sequences[i]
                for m in range(max_len):
                    possible_goals = self.possible_goals(sheep_position, field)
                    topk_goals = self.k_best(possible_goals, max_len)
                    sheep_position = topk_goals[m]
                    for goal in topk_goals:
                        candidate = [seq + [(goal[0], goal[1])], score + goal[4]]
                        all_candidates.append(candidate)
        
            ordered = sorted(all_candidates, key= lambda top: top[1], reverse= True)
            sequences = ordered[:num_beams]
        return sequences[0][0][0]
    
    def gather_closest_goal(self,closest_goal,field,figure):
        figure_position = self.get_player_position(figure,field)

        distance_x = figure_position[1]-closest_goal[1]
        distance_y = figure_position[0]-closest_goal[0]
        can_up = self.valid_move(figure, figure_position[0]-1,figure_position[1],field)
        can_down = self.valid_move(figure, figure_position[0]+1,figure_position[1],field)
        can_left = self.valid_move(figure, figure_position[0],figure_position[1]-1,field)
        can_right = self.valid_move(figure, figure_position[0],figure_position[1]+1,field)

        if distance_x == 0:
            #print('item above/below me')
            if distance_y > 0:
                # above me
                if can_up:
                    return MOVE_UP
                elif can_right and can_left:
                    seed = random.randint(0,1)
                    if seed == 0:
                        return MOVE_LEFT
                    else:
                        return MOVE_RIGHT
                elif can_right:
                    return MOVE_RIGHT
                elif can_left:
                    return MOVE_LEFT
                elif can_down:
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
            
            if distance_y <= 0:
                # below me
                if can_down:
                    return MOVE_DOWN
                elif can_right and can_left:
                    seed = random.randint(0,1)
                    if seed == 0:
                        return MOVE_LEFT
                    else:
                        return MOVE_RIGHT
                elif can_right:
                    return MOVE_RIGHT
                elif can_left:
                    return MOVE_LEFT
                elif can_up:
                    return MOVE_UP
                else:
                    return MOVE_NONE

        if distance_y == 0:
                #print('item right/left me')
            if distance_x > 0:
                # left me
                if can_left:
                    return MOVE_LEFT
                elif can_up and can_down:
                    seed = random.randint(0,1)
                    if seed == 0:
                        return MOVE_UP
                    else:
                        return MOVE_DOWN
                elif can_up:
                    return MOVE_up
                elif can_down:
                    return MOVE_down
                elif can_right:
                    return MOVE_RIGHT
                else:
                    return MOVE_NONE
            
            if distance_x <= 0:
                # right me
                if can_right:
                    return MOVE_RIGHT
                elif can_up and can_down:
                    seed = random.randint(0,1)
                    if seed == 0:
                        return MOVE_UP
                    else:
                        return MOVE_DOWN
                elif can_up:
                    return MOVE_up
                elif can_down:
                    return MOVE_down
                elif can_left:
                    return MOVE_LEFT
                else:
                    return MOVE_NONE
            
        if distance_x > 0 and distance_y > 0:
            # left and above me
            if can_up and can_left:
                seed = random.randint(0,1)
                if seed == 0:
                    return MOVE_UP
                else:
                    return MOVE_LEFT
            elif can_up:
                return MOVE_UP
            elif can_left:
                return MOVE_LEFT
            elif can_down:
                return MOVE_DOWN
            elif can_right:
                return MOVE_RIGHT
            else:
                return MOVE_NONE

        if distance_x < 0 and distance_y > 0:
                # right and above me
            if can_up and can_right:
                seed = random.randint(0,1)
                if seed == 0:
                    return MOVE_UP
                else:
                    return MOVE_RIGHT
            elif can_up:
                return MOVE_UP
            elif can_right:
                return MOVE_RIGHT
            elif can_down:
                return MOVE_DOWN
            elif can_left:
                return MOVE_LEFT
            else:
                return MOVE_NONE

        if distance_x > 0 and distance_y < 0:
            # left and below me
            if can_down and can_left:
                seed = random.randint(0,1)
                if seed == 0:
                    return MOVE_DOWN
                else:
                    return MOVE_LEFT
            elif can_down:
                return MOVE_DOWN
            elif can_left:
                return MOVE_LEFT
            elif can_up:
                return MOVE_UP
            elif can_right:
                return MOVE_RIGHT
            else:
                return MOVE_NONE

        if distance_x < 0 and distance_y < 0:
            # right and below me
            if can_down and can_right:
                seed = random.randint(0,1)
                if seed == 0:
                    return MOVE_DOWN
                else:
                    return MOVE_RIGHT
            elif can_down:
                return MOVE_DOWN
            elif can_right:
                return MOVE_RIGHT
            elif can_up:
                return MOVE_UP
            elif can_left:
                return MOVE_LEFT
            else:
                return MOVE_NONE

    def wolf_close(self,player_number,field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf_position = self.get_player_position(CELL_WOLF_1,field)

        if (abs(sheep_position[0]-wolf_position[0]) <= 2 and abs(sheep_position[1]-wolf_position[1]) <= 2):
            #print('wolf is close')
            return True
        return False
    
    def valid_move(self, figure, x_new, y_new, field):
             # Neither the sheep nor the wolf, can step on a square outside the map. Imagine the map is surrounded by fences.
        if x_new > FIELD_HEIGHT - 1:
            return False
        elif x_new < 0:
            return False
        elif y_new > FIELD_WIDTH -1:
            return False
        elif y_new < 0:
            return False

        # Neither the sheep nor the wolf, can enter a square with a fence on.
        if field[x_new][y_new] == CELL_FENCE:
            return False

        # Wolfs can not step on squares occupied by the opponents wolf (wolfs block each other).
        # Wolfs can not step on squares occupied by the sheep of the same player .
        if figure == CELL_WOLF_1:
            if field[x_new][y_new] == CELL_WOLF_2:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_1:
                return False
        elif figure == CELL_WOLF_2:
            if field[x_new][y_new] == CELL_WOLF_1:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_2:
                return False


        # Sheep can not step on squares occupied by the wolf of the same player.
        # Sheep can not step on squares occupied by the opposite sheep.
        if figure == CELL_SHEEP_1:
            if field[x_new][y_new] == CELL_SHEEP_2 or \
                field[x_new][y_new] == CELL_WOLF_1:
                return False
        elif figure == CELL_SHEEP_2:
            if field[x_new][y_new] == CELL_SHEEP_1 or \
                    field[x_new][y_new] == CELL_WOLF_2:
                return False

        return True
    
    def run_from_wolf(self,player_number,field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
            sheep = CELL_SHEEP_1
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
            sheep = CELL_SHEEP_2

        distance_x = sheep_position[1] - wolf_position[1]
        abs_distance_x = abs(sheep_position[1] - wolf_position[1])
        distance_y = sheep_position[0] - wolf_position[0]
        abs_distance_y = abs(sheep_position[0] - wolf_position[0])

        can_up = self.valid_move(sheep, sheep_position[0]-1,sheep_position[1],field)
        can_down = self.valid_move(sheep, sheep_position[0]+1,sheep_position[1],field)
        can_left = self.valid_move(sheep, sheep_position[0],sheep_position[1]-1,field)
        can_right = self.valid_move(sheep, sheep_position[0],sheep_position[1]+1,field)
        print(can_up,can_down, can_left, can_right)
        
        if distance_y > 0 and distance_x == 0:
            #w above the s
            if can_down:
                return MOVE_DOWN
            elif can_left and can_right:
                seed = random.randint(0,2)
                if seed == 0:
                    return MOVE_LEFT
                if seed == 1:
                    return MOVE_RIGHT
            else:
                return MOVE_NONE

        if distance_y < 0 and distance_x == 0:
            #w below the s
            if can_up:
                return MOVE_UP
            elif can_left and can_right:
                seed = random.randint(0,2)
                if seed == 0:
                    return MOVE_LEFT
                if seed == 1:
                    return MOVE_RIGHT
            else:
                return MOVE_NONE

        if distance_y == 0 and distance_x > 0:
            #w left the s
            if can_right:
                return MOVE_RIGHT
            elif can_up and can_down:
                seed = random.randint(0,2)
                if seed == 0:
                    return MOVE_UP
                if seed == 1:
                    return MOVE_DOWN
            else:
                return MOVE_NONE

        if distance_y == 0 and distance_x < 0:
            #w right the s
            if can_left:
                return MOVE_LEFT
            elif can_up and can_down:
                seed = random.randint(0,2)
                if seed == 0:
                    return MOVE_UP
                if seed == 1:
                    return MOVE_DOWN
            else:
                return MOVE_NONE

        if distance_y < 0 and distance_x < 0:
            #w below and right the s
            if distance_y >= distance_x:
                #(x=-2, y=-1)
                if can_left:
                    return MOVE_LEFT
                elif can_up:
                    return MOVE_UP
                elif can_right:
                    return MOVE_RIGHT
                elif can_down:
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
            else:
                if can_up:
                    return MOVE_UP
                elif can_left:
                    return MOVE_LEFT   
                elif can_right:
                    return MOVE_RIGHT
                elif can_down:
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
      
        if distance_y > 0 and distance_x < 0:
            #w above and right the s
            if abs_distance_x > abs_distance_y:
                #(x=-2, y=1)
                if can_left:
                    return MOVE_LEFT
                elif can_down:
                    return MOVE_DOWN
                elif can_right:
                    return MOVE_RIGHT
                elif can_up:
                    return MOVE_UP
                else:
                    return MOVE_NONE
            else:
                if can_down:
                    return MOVE_DOWN
                elif can_left:
                    return MOVE_LEFT   
                elif can_right:
                    return MOVE_RIGHT
                elif can_up:
                    return MOVE_UP
                else:
                    return MOVE_NONE

        if distance_y > 0 and distance_x > 0:
            #w above and left the s
            if abs_distance_x > abs_distance_y:
                    #(x = 2, y=1)
                if can_right:
                    return MOVE_RIGHT
                elif can_down:
                    return MOVE_DOWN
                elif can_left:
                    return MOVE_LEFT
                elif can_up:
                    return MOVE_UP
                else:
                    return MOVE_NONE
            else:
                if can_down:
                    return MOVE_DOWN
                elif can_right:
                    return MOVE_RIGHT 
                elif can_left:
                    return MOVE_LEFT
                elif can_up:
                    return MOVE_UP
                else:
                    return MOVE_NONE


        if distance_y < 0 and distance_x > 0:
            #w below and left the s
            if abs_distance_x > abs_distance_y:
                #(x = 2, y=-1)
                if can_right:
                    return MOVE_RIGHT
                elif can_up:
                    return MOVE_UP
                elif can_left:
                    return MOVE_LEFT
                elif can_down:
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
            else:
                if can_up:
                    return MOVE_UP
                elif can_right:
                    return MOVE_RIGHT 
                elif can_left:
                    return MOVE_LEFT
                elif can_down:
                    return MOVE_DOWN
                else:
                    return MOVE_NONE
        else: #this method was wrongly called
            return MOVE_NONE

    def move_sheep(self, p_num, p_state, p_time_remaining, field):
        if p_num == 1:
            figure = CELL_SHEEP_1
        else:
            figure = CELL_SHEEP_2

        if self.wolf_close(p_num, field):
            move = self.run_from_wolf(p_num, field)
            print("run move {}".format(move))
        elif self.food_present(field):
            move = self.gather_closest_goal(self.beam_search(p_num, field), field, figure)
            print("normal move {}".format(move))
        else:
            move = MOVE_NONE

        #move = self.gather_closest_goal(self.beam_search1(p_num, field), field, figure)  

        return move, p_state

    def move_wolf(self, p_num, p_state, p_time_remaining, field):
        if p_num == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            move = self.gather_closest_goal(sheep_position, field, CELL_WOLF_1)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            move = self.gather_closest_goal(sheep_position, field, CELL_WOLF_2)

        return move, p_state

    