import pygame

from pygame.math import Vector2
from utility import DDA, CvCoor, COLORS, FontText, persamaan, Button, InputBox, Tema

class Kartesius:
	pos = Vector2(0, 0)
	fokus = 100

	@classmethod
	def render(cls, surface, menu):
		color = COLORS.fg_color

		x, y = CvCoor.xy(cls.pos.x, cls.pos.y)
		DDA((0, y), (CvCoor.size[0], y), surface, color) # X
		DDA((x, 0), (x, CvCoor.size[1]), surface, color) # y

		x, y = CvCoor.x(cls.fokus), CvCoor.y(cls.pos.y)
		DDA((x, y), (x, y - 10), surface, color) # F
		FontText.render(surface, FontText.font_22, (x, y - 25), "f", True, color)

		x = CvCoor.x(cls.fokus * 2)
		DDA((x, y), (x, y - 10), surface, color) # 2F
		FontText.render(surface, FontText.font_22, (x, y - 25), "r", True, color)

		if menu.cembung:
			x = CvCoor.x(cls.fokus * -1)
			DDA((x, y), (x, y - 10), surface, color) # F Mirror
			FontText.render(surface, FontText.font_22, (x, y - 25), "f", True, color)

			x = CvCoor.x(cls.fokus * 2 * -1)
			DDA((x, y), (x, y - 10), surface, color) # 2F Mirror
			FontText.render(surface, FontText.font_22, (x, y - 25), "r", True, color)

	@classmethod
	def handle_movement(cls, key_pressed, mouse_pressed, mouse_pos):
		if key_pressed[pygame.K_q]:
			cls.fokus += 1
		if key_pressed[pygame.K_e]:
			cls.fokus -= 1

		if mouse_pressed[2] and not Button.check_all_col(mouse_pos) and not InputBox.check_all_col(mouse_pos):
			cls.fokus = (mouse_pos[0] - CvCoor.size[0]//2) * -1

	@classmethod
	def handle_mirror(cls):
		if cls.fokus < 0:
			cls.fokus *= -1

	@classmethod
	def set_fokus(cls, value):
		cls.fokus = value

	@classmethod
	def get_fokus(cls):
		return cls.fokus

class Benda:
	jarak = 200
	tinggi = 100
	sinar_1 = 0
	sinar_2 = 0
	mirror_x = False
	mirror_y = False
	color_awal = COLORS.green
	color_pantul = COLORS.greenyellow

	@classmethod
	def render_cembung(cls, surface):

		x, y = CvCoor.xy(cls.jarak, cls.tinggi)
		kt_x, kt_y = CvCoor.xy(Kartesius.pos.x, Kartesius.pos.y)
		fokus = CvCoor.x(Kartesius.fokus * -1)

		cls.draw(surface, x, y, kt_y)

		# Sinar A ke garis kartesius
		x_new, y_new = persamaan((kt_x, y), (0, y), cls.sinar_1)
		pygame.draw.line(surface, cls.color_awal, (kt_x, y), (x_new, y_new))

		# Sinar A ke fokus
		x_new, y_new = persamaan((kt_x, y), (fokus, kt_y), cls.sinar_2)
		pygame.draw.line(surface, cls.color_pantul, (kt_x, y), (x_new, y_new))

		# Sinar C
		x_new, y_new = persamaan((kt_x, kt_y), (x, y), 0)
		pygame.draw.line(surface, COLORS.blue, (kt_x, kt_y), (x_new, y_new))

	@classmethod
	def render_cekung(cls, surface):
		x, y = CvCoor.xy(cls.jarak, cls.tinggi)
		kt_x, kt_y = CvCoor.xy(Kartesius.pos.x, Kartesius.pos.y)
		bayangan_x, bayangan_y = CvCoor.xy(Bayangan.jarak, Bayangan.tinggi * -1)

		cls.draw(surface, x, y, kt_y)

		# Sinar A ke garis kartesius
		pygame.draw.line(surface, cls.color_awal, (kt_x, y), (x, y))

		# Sinar A ke fokus
		pygame.draw.line(surface, cls.color_pantul, (kt_x, y), (bayangan_x, bayangan_y))

	@classmethod
	def draw(cls, surface, x, y, kt_y):
		# Gambar benda
		img = pygame.transform.flip(Tema.curr_chr, cls.mirror_x, cls.mirror_y)
		size = img.get_size()
		w, h = cls.tinggi * size[0]//size[1], cls.tinggi
		if w < 0:
			w *= -1
		if h < 0:
			h *= -1
		if w > 1000:
			w = 1000
		if h > 1000:
			h = 1000
		img = pygame.transform.scale(img, (w, h))
		rect = img.get_rect(topleft=(x, y))
		if cls.mirror_y:
			rect = img.get_rect(bottomleft=(x, y + 1))
		surface.blit(img, rect)

		pygame.draw.line(surface, COLORS.fg_color, (x, kt_y), (x, y))

	@classmethod
	def handle_mirror(cls):
		# Kalau gak mirror
		if cls.jarak < 0:
			cls.mirror_x = True
			cls.sinar_1 = CvCoor.size[0]

			if cls.jarak >= Kartesius.fokus:
				cls.sinar_2 = 0
			else:
				cls.sinar_2 = CvCoor.size[0]
		else:
			# Kalau mirror
			cls.mirror_x = False
			cls.sinar_1 = 0

			if cls.jarak <= Kartesius.fokus:
				cls.sinar_2 = 0
			else:
				cls.sinar_2 = CvCoor.size[0]

		if cls.tinggi < 0:
			cls.mirror_y = True
		else:
			cls.mirror_y = False

	@classmethod
	def handle_movement(cls, key_pressed, mouse_pressed, mouse_pos):
		if key_pressed[pygame.K_a]:
			cls.jarak += 1
		if key_pressed[pygame.K_d]:
			cls.jarak -= 1
		if key_pressed[pygame.K_w]:
			cls.tinggi += 1
		if key_pressed[pygame.K_s]:
			cls.tinggi -= 1

		if mouse_pressed[0] and not Button.check_all_col(mouse_pos) and not InputBox.check_all_col(mouse_pos):
			cls.jarak = (mouse_pos[0] - CvCoor.size[0]//2) * -1
			cls.tinggi = (mouse_pos[1] - CvCoor.size[1]//2) * -1

	@classmethod
	def set_jarak(cls, value):
		cls.jarak = value

	@classmethod
	def get_jarak(cls):
		return abs(cls.jarak)

	@classmethod
	def set_tinggi(cls, value):
		cls.tinggi = value

	@classmethod
	def get_tinggi(cls):
		return cls.tinggi

class Bayangan:
	jarak = 0
	tinggi = 0
	mirror_x = True
	mirror_y = True

	@classmethod
	def update(cls):
		try:
			cls.jarak = int((Kartesius.fokus * Benda.jarak) / (Benda.jarak - Kartesius.fokus))
		except ZeroDivisionError:
			cls.jarak = 0
		try:
			cls.tinggi = int((cls.jarak / Benda.jarak) * Benda.tinggi)
		except ZeroDivisionError:
			cls.tinggi = 0

	@classmethod
	def render_cembung(cls, surface):

		# Convert Kordinat
		x, y = CvCoor.xy(cls.jarak * -1, cls.tinggi * -1)
		kt_x, kt_y = CvCoor.xy(Kartesius.pos.x, Kartesius.pos.y)
		fokus = CvCoor.x(Kartesius.fokus)

		cls.draw(surface, x, y, kt_y)

		# Sinar B ke garis kartesius
		x_new, y_new = persamaan((kt_x, y), (0, y), Benda.sinar_2)
		pygame.draw.line(surface, COLORS.deeppink, (kt_x, y), (x_new, y_new))

		# Sinar B ke fokus
		x_new, y_new = persamaan((kt_x, y), (fokus, kt_y), Benda.sinar_1)
		pygame.draw.line(surface, COLORS.red, (kt_x, y), (x_new, y_new))

		# Sinar C
		x_new, y_new = persamaan((kt_x, kt_y), (x, y), CvCoor.size[0])
		pygame.draw.line(surface, COLORS.deepskyblue, (kt_x, kt_y), (x_new, y_new))

	@classmethod
	def render_cekung(cls, surface):
		x, y = CvCoor.xy(cls.jarak, cls.tinggi * -1)
		kt_x, kt_y = CvCoor.xy(Kartesius.pos.x, Kartesius.pos.y)
		benda_x, benda_y = CvCoor.xy(Benda.jarak, Benda.tinggi)

		cls.draw(surface, x, y, kt_y)

		# Sinar B ke garis kartesius
		pygame.draw.line(surface, COLORS.deeppink, (kt_x, y), (x, y))

		# Sinar B ke fokus
		pygame.draw.line(surface, COLORS.red, (kt_x, y), (benda_x, benda_y))

	@classmethod
	def draw(cls, surface, x, y, kt_y):
		# Bayangan
		img = pygame.transform.flip(Tema.curr_chr, cls.mirror_x, cls.mirror_y)
		img.set_alpha(155)
		size = img.get_size()
		w, h = cls.tinggi * size[0]//size[1], cls.tinggi
		if w < 0:
			w *= -1
		if h < 0:
			h *= -1
		if w > 1000:
			w = 1000
		if h > 1000:
			h = 1000
		img = pygame.transform.scale(img, (w, h))
		rect = img.get_rect(topleft=(x, y))
		if cls.mirror_y:
			rect = img.get_rect(bottomleft=(x, y + 1))
		surface.blit(img, rect)

		pygame.draw.line(surface, COLORS.fg_color, (x, kt_y), (x, y))

	@classmethod
	def handle_mirror(cls, menu):
		if menu.cembung:
			if cls.jarak < 0:
				cls.mirror_x = False
			else:
				cls.mirror_x = True
		else:
			if cls.jarak < 0:
				cls.mirror_x = True
			else:
				cls.mirror_x = False

		if cls.tinggi < 0:
			cls.mirror_y = False
		else:
			cls.mirror_y = True

