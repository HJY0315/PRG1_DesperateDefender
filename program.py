import random

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']

defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    num_rows = len(field)
    num_columns = len(field[0])

    print('{:5} {:5} {:5}'.format(1,2,3))

    print(' ',end = '')   
    for column in range(num_columns):
        print('+-----',end = '')
    print('+')

    for row in range(num_rows):
        print(chr(ord('A')+row),end ='')
        
        for column in field[row]:
            if column != None:
                print('|{:^5}'.format(str(column[0])),end = '')
            else:
                print('|{:^5}'.format(' '),end = '')
        print('|')
        
        print(' ',end = '')        
        for column in field[row]:
            if column != None:
                print('|{:^5}'.format(str(column[1][0])+'/'+str(column[1][1])),end = '')
            else:
                print('|{:^5}'.format(' '),end = '')
                
        print('|')

        print(' ',end = '')
        for column in range(len(field[0])):
            print('+-----',end = '')
        print('+')
        
    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print('Turn {}'.format(game_vars['turn']),end='     ')
    print('Threat = [{:<10}]'.format('-' * game_vars['threat']),end='    ')
    print('Danger Level = {}'.format(game_vars['danger_level']))
    print('Gold = {}'.format(game_vars['gold']),end = '     ')
    print('Monsters killed = {}/{}'.format(game_vars['monsters_killed'],game_vars['monster_kill_target']))
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Upgrade Unit")
    print("5. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):
    row = ord(position[0]) - ord('A')
    column = int(position[1]) - 1 #position = 'A7'example
    if row > 4:
        return False
    elif field[row][column] == None:
        if unit_name in defender_list:
            field[row][column] = [unit_name,[defenders[unit_name]['maxHP'],defenders[unit_name]['maxHP']]]  #[shortform name of unit, [remainding HP, maximum HP]]
        else:
            field[row][column] = [unit_name,[monsters[unit_name]['maxHP'],monsters[unit_name]['maxHP']]]
        return True
    else:
        return False

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    while True:     #keep prompting for a valid input
        try:
            choice = int(input('Your choice? '))
        except:
            print('Please Enter a Number!')
        else:
            if choice <= 3:  # A valid input, proceed to next step
                break
            else:   #If the input is a number but out of range #eg.5,6,7
                print('Invalid input')
    while True:
        if choice == 1 or choice == 2:       # 1 for archer, 2 for wall
            if game_vars['gold'] >= defenders[defender_list[choice-1]]['price']:  # defender_list = [archer,wall] 
                position = input('Place where? ')
                position = position.upper()
                if len(position) == 1:      #eg 1,a,b
                    print('Invalid input')
                else:
                    if int(position[1]) <= 3:
                        result = place_unit(field, position, defender_list[choice-1])
                        if result == True:      #Placement of unit is done and gold is deducted
                            game_vars['gold'] -= defenders[defender_list[choice-1]]['price']
                            return True
                        else:       #result = False which means the placement of unit is not succes
                            print('Invalid input')
                    else:       #eg. a5,b7
                        print('Please put your unit on first three column')
            else:
                print('Insufficient gold')
                return False     # Return to prompt input for combat menu and buy unit
        else:       #choice == 3
            return False
    return

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, column):
    for rows in range(row):
        count = 0   #Number of attack from the archer
        for columns in range(column):
            if field[rows][columns] != None:
                if field[rows][columns][0] == defender_list[0]:     # number of attack increase by one for every archer that we have in a row
                    count += 1
                elif field[rows][columns][0] == defender_list[1]:   #it will skip the wall
                    continue
                else:            # if the column is monster
                    while count > 0:        # if there is archer in the row 
                        num = random.randint(defenders[defender_name]['min_damage'],defenders[defender_name]['max_damage']) # random damage between min damage and max damage of archer
                        field[rows][columns][1][0] -= num
                        field[rows][columns][1] = [field[rows][columns][1][0],field[rows][columns][1][1]]
                        print('{} in lane {} shoots {} for {} damage!'.format(defenders[defender_name]['name'],chr(ord('A')+rows),monsters[field[rows][columns][0]]['name'],num))
                        if field[rows][columns][1][0] <= 0:     # Update the game variable if the monster died
                            print('{} dies!'.format(monsters[field[rows][columns][0]]['name']))
                            game_vars['monsters_killed'] += 1
                            game_vars['num_monsters'] -= 1
                            game_vars['gold'] += int(monsters[field[rows][columns][0]]['reward'])
                            print('You gain {} gold as a reward.'.format(monsters[field[rows][columns][0]]['reward']))
                            game_vars['threat'] += int(monsters[field[rows][columns][0]]['reward'])
                            field[rows][columns] = None
                            break
                        count -= 1    
    return

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_name, field, row, column):
    for rows in range(row):
        for columns in range(column):
            if field[rows][columns] != None:
                if field[rows][columns][0] == monster_name:
                    if columns == 0:    # If it is the first column, means that the monster will step out of map and game over
                        print('{} in lane {} advances!'.format(monsters[monster_name]['name'],chr(ord('A')+rows)))
                        print('A {} has reached the city! All is lost!'.format(monsters[monster_name]['name']))
                        field[rows][columns] = None  # remove the monster from original place
                        global play_game
                        play_game = False
                        global lost_game
                        lost_game = True        #For print statement of game over
                        break
                        
                    else:
                        position = chr(ord('A')+rows) + str(columns)    # get the position of monster
                        x = ord(position[0]) - ord('A')   # index of row
                        y = int(position[1]) - 1     #index of column of monster and minus 1 which means a column to left
                        
                        if monster_name == monster_list[1]:  #monster_list = ['ZOMBI', 'WWOLF']  IF IT IS Werewolf
                            advance = False
                            if field[x][y] == None:     # if next one column is empty, wolf advance one steps
                                field[x][y] = [field[rows][columns][0],[field[rows][columns][1][0],field[rows][columns][1][1]]]
                                field[rows][columns] = None
                                if y == 0:
                                    print('{} in lane {} advances!'.format(monsters[monster_name]['name'],chr(ord('A')+rows)))
                                    print('A {} has reached the city! All is lost!'.format(monsters[monster_name]['name']))
                                    field[rows][columns] = None  # remove the monster from original place
                                    return False
                                    break
                                advance = True
                            else:
                                if field[x][y][0] in defender_list:     #if next column have defender, attack
                                    num = random.randint(monsters[monster_name]['min_damage'],monsters[monster_name]['max_damage'])
                                    field[x][y][1][0] -= num        #remainding HP is deducted
                                    field[x][y][1] = [field[x][y][1][0],field[x][y][1][1]]  #update the HP
                                    print('{} in lane {} deals {} damage to {}!'.format(monsters[monster_name]['name'],chr(ord('A')+rows),num,defenders[field[x][y][0]]['name']))
                                    if field[x][y][1][0] <= 0:      #remove the defender if remainding HP is <= 0(died)
                                        print('{} dies!'.format(field[x][y][0]))
                                        field[x][y] = None
                                        break
                                
                            if advance == True:     #only can advance two step if previous step is empty
                                if field[x][y-1] == None: # if next two column from original column is empty, wolf advances two steps
                                    field[x][y-1] = [field[x][y][0],[field[x][y][1][0],field[x][y][1][1]]]
                                    field[x][y] = None
                                    advance = True
                                else:
                                    if field[x][y-1][0] in defender_list:       #if next two column from original column have defender, attack
                                        num = random.randint(monsters[monster_name]['min_damage'],monsters[monster_name]['max_damage'])
                                        field[x][y-1][1][0] -= num
                                        field[x][y-1][1] = [field[x][y-1][1][0],field[x][y-1][1][1]]
                                        print('{} in lane {} deals {} damage to {}!'.format(monsters[monster_name]['name'],chr(ord('A')+rows),num,defenders[field[x][y-1][0]]['name']))
                                        if field[x][y-1][1][0] <= 0:
                                            print('{} dies!'.format(field[x][y-1][0]))
                                            field[x][y-1] = None
                                
                            if advance == True:     # If monster advance
                                print('{} in lane {} advances!'.format(monsters[monster_name]['name'],chr(ord('A')+rows)))
                                
                        else:           # if it is zombie
                            position = chr(ord('A')+rows) + str(columns)    # get the position of monster
                            x = ord(position[0]) - ord('A')     # index of row
                            y = int(position[1]) - 1        #index of column of monster and minus 1 which means a column to left
                            
                            if field[x][y] == None:     #If next column is empty , advance
                                field[x][y] = [field[rows][columns][0],[field[rows][columns][1][0],field[rows][columns][1][1]]]
                                field[rows][columns] = None
                                print('{} in lane {} advances!'.format(monsters[monster_name]['name'],chr(ord('A')+rows)))
                                
                            elif field[x][y][0] in monster_list:  ##if column in front of monster is monster too, it do nothing 
                                continue
                            
                            else:           # If column in front of monster is defender, it will attack the defender with random damage
                                num = random.randint(monsters[monster_name]['min_damage'],monsters[monster_name]['max_damage'])
                                field[x][y][1][0] -= num
                                field[x][y][1] = [field[x][y][1][0],field[x][y][1][1]]
                                print('{} in lane {} deals {} damage to {}!'.format(monsters[monster_name]['name'],chr(ord('A')+rows),num,field[x][y][0]))
                                if field[x][y][1][0] <= 0:      # remove the defender if remainding HP <= 0  (died)
                                    print('{} dies!'.format(field[x][y][0]))
                                    field[x][y] = None
                                        
        
                else:           # check next column if current column is not monster
                    continue
    return

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):
    while True:
        if game_vars['num_monsters'] <= 5:
            row = random.randint(0,len(field)-1) #largest num generated should be 4
            position = chr(ord('A')+ row) + '7'
            result = place_unit(field, position, monster_list)
            if result == True:
                game_vars['num_monsters'] += 1
                break
    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    config_file = open('game_vars.txt', 'w')
    config_file.write('gold={}\n'.format(game_vars['gold']))
    config_file.write('turn={}\n'.format(game_vars['turn']))
    config_file.write('threat={}\n'.format(game_vars['threat']))
    config_file.write('danger_level={}\n'.format(game_vars['danger_level']))
    config_file.write('num_monsters={}\n'.format(game_vars['num_monsters']))
    config_file.write('monster_kill_target={}\n'.format(game_vars['monster_kill_target']))
    config_file.write('monsters_killed={}\n'.format(game_vars['monsters_killed']))
    config_file.close()
    config_file = open('game_field.txt', 'w')
    # Write nested for loop
    for row in range(len(field)):
        for column in range(len(field[row])):
            if field[row][column] != None:
                config_file.write('{},{},{},{},{}\n'.format(row,column,field[row][column][0],field[row][column][1][0],field[row][column][1][1]))
    # save row, column, shortname, remainding life, max life

    print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    config_file = open('game_vars.txt','r')
    for line in config_file:
        info = line.strip('\n')
        temp_list = info.split('=')
        game_vars[temp_list[0]] = int(temp_list[1]) # Replace the original new data with the previous stored data
    config_file.close()
    fieldfile = open('game_field.txt', 'r')
    for line in fieldfile:
        line = line.strip('\n')
        line_list = line.split(',')
        if line_list[2] in defender_list:
            field[int(line_list[0])][int(line_list[1])] = [line_list[2],[int(line_list[3]),int(line_list[4])]] 
            
        else:
            field[int(line_list[0])][int(line_list[1])] = [line_list[2],[int(line_list[3]),int(line_list[4])]]
    difference = game_vars['danger_level'] - 1
    for monster in monster_list:
        monsters[monster]['maxHP'] += difference
        monsters[monster]['min_damage'] += difference
        monsters[monster]['max_damage'] += difference
        monsters[monster]['reward'] += difference
    game_vars['turn'] -= 1      # deducted by 1 because when it start to play game, turn will increase by 1
    game_vars['gold'] -= 1      # same reason
    global count
    count += game_vars['turn'] // 12
    return

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
    
show_main_menu()
lost_game = False
count = 0  # for the danger level
choice = int(input('Your choice? '))

if choice == 1:
    play_game = True
    initialize_game()

elif choice == 2:
    play_game = True
    load_game(game_vars)

else:
    play_game = False

while play_game == True:
    game_vars['turn'] += 1  #Start with turn 1
    if game_vars['turn'] >= 2:  #Every turn after turn 1 will get 1 gold
        game_vars['gold'] += 1
    if game_vars['turn'] >= 12:  # danger level increase for every 12 turn
        game_vars['danger_level'] = (game_vars['turn'] // 12) + 1
    if game_vars['turn'] - (12 * count) >= 12:      #atributes of monsters increase by 1 for every 12 turn
        print('The evil grows stronger!')           #first 12 turn, count = 0 and turn is not deducted so it will increase the atributes, count += 1
        count += 1
        for monster in monster_list:                # for 20th turn, count = 1 and turn is deducted by 12 which will remain 8(not meet the condition), atributes not increase
            monsters[monster]['min_damage'] += 1
            monsters[monster]['max_damage'] += 1
            monsters[monster]['maxHP'] += 1
            monsters[monster]['reward'] += 1
    
    if game_vars['num_monsters'] == 0:  #Monster will spawn if there is no monster on the field, generated randomly between zombie and werewolf
        rand = random.randint(1,2)
        if rand == 1:
            spawn_monster(field, monster_list[0])
        else:
            spawn_monster(field, monster_list[1])
    draw_field() 
    while True:
        show_combat_menu(game_vars)
        validation = True   #Check the validation of input for combat menu
        try:
            choice = int(input('Your choice? '))
        except:         # It will keep prompt user for choice as long as his choice is invalid
            print('Invalid input')
            validation = False
        else:
            if choice > 5:
                print('Invalid input')
                validation = False
        if validation == True:      #choice is valid and proceed
            if choice == 1:
                print('What unit do you wish to buy?\n1. Archer (5 gold)\n2. Wall (3 gold)\n3. Don\'t buy')
                if buy_unit(field,game_vars) == True:   # Proceed to defender attack, monster advance and next turn if the placement of unit is success (Break from while loop)
                    break         
            elif choice == 2:        # Break from while loop and proceed to defender attack and monster advance and next turn
                break
            elif choice == 3:
                save_game()    
            elif choice == 4:
                save_game()
            else:        # Quit game
                play_game = False
                break
        else:       # repeat to prompt input for choice
            continue
    if play_game == False:   #Quit game to prevent the code run through the defender attack and monster advance
        break
    else:

        defender_attack(defender_list[0], field, len(field),len(field[0]))
        if play_game == False:
            break
        result = monster_advance(monster_list[1], field, len(field), len(field[0])) # for werewolf
        if result == False:
            play_game = False
            lost_game = True
            break
        monster_advance(monster_list[0], field, len(field), len(field[0])) # for zombie
        if result == False:
            play_game = False
            lost_game = True
            break
        increase_threat = random.randint(1,game_vars['danger_level'])  # random between 1 and danger level
        game_vars['threat'] += increase_threat
        if game_vars['threat'] >= 10:       # if threat > 10, randomly spawn zombie or werewolf and treat minus 10
            game_vars['threat'] -= 10
            x = random.randint(1,2)
            if x == 1:
                spawn_monster(field, monster_list[0])
            else:
                spawn_monster(field, monster_list[1])
        if game_vars['monsters_killed'] >= 20:      # victory if monster killed >= 20
            print('You have protected the city! You win!')
            play_game = False

if lost_game == True:
    print('You have lost the game. :(')
    
else:
    print('See you next time')


