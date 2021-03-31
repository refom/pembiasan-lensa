import pygame

from pygame import gfxdraw
from pygame.math import Vector2


class COLORS:
	# Color
	white = (255,255,255)
	whitesmoke = (245,245,245)
	gray = (150,150,150)
	black = (0,0,0)

	red = (255, 0, 0)
	deeppink = (255,20,147)

	green = (0, 255, 0)
	greenyellow = (173,255,47)
	green2 = (0,170,0)
	dark_green = (0,100,0)

	blue = (0, 0, 255)
	deepskyblue = (0,191,255)

	fg_color = white
	bg_color = black

class FontText:
	pygame.font.init()
	title = None
	normal = None
	empty = None

	@classmethod
	def update(cls):
		cls.font_22 = pygame.font.Font(cls.empty, 22)
		cls.font_small = pygame.font.Font(cls.normal, 18)
		cls.font_normal = pygame.font.Font(cls.normal, 24)
		cls.font_semi_normal = pygame.font.Font(cls.normal, 21)
		cls.font_title = pygame.font.Font(cls.title, 100)
		cls.font_h1 = pygame.font.Font(cls.normal, 80)
		cls.font_h2 = pygame.font.Font(cls.normal, 60)
		cls.font_h3 = pygame.font.Font(cls.normal, 40)

	@staticmethod
	def render(surface, font, pos, text, aa, color):
		teks = font.render(str(text), aa, color)
		surface.blit(teks, teks.get_rect(center=pos))


class Button:
	all_buttons = []
	static_buttons = []
	revers = False

	def __init__(self, xy, wh, text, statik=False, font=None, shade=True):
		self.rect = pygame.Rect((0,0), wh)
		self.pos = Vector2(xy)
		self.text = text
		self.shade = shade

		if font:
			self.font = font
		else:
			self.font = FontText.font_h3

		if statik:
			self.static_buttons.append(self)
		else:
			self.all_buttons.append(self)

	def render(self, surface, mouse_pos):
		self.rect.center = self.pos.xy
		hover = COLORS.gray

		if self.revers:
			fg_color = COLORS.bg_color
			bg_color = COLORS.fg_color
		else:
			fg_color = COLORS.fg_color
			bg_color = COLORS.bg_color

		if self.check_collisions(mouse_pos):
			pygame.draw.rect(surface, hover, self.rect, 0, 5)
			
			FontText.render(surface, self.font, self.pos.xy, self.text, True, fg_color)
		else:
			# Background
			pygame.draw.rect(surface, hover, self.rect, 0, 5)
			self.rect.center = (self.pos.x - 5, self.pos.y - 5)
			pygame.draw.rect(surface, bg_color, self.rect, 0, 5)

			# Text
			if self.shade:
				FontText.render(surface, self.font, self.pos.xy, self.text, True, hover)
			pos = (self.pos.x - 2, self.pos.y - 2)
			FontText.render(surface, self.font, pos, self.text, True, fg_color)


	def check_collisions(self, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			return True

	@classmethod
	def check_all_col(cls, mouse_pos):
		for btn in cls.all_buttons:
			if btn.check_collisions(mouse_pos):
				return True
		for btn in cls.static_buttons:
			if btn.check_collisions(mouse_pos):
				return True

	@classmethod
	def clear_all(cls):
		cls.all_buttons.clear()


def DDA(xy1, xy2, surface, color):
	# Variabel lokal
	x = xy1[0]
	y = xy1[1]

	# Ambil Panjangnya kordinat
	dx = xy2[0] - xy1[0]
	dy = xy2[1] - xy1[1]

	# Ambil kordinat ter-panjang
	step = int(max(abs(dx), abs(dy)))

	# Ambil butuh brapa increment untuk x dan y
	try:
		xinc = dx/step
	except ZeroDivisionError:
		xinc = 0
	try:
		yinc = dy/step
	except ZeroDivisionError:
		yinc = 0

	# Gambar garisnya
	for i in range(step):
		x += xinc
		y += yinc
		try:
			gfxdraw.pixel(surface, round(x), round(y), color)
		except:
			x = int(x)
			y = int(y)


class CvCoor:
	size = (0, 0)
	
	# Kuadran II
	@classmethod
	def x(cls, x):
		return (cls.size[0]//2 + x * -1)

	@classmethod
	def y(cls, y):
		return (cls.size[1]//2 + y * -1)

	@classmethod
	def xy(cls, x, y):
		return cls.x(x), cls.y(y)

	@classmethod
	def update(cls, size):
		cls.size = (int(size[0]), int(size[1]))

# Mencari Gradien/Slope
def gradien(xy1, xy2):
	try:
		m = (xy2[1] - xy1[1]) / (xy2[0] - xy1[0])
	except ZeroDivisionError:
		m = 0
	return m

# Mencari Persamaan garis
def persamaan(xy1, xy2, panjang):
	m = gradien(xy1, xy2)
	y = xy2[1] + m * (panjang - xy2[0])
	return panjang, y


class InputBox:
	all_input_box = []

	def __init__(self, xy, wh, value, func_set, func_get):
		self.rect = pygame.Rect(xy, wh)
		self.value = value
		self.text = str(value)
		self.active = False
		self.change = False
		self.func_set = func_set
		self.func_get = func_get
		self.all_input_box.append(self)

	@classmethod
	def handle_event(cls, events):
		for event in events:
			for i_box in cls.all_input_box:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if i_box.rect.collidepoint(event.pos):
						i_box.active = not i_box.active
					else:
						i_box.active = False

				if event.type == pygame.KEYDOWN:
					if i_box.active:
						if event.key == pygame.K_RETURN:
							try:
								i_box.value = int(i_box.text)
							except:
								i_box.value = 100
							i_box.active = False
							i_box.change = True
						elif event.key == pygame.K_BACKSPACE:
							i_box.text = i_box.text[:-1]
						else:
							i_box.text += event.unicode

	def render(self, surface):
		if self.active:
			text_obj = FontText.font_normal.render(str(self.text), True, COLORS.green2)
		else:
			self.text = str(self.value)
			text_obj = FontText.font_normal.render(str(self.text), True, COLORS.black)
		surface.blit(text_obj, (self.rect.x, self.rect.y))

	@classmethod
	def update_box(cls):
		for box in cls.all_input_box:
			if box.change:
				box.func_set(box.value)
				box.change = False
			else:
				box.value = abs(box.func_get())

	def check_collisions(self, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			return True

	@classmethod
	def check_all_col(cls, mouse_pos):
		if cls.all_input_box:
			for box in cls.all_input_box:
				if box.check_collisions(mouse_pos):
					return True

	@classmethod
	def clear_all(cls):
		cls.all_input_box.clear()
