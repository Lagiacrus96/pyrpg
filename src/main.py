import pygame
import random

pygame.init()

# Game window size
"""
Small = 640 x 480
Medium = 800 x 600
Large = 1280 x 720
Full HD = 1920 x 1080
"""
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))

# Grid settings
TILESIZE = 16 # Size of one tile is 40 pixels
SCALE_FACTOR = 3
SCALE_TILESIZE = TILESIZE * SCALE_FACTOR
GRID_WIDTH = screen.get_width() // SCALE_TILESIZE
GRID_HEIGHT = screen.get_height() // SCALE_TILESIZE

# Battle settings
battleui_height = 300
battleui_y = screen_height - battleui_height
selected_option = 0 # 0, 1, 2, 3 are attack, ability, item, flee

# Movement timing
move_delay = 300
last_move_time = pygame.time.get_ticks()
battle_delay = 500
#last_battle_time = pygame.time.get_ticks()


# Default movement states
w_pressed, a_pressed, s_pressed, d_pressed = False, False, False, False

# Game states
STATE_EXPLORE = "exploration"
STATE_BATTLE = "battle"
GAME_STATE = STATE_EXPLORE
player_inventory = {"gold": 0}

class GameEntity:
    """
    A base class for all player characters and enemies in the game.

    Attributes:
        pos (list of int): X and Y grid coordinates for the entity's position on the map.
        health (int): The health of the entity. Represents the entity's vitality.
        colour (tuple): The RGB color of the entity, used for rendering.

    Methods:
        draw(surface): Draws the entity on the specified surface as a rectangle.
    """
    def __init__(self, xpos, ypos, max_health, colour):
        """
        Initializes a new GameEntity instance.

        Args:
            xpos (int): The X-coordinate of the entity on the grid.
            ypos (int): The Y-coordinate of the entity on the grid.
            health (int): The initial health of the entity.
            colour (tuple): The RGB color of the entity.
        """
        self.pos = [xpos, ypos]
        self.max_health = max_health
        self.current_health = max_health
        self.colour = colour


    def draw(self, surface):
        """
        Draws the entity as a rectangle onto the given surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the entity.
        """
        pygame.draw.rect(surface, self.colour, (self.pos[0] * SCALE_TILESIZE, self.pos[1] * SCALE_TILESIZE, SCALE_TILESIZE, SCALE_TILESIZE))

class Character(GameEntity):
    """
    A class for player-controlled characters in the game. Inherits attributes and 
    methods from GameEntity.

    Additional behaviors or methods specific to Character can be described here.
    """
    def __init__(self, xpos, ypos, max_health, starting_level, experience, colour):
        """
        Initializes a new Character instance, inheriting from GameEntity.

        Args:
            xpos (int): The X-coordinate of the character on the grid.
            ypos (int): The Y-coordinate of the character on the grid.
            health (int): The initial health of the character.
            colour (tuple): The RGB color of the character.
        """
        self.experience = experience
        super().__init__(xpos, ypos, max_health, colour)
    
    def level_up(self):
        pass #TODO


class Enemy(GameEntity):
    """
    A class for enemies in the game. Inherits attributes and methods from GameEntity.

    Additional details about Enemy-specific behaviors or methods can be added here.
    """
    def __init__(self, xpos, ypos, max_health, colour):
        """
        Initializes a new Enemy instance, inheriting from GameEntity.

        Args:
            xpos (int): The X-coordinate of the enemy on the grid.
            ypos (int): The Y-coordinate of the enemy on the grid.
            health (int): The initial health of the enemy.
            colour (tuple): The RGB color of the enemy.
        """
        super().__init__(xpos, ypos, max_health, colour)

class BattleSystem:
    """
    A class for configuring and activating battles

    Attributes:
        player (GameEntity):
        enemy (GameEntity):
    
    Methods:
        perform_turn:
        player_turn:
        enemy_turn:
        calculate_enemy_damage:
        enemy_attack:
    """
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.is_player_turn = True # TODO We start with the player's turn for now
        self.current_action = None

    def perform_turn(self):
        global last_move_time, current_time
        if self.is_player_turn:
            if current_time - last_move_time > battle_delay:
                self.player_turn()
                last_move_time = current_time
        else:
            if current_time - last_move_time > battle_delay:
                self.enemy_turn()
                last_move_time = current_time

        self.check_end_conditions()

    def player_attack(self):
        """
        The method that determines what happens when a player chooses to attack.
        """
        print("You attacked!") #TODO
        crit_chance = 10
        roll = random.randint(1,100)
        if roll <= crit_chance:
            print("You did a critical hit!")
            player_damage = 15
        else:
            player_damage = 10
        self.enemy.current_health -= player_damage

    def player_ability(self):
        """
        The method that determines what happens when a player chooses an ability.
        """
        print("You used all your strength!") #TODO
        player_damage = 20
        self.enemy.current_health -= player_damage

    def player_item(self):
        """
        The method that determines what happens when a player chooses an item.
        """
        print("You healed!") #TODO
        if self.player.current_health + 30 > self.player.max_health:
            self.player.current_health = self.player.max_health
        else:
            self.player.current_health += 30


    def player_flee(self):
        global battle, GAME_STATE
        """
        The method that determines what happens when a player chooses to flee.
        """
        print("You fled!") #TODO
        battle_end()
    
    def player_turn(self):
        global GAME_STATE, battle
        
        if self.current_action == None:
            return
        
        if self.current_action == "attack":
            self.player_attack()

        elif self.current_action == "ability":
            self.player_ability()

        elif self.current_action == "item":
            self.player_item()

        elif self.current_action == "flee":
            self.player_flee()

        self.current_action = None
        self.is_player_turn = False


    def enemy_turn(self):
        self.enemy_attack()
        self.is_player_turn = True

    
    def enemy_attack(self):
        print("The enemy attacked!") #TODO
        crit_chance = 5
        roll = random.randint(1,100)
        if roll <= crit_chance:
            print("The enemy critically hit you!")
            enemy_damage = 15
        else:
            enemy_damage = 10
        self.player.current_health -= enemy_damage
    
    def check_end_conditions(self):
        global GAME_STATE
        if self.player.current_health <= 0:
            print("you lost")
        elif self.enemy.current_health <= 0:
            print("You win!")
            player_inventory["Gold"] += 10
            player_inventory["Bronze Sword"] = 1
            player_inventory["Potion"] = 1
        else:
            return
        battle_end()
        
class BattleUI:
    global screen
    """
    A class for creating and updating the UI within battles

    Attributes:
        player (GameEntity):
        enemy (GameEntity)
        screen (TODO):
    
    Methods:
        TODO
    """
    def __init__(self, player, enemy, screen, font = pygame.font.Font(None, 65)):
        self.player = player
        self.enemy = enemy
        self.screen = screen
        self.font = font
    
    def draw_background(self):
        pygame.draw.rect(screen, (0, 0, 0), (0, battleui_y, screen_width, battleui_height))
        pygame.draw.rect(screen, (40, 0, 0), (0, 0, screen_width, battleui_y))
    
    def draw_player_stats(self):
        player_health_text = self.font.render("Player health: " + str(self.player.current_health) + " / " + str(self.player.max_health), True, (255, 255, 255))
        player_health_rect = player_health_text.get_rect(center = (screen_width * 1 // 5, screen_height * 6 // 7))
        screen.blit(player_health_text, player_health_rect)
    
    def draw_enemy_stats(self):
        enemy_health_text = self.font.render("Enemy health: " + str(self.enemy.current_health) + " / " + str(self.enemy.max_health), True, (255, 255, 255))
        enemy_health_rect = enemy_health_text.get_rect(center = (screen_width * 4 // 5, screen_height *6 // 7))
        screen.blit(enemy_health_text, enemy_health_rect)

    def draw_battle_menu(self):
        battle_attack = self.font.render("Attack", True, (255, 255, 255))
        attack_rect = battle_attack.get_rect(center = (screen_width // 2, screen_height * 6// 7 - 90))
        if selected_option == 0:
            pygame.draw.rect(screen, (0, 0, 255), attack_rect)
        screen.blit(battle_attack, attack_rect)

        battle_ability = self.font.render("Ability", True, (255, 255, 255))
        ability_rect = battle_ability.get_rect(center = (screen_width // 2, screen_height * 6// 7 - 30))
        if selected_option == 1:
            pygame.draw.rect(screen, (0, 0, 255), ability_rect)
        screen.blit(battle_ability, ability_rect)

        battle_item = self.font.render("Item", True, (255, 255, 255))
        item_rect = battle_item.get_rect(center = (screen_width // 2, screen_height * 6 // 7 + 30))
        if selected_option == 2:
            pygame.draw.rect(screen, (0, 0, 255), item_rect)
        screen.blit(battle_item, item_rect)

        battle_flee = self.font.render("Flee", True, (255, 255, 255))
        flee_rect = battle_flee.get_rect(center = (screen_width // 2, screen_height * 6 // 7 + 90))
        if selected_option == 3:
            pygame.draw.rect(screen, (0, 0, 255), flee_rect)
        screen.blit(battle_flee, flee_rect)

# Player settings
start_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2] # Starting position in grid terms
player = Character(start_pos[0], start_pos[1], 100, 1, 0, [0, 0, 255])

def global_event_handling(event):
    """
    A function to handle the events that can occur both inside and outside of battles

    Args:
        event (?):
    """
    global running
    if event.type == pygame.QUIT:
        running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False

def encounter():
        global GAME_STATE, enemy1, battle, player, remember_pos, battle_ui, screen
        remember_pos = player.pos
        player.pos = [GRID_WIDTH // 5, GRID_HEIGHT // 3]
        enemy1 = Enemy(4 * GRID_WIDTH // 5, GRID_HEIGHT // 3, 50, [255, 0, 0])
        battle = BattleSystem(player, enemy1)
        battle_ui = BattleUI(player, enemy1, screen)
        GAME_STATE = STATE_BATTLE


def explore_event_handling(event):
    """
    A function to handle specifically the events that only occur whilst not in battle.

    Args:
        event (?):
    """
    global running, GAME_STATE, current_time, a_pressed, d_pressed, w_pressed, s_pressed, player, enemy1


    # Movement handling
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            a_pressed = True
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            d_pressed = True
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            w_pressed = True
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            s_pressed = True
        
    if event.type == pygame.KEYUP:
        # Movement handling
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            a_pressed = False
        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            d_pressed = False
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            w_pressed = False
        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            s_pressed = False

def battle_event_handling(event, battle_system):
    global selected_option, running, GAME_STATE, current_time, a_pressed, d_pressed, w_pressed, s_pressed, player, enemy1

    # Menu event handling
    menu_options = {
        0: "attack",
        1: "ability",
        2: "item",
        3: "flee"
    }
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_option = (selected_option - 1) % 4
        elif event.key == pygame.K_DOWN:
            selected_option = (selected_option + 1) % 4
        elif event.key == pygame.K_RETURN:
            battle_system.current_action = menu_options[selected_option]

def explore_state():
    global last_move_time, player, current_time
    encounter_occur = random.randint(1, 100)

    if current_time - last_move_time > move_delay:
        if w_pressed and player.pos[1] > 0:
            player.pos[1] -= 1
            if encounter_occur >= 90:
                encounter()

        if s_pressed and player.pos[1] < GRID_HEIGHT - 1:
            player.pos[1] += 1
            if encounter_occur >= 90:
                encounter()

        if a_pressed and player.pos[0] > 0:
            player.pos[0] -= 1
            if encounter_occur >= 90:
                encounter()

        if d_pressed and player.pos[0] < GRID_WIDTH - 1:
            player.pos[0] += 1
            if encounter_occur >= 90:
                encounter()        

        last_move_time = current_time

    # Set explore screen
    screen.fill((0, 70, 0))

    # Draw player
    player.draw(screen)

def battle_state():
    global player, GAME_STATE, remember_pos, battle_ui

    battle_ui.draw_background()
    player.draw(screen)
    enemy1.draw(screen)
    battle_ui.draw_player_stats()
    battle_ui.draw_enemy_stats()
    battle_ui.draw_battle_menu()

def reset_movement_states():
    global w_pressed, a_pressed, s_pressed, d_pressed
    w_pressed, a_pressed, s_pressed, d_pressed = False, False, False, False

def battle_end():
    global GAME_STATE, battle, enemy1, encounter_occur, player, remember_pos
    print("Combat is finished!")
    player.pos = remember_pos
    reset_movement_states()
    GAME_STATE = STATE_EXPLORE
    battle = None
    enemy1 = None
    encounter_occur = 0




# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Explore vs battle event handling
    for event in pygame.event.get():
        global_event_handling(event)
        if GAME_STATE == STATE_EXPLORE:
                explore_event_handling(event)
        elif GAME_STATE == STATE_BATTLE:
                battle_event_handling(event, battle)
                
    if GAME_STATE == STATE_EXPLORE:
        explore_state()

    elif GAME_STATE == STATE_BATTLE:
        battle_state()
        battle.perform_turn()
        
    # Update game
    pygame.display.flip()

# Quit game
pygame.quit()