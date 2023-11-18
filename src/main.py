import pygame

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
battleui_colour = (0, 0, 0)
battle = None

# Movement timing
move_delay = 125
last_move_time = pygame.time.get_ticks()

# Default movement states
w_pressed, a_pressed, s_pressed, d_pressed = False, False, False, False

# Game states
STATE_EXPLORE = "exploration"
STATE_BATTLE = "battle"
GAME_STATE = STATE_EXPLORE

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
    def __init__(self, xpos, ypos, health, colour):
        """
        Initializes a new GameEntity instance.

        Args:
            xpos (int): The X-coordinate of the entity on the grid.
            ypos (int): The Y-coordinate of the entity on the grid.
            health (int): The initial health of the entity.
            colour (tuple): The RGB color of the entity.
        """
        self.pos = [xpos, ypos]
        self.health = health
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
    def __init__(self, xpos, ypos, health, colour):
        """
        Initializes a new Character instance, inheriting from GameEntity.

        Args:
            xpos (int): The X-coordinate of the character on the grid.
            ypos (int): The Y-coordinate of the character on the grid.
            health (int): The initial health of the character.
            colour (tuple): The RGB color of the character.
        """
        super().__init__(xpos, ypos, health, colour)


class Enemy(GameEntity):
    """
    A class for enemies in the game. Inherits attributes and methods from GameEntity.

    Additional details about Enemy-specific behaviors or methods can be added here.
    """
    def __init__(self, xpos, ypos, health, colour):
        """
        Initializes a new Enemy instance, inheriting from GameEntity.

        Args:
            xpos (int): The X-coordinate of the enemy on the grid.
            ypos (int): The Y-coordinate of the enemy on the grid.
            health (int): The initial health of the enemy.
            colour (tuple): The RGB color of the enemy.
        """
        super().__init__(xpos, ypos, health, colour)

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
        if self.is_player_turn:
            self.player_turn()
        else:
            self.enemy_turn()

        self.check_end_conditions()

    def player_attack(self):
        """
        The method that determines what happens when a player chooses to attack.
        """
        print("You attacked!") #TODO
        player_damage = 1
        self.enemy.health -= player_damage

    def player_ability(self):
        """
        The method that determines what happens when a player chooses an ability.
        """
        print("You did a critial hit!") #TODO
        player_damage = 2
        self.enemy.health -= player_damage

    def player_item(self):
        """
        The method that determines what happens when a player chooses an item.
        """
        print("You healed!") #TODO
        self.player.health += 3


    def player_flee(self):
        global battle, GAME_STATE
        """
        The method that determines what happens when a player chooses to flee.
        """
        print("You fled!") #TODO
        player.pos = remember_pos
        GAME_STATE = STATE_EXPLORE
        battle = None
    
    def player_turn(self):
        global GAME_STATE, battle
        
        if self.current_action == None:
            return
        
        if self.current_action == "attack":
            self.player_attack()
            pygame.time.delay(1000) 

        elif self.current_action == "ability":
            self.player_ability()
            pygame.time.delay(1000)

        elif self.current_action == "item":
            self.player_heal()
            pygame.time.delay(1000)

        elif self.current_action == "flee":
            self.player_flee()
            pygame.time.delay(1000)

        self.current_action = None
        self.is_player_turn = False


    def enemy_turn(self):
        self.enemy_attack()

        self.is_player_turn = True

    def calculate_enemy_damage(self):
        base_damage = 1
        return base_damage
    
    def enemy_attack(self):
        enemy_damage = self.calculate_enemy_damage()
        self.player.health -= enemy_damage
        print("The enemy attacked!") #TODO
        pygame.time.delay(1000)
    
    def check_end_conditions(self):
        global GAME_STATE
        if self.player.health <= 0:
            print("you lost")
        elif self.enemy.health <= 0:
            print("You win!")
        else:
            return
        print("Combat is finished!")
        player.pos = remember_pos
        GAME_STATE = STATE_EXPLORE
        
# Player settings
start_pos = [GRID_WIDTH // 2, GRID_HEIGHT // 2] # Starting position in grid terms
player = Character(start_pos[0], start_pos[1], 9, [0, 0, 255])
enemy1 = Enemy(4 * GRID_WIDTH // 5, GRID_HEIGHT // 2, 3, [255, 0, 0])

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

def explore_event_handling(event):
    """
    A function to handle specifically the events that only occur whilst not in battle.

    Args:
        event (?):
    """
    global running, GAME_STATE, current_time, a_pressed, d_pressed, w_pressed, s_pressed, player, enemy1, remember_pos

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

        # Temporary battle initiation key    
        if event.key == pygame.K_b:
            remember_pos = player.pos
            enemy1.health = 3
            GAME_STATE = STATE_BATTLE
            print(GAME_STATE)
        
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
    global selected_option, running, GAME_STATE, current_time, a_pressed, d_pressed, w_pressed, s_pressed, player, enemy1, remember_pos

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
    if current_time - last_move_time > move_delay:
        if w_pressed and player.pos[1] > 0:
            player.pos[1] -= 1
        if s_pressed and player.pos[1] < GRID_HEIGHT - 1:
            player.pos[1] += 1
        if a_pressed and player.pos[0] > 0:
            player.pos[0] -= 1
        if d_pressed and player.pos[0] < GRID_WIDTH - 1:
            player.pos[0] += 1

        last_move_time = current_time

    # Set explore screen
    screen.fill((0, 70, 0))

    # Draw player
    player.draw(screen)

def battle_state():
    global player, enemy1, GAME_STATE
    screen.fill((20, 0, 0))

    player.pos = [GRID_WIDTH // 5, GRID_HEIGHT // 2]

    player.draw(screen)
    enemy1.draw(screen)
    battle_UI(player, enemy1)

def battle_UI(player, enemy, colour = (255, 255, 255)):
    global selected_option
    font = pygame.font.Font(None, 65)

    # UI background
    pygame.draw.rect(screen, battleui_colour, (0, battleui_y, screen_width, battleui_height))

    # Player stats text
    player_health_text = font.render("Player health: " + str(player.health), True, colour)
    player_health_rect = player_health_text.get_rect(center = (screen_width * 1 // 5, screen_height * 6 // 7))
    # Enemy stats text
    enemy_health_text = font.render("Enemy health: " + str(enemy.health), True, colour)
    enemy_health_rect = enemy_health_text.get_rect(center = (screen_width * 4 // 5, screen_height *6 // 7))

    battle_attack = font.render("Attack", True, (255, 255, 255))
    battle_ability = font.render("Ability", True, (255, 255, 255))
    battle_item = font.render("Item", True, (255, 255, 255))
    battle_flee = font.render("Flee", True, (255, 255, 255))

    attack_rect = battle_attack.get_rect(center = (screen_width // 2, screen_height * 6// 7 - 90))
    ability_rect = battle_ability.get_rect(center = (screen_width // 2, screen_height * 6// 7 - 30))
    item_rect = battle_item.get_rect(center = (screen_width // 2, screen_height * 6 // 7 + 30))
    flee_rect = battle_flee.get_rect(center = (screen_width // 2, screen_height * 6 // 7 + 90))

    # Highlight selected option
    if selected_option == 0:
        pygame.draw.rect(screen, (0, 0, 255), attack_rect)
    elif selected_option == 1:
        pygame.draw.rect(screen, (0, 0, 255), ability_rect)
    elif selected_option == 2:
        pygame.draw.rect(screen, (0, 0, 255), item_rect)
    elif selected_option == 3:
        pygame.draw.rect(screen, (0, 0, 255), flee_rect)
    
    # Display text
    screen.blit(player_health_text, player_health_rect)
    screen.blit(enemy_health_text, enemy_health_rect)
    screen.blit(battle_attack, attack_rect)
    screen.blit(battle_ability, ability_rect)
    screen.blit(battle_item, item_rect)
    screen.blit(battle_flee, flee_rect)

    pygame.display.flip()

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
                if battle is None:
                    battle = BattleSystem(player, enemy1)

                battle_event_handling(event, battle)
                
    if GAME_STATE == STATE_EXPLORE:
        battle = None
        explore_state()

    elif GAME_STATE == STATE_BATTLE:
        battle_state()
        battle.perform_turn()
        
    # Update game
    pygame.display.flip()

# Quit game
pygame.quit()