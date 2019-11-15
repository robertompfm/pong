"""
CODE OF GAME PONG
The game Pong was one of the projects of the course Introduction to Interactive Programing with Python by Rice University through Coursera
This is an adapted version of the project I submitted, this time I did using pygame instead of simpleGUI
there are still a lot of things to improve but I am happy with the result, it was a good exercise 
"""

# importing modules used in the code

import pygame
import random

# initialize pygame
pygame.init()


# initialize global constants
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
LEFT = False
RIGHT = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 , 255)



class PongGame:
	"""
	class that will manage the game loop
	"""
	def __init__(self):
		"""
		initialize game settings
		"""
		# variables that won't change
		self._display_width = WIDTH
		self._display_height = HEIGHT
		self._in_game = True
		self._right = RIGHT
		self._left = LEFT
		self._color = WHITE
		self._background = BLACK
		self._lines_color = BLUE
		self._half_pad_width = HALF_PAD_WIDTH

		# initialize display
		self.display = pygame.display.set_mode((self._display_width, self._display_height))
		pygame.display.set_caption("PONG")		

		# initializing ball object
		self.ball = Ball(BALL_RADIUS, self.display, self._color)

		# initialize paddle objects
		pad1_xcoord = WIDTH - HALF_PAD_WIDTH
		pad2_xcoord = HALF_PAD_WIDTH

		self.paddle1 = Paddle(PAD_WIDTH, PAD_HEIGHT, pad1_xcoord, self._color, self.display)
		self.paddle2 = Paddle(PAD_WIDTH, PAD_HEIGHT, pad2_xcoord, self._color, self.display)

		#initialize scores
		score1_pos = (int((3/4)*self._display_width),int((1/8)*self._display_width))
		score2_pos = (int((1/4)*self._display_width),int((1/8)*self._display_width))
		self.score1 = Score(score1_pos, self._color, self.display)
		self.score2 = Score(score2_pos, self._color, self.display)


	def new_game(self):
		"""
		start a new game
		"""
		# setting initial values
		self.score1.reset_score()
		self.score2.reset_score()
		self.paddle1.set_position(HEIGHT // 2)
		self.paddle2.set_position(HEIGHT // 2)
		self.spawn_direction = self._right
		
		# spawn ball
		self.ball.spawn(self.spawn_direction)


	def loop(self):
		"""
		game loop
		"""
		self.clock = pygame.time.Clock()
		self.new_game()

		while self._in_game:
			for event in pygame.event.get():
				self.check_quit(event)
				self.check_keydown(event)
				self.check_keyup(event)

			self.paddle1.update_position()
			self.paddle2.update_position()
			
			self.ball.update_position()

			self.check_goal([self.paddle1, self.paddle2], self.ball)

			self.display.fill(self._background)

			self.draw_lines()
			self.paddle1.draw_paddle()
			self.paddle2.draw_paddle()
			self.ball.draw_ball()
			self.score1.blit_score()
			self.score2.blit_score()
			pygame.display.update()
			self.clock.tick(60)


	# here starts auxiliary and event handling functions...
	def change_game_state(self):
		"""
		change the game state, it should become false to quit the game
		"""
		if self._in_game:
			self._in_game = False
		else:
			self._in_game = True


	def change_spawn_direction(self):
		"""
		change the spawn direction
		"""
		current_direction = self.spawn_direction
		if current_direction == self._right:
			self.spawn_direction = self._left
		else:
			self.spawn_direction = self._right


	def draw_lines(self):
		"""
		draw three lines on the pong field
		"""
		line1_y_axis = self._display_width - self.paddle1.get_width()
		start_pos_line1 = (line1_y_axis, 0)
		end_pos_line1 = (line1_y_axis, self._display_height)

		line2_y_axis = self._display_width // 2
		start_pos_line2 = (line2_y_axis, 0)
		end_pos_line2 = (line2_y_axis, self._display_height)

		line3_y_axis = self.paddle2.get_width()
		start_pos_line3 = (line3_y_axis, 0)
		end_pos_line3 = (line3_y_axis, self._display_height)		

		pygame.draw.line(self.display, self._lines_color, start_pos_line1, end_pos_line1)
		pygame.draw.line(self.display, self._lines_color, start_pos_line2, end_pos_line2)
		pygame.draw.line(self.display, self._lines_color, start_pos_line3, end_pos_line3)


	# setting event handlers
	def check_quit(self, event):
		"""
		if quit button is pressed it changes the game state and quits
		"""
		if event.type == pygame.QUIT:
			self.change_game_state()


	def check_keydown(self, event):
		"""
		event handler for keydown events
		"""
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.paddle1.set_velocity(-7)
			if event.key == pygame.K_DOWN:
				self.paddle1.set_velocity(7)
			if event.key == pygame.K_w:
				self.paddle2.set_velocity(-7)
			if event.key == pygame.K_s:
				self.paddle2.set_velocity(7)


	def check_keyup(self, event):
		"""
		event handler for keyup events
		"""
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				self.paddle1.set_velocity(0)
			if event.key == pygame.K_DOWN:
				self.paddle1.set_velocity(0)
			if event.key == pygame.K_w:
				self.paddle2.set_velocity(0)
			if event.key == pygame.K_s:
				self.paddle2.set_velocity(0)


	def check_goal(self, paddles, ball):
		"""
		check for ball x paddle collision
		if a collision occur the ball should bounce
		"""
		mid_point = self._display_width // 2
		ball_center = ball.get_position()
		ball_radius = ball.get_radius()
		ball_right = ball_center[0] + ball_radius
		ball_left = ball_center[0] - ball_radius
		for paddle in paddles:
			paddle_rect = paddle.get_rectangle()
			if (ball_right >= paddle_rect.left) and (paddle_rect.left > mid_point):
				if paddle_rect.collidepoint(ball_right, ball_center[1]):
					new_x_pos = (2 * paddle_rect.left - ball_right - ball_radius)
					ball.set_position([new_x_pos, ball_center[1]])
					ball.bounce(1.05)
				else:
					self.score2.update_score()
					self.change_spawn_direction()
					ball.spawn(self.spawn_direction)

			elif (ball_left <= paddle_rect.right) and (paddle_rect.right < mid_point):
				if paddle_rect.collidepoint(ball_left, ball_center[1]):
					new_x_pos = (2 * paddle_rect.right - ball_left + ball_radius)
					ball.set_position([new_x_pos, ball_center[1]])
					ball.bounce(1.05)
				else:
					self.score1.update_score()
					self.change_spawn_direction()
					ball.spawn(self.spawn_direction)


###############################################################################################################


# BALL CLASS STARTS HERE....
class Ball:
	"""
	class to create and draw a ball
	"""
	def __init__(self, radius, display, color):
		"""
		initialize the ball
		"""
		# variables that won't change value
		self._radius = radius
		self._display = display
		self._color = color

		# variables that will change value
		self.position = [self._display.get_width() // 2, self._display.get_height() // 2]
		self.velocity = [0, 0]


	def spawn(self, direction):
		"""
		spawn ball from the center, the ball goes upper right if true, and upper left if false
		"""
		self.position = [self._display.get_width() // 2, self._display.get_height() // 2]
		if direction:
			self.velocity = [(random.randrange(12,24)/10.0),-(random.randrange(6,18)/10.0)]
		else:
			self.velocity = [-(random.randrange(12,24)/10.0),-(random.randrange(6,18)/10.0)]


	def update_position(self):
		"""
		update the ball position based on its speed
		"""
		self.position[0] += self.velocity[0] # update x position
		self.position[1] += self.velocity[1] # update y position

		self.boundary_collision() # check collision with the borders


	def boundary_collision(self):
		"""
		if the ball collides with the boundary the ball will bounce
		"""
		upper_boundary = self._radius
		lower_boundary = (self._display.get_height() - self._radius)
		
		if self.position[1] <= upper_boundary:
			self.position[1] = 2 * upper_boundary - self.position[1]
			self.velocity[1] *= -1

		if self.position[1] >= lower_boundary:
			self.position[1] = lower_boundary - (self.position[1] % lower_boundary)
			self.velocity[1] *= -1


	def draw_ball(self):
		"""
		draw the ball on the display
		"""
		x_position = int(self.position[0])
		y_position = int(self.position[1])
		pygame.draw.circle(self._display, self._color, [x_position, y_position], self._radius)


	def get_position(self):
		"""
		returns current position
		"""
		return self.position


	def set_position(self, new_coord):
		"""
		set a new pair of coordinates as ball position
		"""
		self.position = new_coord


	def get_velocity(self):
		"""
		returns current velocity
		"""
		return self.velocity


	def set_velocity(self, new_vel):
		"""
		set a new pair of values as ball velocity
		"""
		self.velocity = new_vel


	def bounce(self, num = 1):
		"""
		bounce the ball on the paddle and allow change in the speed
		"""
		self.velocity[0] *= -num
		self.velocity[1] *= num
	

	def get_radius(self):
		"""
		returns the ball radius value
		"""
		return self._radius



#############################################################################################################################

# PADDLE CLASS STARTS HERE...
class Paddle:
	"""
	class to create and draw the paddles
	"""
	def __init__(self, width, height, x_coord, color, display):
		"""
		initializes a paddle
		"""
		# variables that won't change value
		self._width, self._height = width, height
		self._color = color
		self._display = display
		self._x_coord = x_coord
		
		# variable that will change value throughout the game
		self.rectangle = pygame.Rect((0 , 0), (self._width, self._height))
		self.rectangle.center = (self._x_coord, int(self._display.get_height() / 2))
		self.vel = 0


	def update_position(self):
		"""
		updates the paddle position
		"""
		self.rectangle.top += self.vel
		self.keep_on_screen()
		

	def keep_on_screen(self):
		"""
		prevents the paddling from passing through the boundaries 
		"""
		if (self.rectangle.bottom > self._display.get_height()):
			self.set_position(self._display.get_height() - self._height)
		elif (self.rectangle.top < 0):
			self.set_position(0)


	def set_position(self, topPos):
		"""
		change the paddle y coordinate
		"""
		self.rectangle.top = topPos


	def get_position(self):
		"""
		return the paddle's center position coordinates as a tuple
		"""
		return self.rectangle.center


	def set_velocity(self, vel):
		"""
		set a number as velocity on y direction
		"""
		self.vel = vel


	def get_velocity(self):
		"""
		returns the current velocity on y direction
		"""
		return self.vel


	def get_rectangle(self):
		"""
		returns the paddle's rectangle
		"""
		return self.rectangle


	def draw_paddle(self):
		"""
		command to draw the paddle
		"""
		pygame.draw.rect(self._display, self._color, self.rectangle)
	

	def get_width(self):
		"""
		get paddle width
		"""
		return self._width


############################################################################################################################
# SCORE CLASS STARTS HERE...

class Score:
	"""
	class that will handle the game score
	"""
	def __init__(self, center_pos, color, display):
		"""
		initializing socre
		"""
		self._display = display
		self._color = color
		self._center_pos = center_pos
		self._font = pygame.font.Font("freesansbold.ttf", 40) 
		
		self.score = 0
	

	def update_score(self):
		"""
		update the score value by one
		"""
		self.score += 1

	
	def get_score(self):
		"""
		returns current score
		"""
		return self.score


	def set_score(self, new_val):
		"""
		set a new value to score
		"""
		self.score = new_val


	def reset_score(self):
		"""
		resets the score to zero
		"""
		self.score = 0


	def blit_score(self):
		"""
		draws the score on the screen
		"""
		text_surface = self._font.render(str(self.get_score()), True, self._color)
		text_rect = text_surface.get_rect()
		text_rect.center = self._center_pos
		self._display.blit(text_surface, text_rect)



###############################################################################################################################


# callling the game and starting the loop
new_game = PongGame()
new_game.loop()

pygame.quit()
quit()