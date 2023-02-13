# Snake game in Pygame
# By: Jerry Cui

# Imports
import pygame
from random import randint
from sys import exit

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# The different fonts that will be used during the game
font = "freesansbold.ttf"
title_font = pygame.font.Font(font, 48)
subtitle_font = pygame.font.Font(font, 36)
score_font = pygame.font.Font(font, 18)
big_font = pygame.font.Font(font, 80)  # For a big "GAME OVER" text death screen

# Constants
SCREEN_WIDTH = 1440  # Don't change this, as my GUI is designed for this screen size
SCREEN_HEIGHT = 1000

SQUARE_WIDTH = 40
SQUARE_HEIGHT = 40

FPS = 180  # Frames per second. This is the perfect balance between a laggy game and game that's too fast

# Set colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (187, 41, 187)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

UP = (0, -1)  # Your x value stays the same (increased by distance * 0, while your y value changes by distance * -1)
RIGHT = (1, 0)  # Same goes for other directions
DOWN = (0, 1)
LEFT = (-1, 0)

SPEED_INCREASE = 0.5  # By how much the game gets faster after each fruit eaten
TIME_INCREASE = 5  # Bonus time for each fruit eaten
FRUIT_LIFETIME = 5  # How many seconds a fruit lasts for

# Setting up some stuff
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load assets
increase_sound = pygame.mixer.Sound("increase.wav")

# Variables that need to be defined at the start but aren't constants
mode = "Classic"
music = "On"
sound_fx = "On"


# Functions related to the dictionaries
# Regular, player squares
def square__init__(x, y):
	# Create the square dictionary and set the attributes
	self = {}  # The dictionary used to store its attributes
	
	self["x"] = x
	self["y"] = y
	
	self["queue"] = []  # A list of which direction to move
	self["draw_rect"] = pygame.Rect(self["x"], self["y"], SQUARE_WIDTH, SQUARE_HEIGHT)  # The Rect object used for
	# drawing the square
	self["colour"] = RED  # the default colour is red
	
	return self  # This square object has been created and is now returned to be used in the game


def square_main(self, number, player, mode):
	# The main function for the square, which is executed every time it moves
	# number variable is which place it is in the list of squares (starting from 0), player variable is 1 for Player 1,
	# or 2 for Player 2 and mode is the game mode
	global score, square_ticker_max, time_left, fruits  # Needed global variables
	# Score is the score of the player, square_ticker_max is the number of frames delayed before moving everything
	# (so the lower it is, the faster the game goes), time_left is how much time is left and fruits is the list of
	# fruits
	
	self["x"] += SQUARE_WIDTH * self["queue"][0][0]
	self["y"] += SQUARE_HEIGHT * self["queue"][0][1]
	# Each item in the list self["queue"] is one of the directions, which is a list of 0, -1 or 1. This is then
	# multiplied by square's dimensions to get the new coordinates
	
	self["draw_rect"] = pygame.Rect(self["x"], self["y"], SQUARE_WIDTH, SQUARE_HEIGHT)
	
	# Check collision with fruit
	if self["x"] == fruits[0]["x"] and self["y"] == fruits[0]["y"]:
		# Since everything happens on a "grid" if they have both the same x and y, they are on the same grid square
		if player == 1:  # If this is Player 1 right now
			squares.append(square__init__(squares[-1]["x"], squares[-1]["y"]))
		# A new square is being added to the back of the list, with the same coordinates of the current last square
		elif player == 2:  # For player 2
			squares2.append(square__init__(squares2[-1]["x"], squares2[-1]["y"]))
			squares2[-1]["colour"] = BLUE  # Since the default colour for squares is red, we have to specify a blue one
		# Replace the fruits list
		fruits = [fruit__init__(randint(1, SCREEN_WIDTH // SQUARE_WIDTH - 1) * SQUARE_WIDTH,
		                            randint(1, SCREEN_HEIGHT // SQUARE_WIDTH - 1) * SQUARE_WIDTH)]
		# Add a new fruit. We divide the screen_dimensions by 40 so that we get a number, that when multiplied again,
		# is a multiple of 40 so it is perfectly on a grid square. -1 because otherwise fruit could spawn on the right
		# and bottom edges
		
		if sound_fx == "On":  # Play the sound effect only if sound_fx is turned on
			pygame.mixer.Sound.play(increase_sound)
		
		if mode == "Classic" or "Obstacle Course":
			score += 1  # Score is only counted in these game modes
			square_ticker_max -= SPEED_INCREASE  # Slowly increase speed, only in these game modes
			time_left += TIME_INCREASE  # Time is also only counted in this mode
	
	if number + 1 != len(squares) and player == 1:  # If this is not currently the last square and player 1
		squares[number + 1]["queue"].append(self["queue"][0])  # Set the direction of the next square, which is the
	# current direction
	if number + 1 != len(squares2) and player == 2:  # For player 2
		squares2[number + 1]["queue"].append(self["queue"][0])
	
	self["queue"].remove(self["queue"][0])  # Remove the direction from this queue, since we just moved it
	
	square_draw(self)  # Draw itself


def square_draw(self):
	# Just draw the square passed in the function
	pygame.draw.rect(display, self["colour"], self["draw_rect"], 0, 6)  # 6 is the how round the square corners are


# Fruit squares
def fruit__init__(x, y):
	# Initialize the fruit obje- I mean dictionaries, basically similar to the square__init__
	self = {}
	
	self["x"] = x
	self["y"] = y
	
	self["draw_rect"] = pygame.Rect(self["x"], self["y"], SQUARE_WIDTH, SQUARE_HEIGHT)
	
	self["timer"] = FPS * FRUIT_LIFETIME  # The life time, in frames, of the fruit before it disappears
	
	return self


def fruit_main(self):
	# The main code for the fruit. All it does is subtract from the timer, and finish the fruit if it reaches 0
	fruit_draw(self)  # Draw goes first because return would skip the rest of the function
	
	self["timer"] -= 1
	if self["timer"] <= 0:
		return "Done"
	
	
def fruit_draw(self):
	# Draw the fruit, same as a player square but green
	pygame.draw.rect(display, GREEN, self["draw_rect"], 0, 6)


# Obstacles
def obstacle__init__(x, y):
	# Another type of square that serves as an obstacle
	self = {}
	
	self["x"] = x
	self["y"] = y
	
	self["draw_rect"] = pygame.Rect(self["x"], self["y"], SQUARE_WIDTH, SQUARE_HEIGHT)
	
	return self


def obstacle_main(self):
	# There is no code for the obstacles to execute, so its just the drawing
	pygame.draw.rect(display, GREY, self["draw_rect"], 0, 6)


#  More important data for the game that required the above functions
# Create the lists that contain all the squares for both players, and set their positions
squares = [square__init__(0, 0),
           square__init__(0 - SQUARE_WIDTH, 0),
           square__init__(0 - SQUARE_WIDTH * 2, 0)]
squares2 = [square__init__(SCREEN_WIDTH - SQUARE_WIDTH * 3, SCREEN_HEIGHT - SQUARE_HEIGHT),
            square__init__(SCREEN_WIDTH - SQUARE_WIDTH * 2, SCREEN_HEIGHT - SQUARE_HEIGHT),
            square__init__(SCREEN_WIDTH - SQUARE_WIDTH, SCREEN_HEIGHT - SQUARE_HEIGHT)]

# All the squares for Player 1 start off moving right, while they start moving left for Player 2
for square in squares:
	square["queue"].append(RIGHT)
for square in squares2:
	square["queue"].append(LEFT)

square_ticker_max = 15  # Squares only animate once every square_ticker_max frames. Square ticker is the countdown
square_ticker = 15  # until it reaches 0, in which case it goes back to whatever value square_ticker_max is

score = 0  # The score (there is no score for two player modes)

# First square for each player must be set to a special colour
squares[0]["colour"] = ORANGE
squares2[0]["colour"] = PURPLE
squares2[1]["colour"] = BLUE  # Player 2 squares must be set to blue because they are red by default
squares2[2]["colour"] = BLUE

# List of fruits, using the same random generation algorithm
fruits = [fruit__init__(randint(1, SCREEN_WIDTH // 40 - 1) * 40, randint(1, SCREEN_HEIGHT // 40 - 1) * 40)]
# Fruit can sometimes spawn under obstacles so that the player will lose five seconds - this is to make the obstacle
# game mode more challenging

time_left = 15  # Number of seconds left before the player dies
turn = "Player 1"  # Whose turn it is to move for strategy mode
dead = False  # If either of the players died

fade_out_value = 0  # Increases up to 255 as screen fades to black


def square_collision(object_1, object_2):
	# Checks if there is a collision between two square dictionaries, which is as simple as seeing if their x and y are
	# the same, since everything is on a grid
	return object_1["x"] == object_2["x"] and object_1["y"] == object_2["y"]
	
	
# Game function
def game(mode="Classic"):
	# Play the game, with special rules depending on the mode
	global square_ticker, squares, squares2, square_ticker_max, fruits, time_left, score, turn, fade_out_value, dead
	# global variables required, quite a lot, right?
	
	direction = RIGHT  # Default starting direction for player 1
	direction2 = LEFT  # For player 2
	
	# Start the music, which is different for each game mode and loops infinitely
	if music == "On":  # Only if the user kept it on in the settings
		if mode == "Classic":
			pygame.mixer.music.load("game_music.mp3")
		elif mode == "Two Player":
			pygame.mixer.music.load("two_player_music.mp3")
		elif mode == "Obstacle Course":
			pygame.mixer.music.load("obstacle_music.wav")
		elif mode == "Strategy":
			pygame.mixer.music.load("strategy_music.mp3")
		pygame.mixer.music.play(-1)  # Play the music on loop
	else:
		pygame.mixer.music.stop()   # If the music is turned off, just stop the music
	
	message = None  # The death message, which is currently nothing
	player_1_moved = False  # The players have not made their move yet
	player_2_moved = False  # (only for strategy mode)
	
	if mode == "Obstacle Course":  # Set up obstacles
		obstacles = []  # Starts with an empty list
		for i in range(30):  # 30 obstacles
			obstacles.append(
				obstacle__init__(randint(1, SCREEN_WIDTH // 40 - 1) * 40, randint(1, SCREEN_HEIGHT // 40 - 1) * 40))
			# Randomly generated locations similar to fruit
	else:
		obstacles = []  # If we are not playing obstacle mode, then the list will be empty
	
	while True:  # Main game loop
		display.fill(BLACK)  # Background colour, which is black
		
		for event in pygame.event.get():  # Check if player clicked X
			if event.type == pygame.QUIT:
				exit()
				pygame.quit()
		
		# Get key presses
		if mode != "Strategy":  # If the game mode is not strategy
			key = pygame.key.get_pressed()
			if key[pygame.K_w] and squares[0]["queue"][0] != DOWN:  # You can't travel in one direction if you are
				direction = UP
			elif key[pygame.K_d] and squares[0]["queue"][0] != LEFT:  # already travelling in the opposite one
				direction = RIGHT
			elif key[pygame.K_s] and squares[0]["queue"][0] != UP:
				direction = DOWN
			elif key[pygame.K_a] and squares[0]["queue"][0] != RIGHT:
				direction = LEFT
			
			if square_ticker <= 0:  # If the square_ticker has reached 0, we can now animate our squares
				squares[0]["queue"].append(direction)  # Add the latest direction to the first square's queue (this will
				# be passed on to every next square in the square_main function
				for i in range(0, len(squares)):
					square_main(squares[i], i, 1, mode)  # Call upon the main function of every square, using range
					# instead of iteration so we also know what placement each square is
			else:  # If it is not yet time to animate the squares
				for square in squares:
					square_draw(square)  # Just draw it again
			
			# Now for player 2 movements
			if mode == "Two Player":  # . . . if it is the two_player game mode, otherwise just the same stuff
				if key[pygame.K_UP] and squares2[0]["queue"][0] != DOWN:
					direction2 = UP
				elif key[pygame.K_RIGHT] and squares2[0]["queue"][0] != LEFT:
					direction2 = RIGHT
				elif key[pygame.K_DOWN] and squares2[0]["queue"][0] != UP:
					direction2 = DOWN
				elif key[pygame.K_LEFT] and squares2[0]["queue"][0] != RIGHT:
					direction2 = LEFT
				
				if square_ticker <= 0:
					squares2[0]["queue"].append(direction2)
					for i in range(0, len(squares2)):
						square_main(squares2[i], i, 2, mode)  # Call upon the main function of every square
				
				else:
					for square in squares2:
						square_draw(square)  # Just draw it again
			
			# Subtract a number from the square ticker if it is still above 0
			if square_ticker > 0:
				square_ticker -= 1
			else:  # Otherwise, reset it to the maximum
				square_ticker = square_ticker_max
		else:  # This is if it is strategy mode
			turn_text = score_font.render("Turn: " + turn, True, WHITE)
			display.blit(turn_text, (0, 0))  # Create some text that shows whose turn it is
			
			key = pygame.key.get_pressed()
			if turn == "Player 1":  # If it is player 1's turn
				if key[pygame.K_w] and squares[0]["queue"][0] != DOWN:
					direction = UP  # set player 1's direction to up
					player_1_moved = True  # Player 1 has made their move
				elif key[pygame.K_d] and squares[0]["queue"][0] != LEFT:
					direction = RIGHT
					player_1_moved = True  # Player 1 has made their move
				elif key[pygame.K_s] and squares[0]["queue"][0] != UP:
					direction = DOWN
					player_1_moved = True  # Player 1 has made their move
				elif key[pygame.K_a] and squares[0]["queue"][0] != RIGHT:
					direction = LEFT
					player_1_moved = True  # Player 1 has made their move
					
				if player_1_moved:
					squares[0]["queue"] = [direction, direction]  # Needs to have two items to stop an error happening
					for i in range(0, len(squares)):
						square_main(squares[i], i, 1, mode)  # Call upon the main function of every square,
					# immediately after they key_press
					turn = "Player 2"  # Hand over the turn to the other player
					player_1_moved = False  # Now this is no longer true
					
			else:  # Same thing if it is Player 2's turn
				if key[pygame.K_UP] and squares2[0]["queue"][0] != DOWN:
					direction2 = UP
					player_2_moved = True
				elif key[pygame.K_RIGHT] and squares2[0]["queue"][0] != LEFT:
					direction2 = RIGHT
					player_2_moved = True
				elif key[pygame.K_DOWN] and squares2[0]["queue"][0] != UP:
					direction2 = DOWN
					player_2_moved = True
				elif key[pygame.K_LEFT] and squares2[0]["queue"][0] != RIGHT:
					direction2 = LEFT
					player_2_moved = True
					
				if player_2_moved:
					squares2[0]["queue"] = [direction2, direction2]
					for i in range(0, len(squares2)):
						square_main(squares2[i], i, 2, mode)
					turn = "Player 1"
					player_2_moved = False
			
			for square in squares:  # Draw every square in strategy mode so we can still see it
				square_draw(square)
			for square in squares2:
				square_draw(square)
		
		# Check for collision for game borders
		if (squares[0]["x"] < 0) or (squares[0]["x"] + SQUARE_WIDTH > SCREEN_WIDTH) \
				or (squares[0]["y"] < 0) or (squares[0]["y"] + SQUARE_HEIGHT > SCREEN_HEIGHT):  # If the first square is
			# out of bounds
			if mode != "Two Player" or "Strategy":  # If there was only one player
				message = ("You lost by colliding with the border. Your score was " + str(score) + ".")
			else:
				message = "Player 1 lost by colliding with the border."  # Need to be specific in multi-player
			dead = True  # Yes, someone has died
		
		if mode == "Two Player" or mode == "Strategy":  # Check Player 2's border collisions if there are two players
			if (squares2[0]["x"] < 0) or (squares2[0]["x"] + SQUARE_WIDTH > SCREEN_WIDTH) \
					or (squares2[0]["y"] < 0) or (squares2[0]["y"] + SQUARE_HEIGHT > SCREEN_HEIGHT):
				message = "Player 2 lost by colliding with the border."
				dead = True
		
		# Check square vs square collision: If a player's head square touches its body squares
		for i in range(1, len(squares)):
			if square_collision(squares[0], squares[i]):
				dead = True  # A collision has occurred
				if mode != "Two Player" or "Strategy":
					message = "You lost by colliding with yourself. Your score was " + str(score) + "."
				else:
					message = "Player 1 lost by colliding with itself."
		
		if mode == "Two Player" or mode == "Strategy":  # Same for Player 2
			for i in range(1, len(squares2)):
				if square_collision(squares2[0], squares2[i]):
					dead = True
					message = "Player 2 lost by colliding with itself."
			# Collisions against each other
			for square in squares:  # If Player 2's head touches one of Player 1's body squares
				if square_collision(squares2[0], square):
					dead = True
					message = "Player 2 lost by colliding with Player 1's body."
			for square in squares2:  # Now vice versa
				if square_collision(squares[0], square):
					dead = True
					message = "Player 1 lost by colliding with Player 2's body."
		
		# If the game is obstacles, we have to check for obstacle collisions
		if mode == "Obstacle Course":
			for i in range(len(obstacles)):  # Loop through every obstacle
				if square_collision(squares[0], obstacles[i]):
					dead = True
					message = "You lost by colliding with an obstacle. Your score was " + str(score) + "."
		
		# Now we go through each fruit
		for fruit in fruits:
			result = fruit_main(fruit)  # Call the main function
			if mode != "Strategy":  # Fruit disappear in each game mode except strategy
				if result == "Done":  # This will be the returned value if the fruit has to disappear
					fruits = [fruit__init__(randint(1, SCREEN_WIDTH // SQUARE_WIDTH - 1) * SQUARE_WIDTH,
					                            randint(1, SCREEN_HEIGHT // SQUARE_WIDTH - 1) * SQUARE_WIDTH)]
					# Remove the fruit and replace it with a new one
		
		if mode == "Obstacle Course":  # Make every obstacle draw itself again if we are playing that game mode
			for obstacle in obstacles:
				obstacle_main(obstacle)
		
		if mode == "Classic" or mode == "Obstacle":  # We only need score and time for these game modes
			# Draw score text
			score_text = score_font.render(("Score: " + str(score)), True, WHITE)
			display.blit(score_text, (0, 0))  # Score text
			
			# Timer text
			time_left -= 1 / FPS  # This code is executed FPS times each second, so we have to divide it
			if time_left > 10:
				timer_text = score_font.render(("Time Left: " + str(round(time_left))), True, WHITE)
			else:
				timer_text = score_font.render(("Time Left: " + str(round(time_left, 1))), True, RED)
			# Turns red and shows a decimal point if time goes below 10, so there are to different versions
			display.blit(timer_text, (100, 0))
			
			if time_left <= 0:
				message = "You lost by running out of time."
				dead = True  # Kill the player if they run out of time
		
		# Death animation - music and screen fades out before ending the game
		# However, while fading out, you can control your players for a little bit
		if dead:
			if fade_out_value == 0:
				latest_message = message  # Save the current message so it doesn't change
				if music == "On":  # If there is music, then fade it out over 4 seconds
					pygame.mixer.music.fadeout(4000)
			
			fade_out_value += 1  # increase the opacity by 1
			
			fade_out_rect = pygame.display.get_surface().get_rect()  # What is actually happening is that we are
			fade_out_image = pygame.Surface(fade_out_rect.size, flags=pygame.SRCALPHA)  # drawing a transparent black
			fade_out_image.fill((0, 0, 0))  # Surface object over everything, that gets less and less transparent
			fade_out_image.set_alpha(fade_out_value)
	
			display.blit(fade_out_image, (0, 0))  # Draw this surface
			
			if fade_out_value == 500:  # Once it reaches 500, that's enough
				message = latest_message  # Set the message to the same as it was when the player died
				break  # Finally, leave the loop
		
		clock.tick(FPS)  # Frames per second tick
		pygame.display.update()  # Update the screen
	
	# Reset game variables for next game (This code happens after the loop is broken, which signifies death)
	# This is the same code copied from above
	squares = [square__init__(0, 0),
	           square__init__(0 - SQUARE_WIDTH, 0),
	           square__init__(0 - SQUARE_WIDTH * 2, 0)]
	squares2 = [square__init__(SCREEN_WIDTH - SQUARE_WIDTH * 3, SCREEN_HEIGHT - SQUARE_HEIGHT),
	            square__init__(SCREEN_WIDTH - SQUARE_WIDTH * 2, SCREEN_HEIGHT - SQUARE_HEIGHT),
	            square__init__(SCREEN_WIDTH - SQUARE_WIDTH, SCREEN_HEIGHT - SQUARE_HEIGHT)]
	
	for square in squares:
		square["queue"].append(RIGHT)
	for square in squares2:
		square["queue"].append(LEFT)
	
	square_ticker_max = 15
	square_ticker = 15
	
	score = 0
	
	squares[0]["colour"] = ORANGE
	squares2[0]["colour"] = PURPLE
	squares2[1]["colour"] = BLUE
	squares2[2]["colour"] = BLUE
	
	fruits = [fruit__init__(randint(1, SCREEN_WIDTH // 40 - 1) * 40, randint(1, SCREEN_HEIGHT // 40 - 1) * 40)]
	
	time_left = 15
	turn = "Player 1"
	dead = False
	
	fade_out_value = 0
	
	game_over(message)  # Call the specialized game_over function


def options(return_function):
	# Screen that is shown to toggle music and sound effects
	# return_function is the function to call at the end of this function to return to where you were before
	global music, sound_fx  # Global variables needed
	
	while True:
		display.fill(BLACK)
		
		# Blit one of the four possible combinations depending on the current settings
		if music == "On":
			if sound_fx == "On":
				display.blit(pygame.image.load("options_on_on.png"), (0, 0))
			else:
				display.blit(pygame.image.load("options_on_off.png"), (0, 0))
		else:
			if sound_fx == "On":
				display.blit(pygame.image.load("options_off_on.png"), (0, 0))
			else:
				display.blit(pygame.image.load("options_off_off.png"), (0, 0))
		
		# These are rects that are the click hitbox of each clickable button
		music_rect = pygame.rect.Rect((0, 214), (357, 49))
		sound_rect = pygame.rect.Rect((0, 280), (357, 49))
		back_rect = pygame.rect.Rect((0, 352), (357, 49))
		
		for event in pygame.event.get():  # Basic game loop stuff
			if event.type == pygame.QUIT:
				exit()
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:  # If clicked,
				mouse_pos = pygame.mouse.get_pos()  # get the mouse position
				if music_rect.collidepoint(mouse_pos):  # If the mouse is colliding with the music options
					if music == "On":
						music = "Off"
					elif music == "Off":
						music = "On"
				elif sound_rect.collidepoint(mouse_pos):
					if sound_fx == "On":
						sound_fx = "Off"
					elif sound_fx == "Off":
						sound_fx = "On"
				elif back_rect.collidepoint(mouse_pos):
					return_function()  # Call the function of where this came from
		
		key = pygame.key.get_pressed()
		
		if key[pygame.K_ESCAPE]:  # Pressing escape will also bring you back
			return_function()
		
		clock.tick(FPS)
		pygame.display.update()


def game_over(message):
	# A death screen after each game
	# Message is the death message carried over from the game function
	
	if music == "On":  # Play the defeat music if music is turned on
		pygame.mixer.music.load("defeat_music.mp3")
		pygame.mixer.music.play()
	if music == "Off":
		pygame.mixer.music.load("defeat_music.mp3")  # We still play the music when it is turned off, but we mute it
		pygame.mixer.music.play()  # because the timing is based on the length of the theme
		pygame.mixer.music.set_volume(0)
	
	move_on = False  # It is not yet time to finish the death screen
	game_over_fade_out_value = 0  # Similar to the one in the game function. Controls opacity
	
	while True:
		display.fill(BLACK)
		
		title = big_font.render("GAME OVER", True, WHITE)
		title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 300))  # Center the text
		display.blit(title, title_rect)
		
		result = score_font.render(message, True, WHITE)
		result_rect = result.get_rect(center=(SCREEN_WIDTH / 2, 400))
		display.blit(result, result_rect)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
				pygame.quit()
		
		if not pygame.mixer.music.get_busy():
			move_on = True  # If the music has ended (it is no longer "busy"), then finish the death screen
		
		if move_on:  # Fade out one last time before going back the game screen
			game_over_fade_out_value += 5
			
			fade_out_rect = pygame.display.get_surface().get_rect()
			fade_out_image = pygame.Surface(fade_out_rect.size, flags=pygame.SRCALPHA)
			fade_out_image.fill((0, 0, 0))
			fade_out_image.set_alpha(game_over_fade_out_value)
			
			display.blit(fade_out_image, (0, 0))
			
			if game_over_fade_out_value == 300:
				play_menu()  # Returns to the play menu
		
		clock.tick(FPS)
		pygame.display.update()


def play_menu():
	global mode
	
	if music == "On":
		pygame.mixer.music.load("menu_music.mp3")
		pygame.mixer.music.play(-1)
	else:
		pygame.mixer.music.stop()
	
	pygame.mixer.music.set_volume(1)
	
	setup_status = "None"
	
	while True:
		display.fill(BLACK)
		
		if setup_status == "None":
			if mode == "Classic":
				display.blit(pygame.image.load("classic_menu.png"), (0, 0))
			if mode == "Two Player":
				display.blit(pygame.image.load("two_player_menu.png"), (0, 0))
			if mode == "Obstacle Course":
				display.blit(pygame.image.load("obstacle_menu.png"), (0, 0))
			if mode == "Strategy":
				display.blit(pygame.image.load("strategy_menu.png"), (0, 0))
			
			play_rect = pygame.rect.Rect((0, 214), (355, 49))  # Rect where the play button would be clicked
			setup_rect = pygame.rect.Rect((0, 280), (358, 49))
		elif setup_status == "Option":
			display.blit(pygame.image.load("setup_menu.png"), (0, 0))
			
			game_mode_rect = pygame.rect.Rect(0, 290, 358, 30)
			pygame.draw.rect(display, BLACK, pygame.rect.Rect(0, 330, 358, 30))  # Hide a GUI mistake I made
		elif setup_status == "Game Mode":
			display.blit(pygame.image.load("game_mode_menu.png"), (0, 0))
		
		classic_rect = pygame.rect.Rect((0, 214), (276, 49))
		two_player_rect = pygame.rect.Rect((0, 280), (276, 49))
		obstacle_rect = pygame.rect.Rect((0, 348), (278, 49))
		strategy_rect = pygame.rect.Rect((0, 420), (278, 49))
		
		options_rect = pygame.rect.Rect((0, 585), (300, 49))
		back_rect = pygame.rect.Rect((0, 650), (300, 49))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				if setup_status == "None":
					if play_rect.collidepoint(mouse_pos):
						game(mode)
					if setup_rect.collidepoint(mouse_pos):
						setup_status = "Option"
					if options_rect.collidepoint(mouse_pos):
						options(play_menu)
					if back_rect.collidepoint(mouse_pos):
						main_menu()
				elif setup_status == "Option":
					if game_mode_rect.collidepoint(mouse_pos):
						setup_status = "Game Mode"
					else:
						setup_status = "None" # If you click anywhere else, you go back to the default
				elif setup_status == "Game Mode":
					if classic_rect.collidepoint(mouse_pos):
						mode = "Classic"
					elif two_player_rect.collidepoint(mouse_pos):
						mode = "Two Player"
					elif obstacle_rect.collidepoint(mouse_pos):
						mode = "Obstacle Course"
					elif strategy_rect.collidepoint(mouse_pos):
						mode = "Strategy"
					
					setup_status = "None"
		
		key = pygame.key.get_pressed()
		
		if key[pygame.K_ESCAPE]:
			main_menu()
		
		clock.tick(FPS)
		pygame.display.update()


# Main Menu
def main_menu():
	# Main menu screen
	# Music
	if music == "On":
		pygame.mixer.music.load("menu_music.mp3")
		pygame.mixer.music.play(-1)
	else:
		pygame.mixer.music.stop()
	
	while True:
		display.fill(BLACK)
		
		display.blit(pygame.image.load("main_menu.png"), (0, 0))
		
		play_rect = pygame.rect.Rect((0, 214), (355, 65))  # Rect where the play button would be clicked
		options_rect = pygame.rect.Rect((0, 285), (355, 65))
		quit_rect = pygame.rect.Rect((0, 360), (355, 49))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				if play_rect.collidepoint(mouse_pos):
					play_menu()
				if options_rect.collidepoint(mouse_pos):
					options(main_menu)
				if quit_rect.collidepoint(mouse_pos):
					exit()
		
		clock.tick(FPS)
		pygame.display.update()


if __name__ == "__main__":
	main_menu()
