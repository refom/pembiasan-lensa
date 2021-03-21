import pygame
from pygame import gfxdraw

if not pygame.font:
	print("Font gak ada")

pygame.init()
pygame.display.set_caption("Pembiasan Cahaya")
SCREEN = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 120

# Color
WHITE = (255,255,255)
WHITESMOKE = (245,245,245)
LIGHT_GRAY = (200,200,200)
GRAY = (150,150,150)
DARK_GRAY = (50,50,50,128)
DARK_GRAY2 = (50,50,50,90)
BLACK = (0,0,0)

RED = (255, 0, 0)
DEEPPINK = (255,20,147)

GREEN = (0, 255, 0)
GREEN2 = (0,128,0)
DARK_GREEN = (0,100,0)
GREENYELLOW = (173,255,47)

BLUE = (0, 0, 255)
DEEPSKYBLUE = (0,191,255)

"""
RUMUS
Jarak Bayangan = (Fokus * Jarak Benda) / (Jarak Benda - Fokus)
Tinggi Bayangan = (Jarak Bayangan / Jarak Benda) * Tinggi Benda
"""

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

# DDA
def DDA(xy1, xy2):
	# Variabel lokal
	x = xy1[0]
	y = xy1[1]

	# Ambil Panjangnya kordinat
	dx = xy2[0] - xy1[0]
	dy = xy2[1] - xy1[1]

	# Ambil kordinat ter-panjang
	step = max(abs(dx), abs(dy))

	try:
		# Ambil butuh brapa increment untuk x dan y
		xinc = dx/step
	except ZeroDivisionError:
		xinc = 0
	else:
		try:
			yinc = dy/step
		except ZeroDivisionError:
			yinc = 0

	# Gambar garisnya
	for i in range(step):
		x += xinc
		y += yinc
		try:
			gfxdraw.pixel(SCREEN, round(x), round(y), fg_color)
		except:
			x = int(x)
			y = int(y)

# Convert Kordinat
class CvCoor:
	# Kuadran II
	@staticmethod
	def x(x):
		return (width//2) + x * -1

	@staticmethod
	def y(y):
		return (height//2) + y * -1

	@staticmethod
	def xy(x, y):
		return CvCoor.x(x), CvCoor.y(y)

class Kartesius:
	x = 0
	y = 0
	fokus = 100
	fokus_mirror = False

	@classmethod
	def handle_movement(cls, key_pressed, mouse_pressed):
		if key_pressed[pygame.K_q]:
			cls.fokus -= 1
		if key_pressed[pygame.K_e]:
			cls.fokus += 1
		
		if key_pressed[pygame.K_1]:
			print(int(clock.get_fps()))

		if mouse_pressed[2]:
			mouse_pos = pygame.mouse.get_pos()
			cls.fokus = (mouse_pos[0] - width//2) * -1

	@classmethod
	def handle_mirror(cls):
		if cls.fokus < 0:
			cls.fokus_mirror = True
			cls.fokus *= -1
		else:
			cls.fokus_mirror = False

	@classmethod
	def draw(cls):
		x, y = CvCoor.xy(cls.x, cls.y)
		DDA((0, y), (width, y)) # x
		DDA((x, 0), (x, height)) # y

	@classmethod
	def draw_fokus(cls):
		x, y = CvCoor.x(cls.fokus), CvCoor.y(cls.y)
		DDA((x, y), (x, y - 10)) # F
		Kartesius.draw_text("f", x, y)
		
		x = CvCoor.x(cls.fokus * -1)
		DDA((x, y), (x, y - 10)) # F Mirror
		Kartesius.draw_text("f", x, y)

		x = CvCoor.x(cls.fokus * 2)
		DDA((x, y), (x, y - 10)) # 2F
		Kartesius.draw_text("r", x, y)

		x = CvCoor.x(cls.fokus * 2 * -1)
		DDA((x, y), (x, y - 10)) # 2F Mirror
		Kartesius.draw_text("r", x, y)

	@staticmethod
	def draw_text(teks, x, y):
		font = pygame.font.Font(None, 24)
		text = font.render(teks, False, fg_color)
		textpos = text.get_rect(centerx=x, centery=y - 20)
		SCREEN.blit(text, textpos)

class Benda:
	jarak = 200
	tinggi = 100
	panjang_sinar1 = 0
	panjang_sinar2 = 0

	@classmethod
	def draw(cls):
		# Kordinat Kartesius
		kt_x, kt_y = CvCoor.xy(Kartesius.x, Kartesius.y)

		# Kordinat Fokus
		if Kartesius.fokus_mirror:
			fokus = CvCoor.x(Kartesius.fokus)
		else:
			fokus = CvCoor.x(Kartesius.fokus * -1)

		# Kordinat Benda
		x, y = CvCoor.xy(cls.jarak, cls.tinggi)
		# Gambar Benda
		DDA((x, kt_y), (x, y))
		# kalau ada night mode, set warna
		if Button.night_mode:
			color_awal = GREEN
			color_pantul = GREENYELLOW
		else:
			color_awal = DARK_GREEN
			color_pantul = GREEN2

		"""
			Algoritma Sinar A
		1. gambar garis dari titik x kartesius ke 0 (garis kebelakang)
		2. gambar garis dari titik x kartesius ke titik fokus seberang
		Panjang sinar 1 = sinar lurus
		Panjang sinar 2 = sinar ke fokus
		"""

		# Sinar A ke garis kartesius
		x_a1, y_a1 = persamaan((kt_x, y), (0, y), cls.panjang_sinar1)
		pygame.draw.line(SCREEN, color_awal, (kt_x, y), (x_a1, y_a1))

		# Sinar A ke fokus
		x_a2, y_a2 = persamaan((kt_x, y), (fokus, kt_y), cls.panjang_sinar2)
		pygame.draw.line(SCREEN, color_pantul, (kt_x, y), (x_a2, y_a2))

		# Sinar C
		x_new, y_new = persamaan((kt_x, kt_y), (x, y), 0)
		pygame.draw.line(SCREEN, BLUE, (kt_x, kt_y), (x_new, y_new))

	@classmethod
	def handle_mirror(cls):
		# Kalau gak mirror
		if cls.jarak < Kartesius.x:
			cls.panjang_sinar1 = width

			if cls.jarak >= Kartesius.fokus:
				cls.panjang_sinar2 = 0
			else:
				cls.panjang_sinar2 = width
		else:
			# Kalau mirror
			cls.panjang_sinar1 = 0

			if cls.jarak <= Kartesius.fokus:
				cls.panjang_sinar2 = 0
			else:
				cls.panjang_sinar2 = width

	@classmethod
	def handle_movement(cls, key_pressed, mouse_pressed):
		if key_pressed[pygame.K_a]:
			cls.jarak += 1
		if key_pressed[pygame.K_d]:
			cls.jarak -= 1
		if key_pressed[pygame.K_w]:
			cls.tinggi += 1
		if key_pressed[pygame.K_s]:
			cls.tinggi -= 1
		
		if mouse_pressed[0]:
			mouse_pos = pygame.mouse.get_pos()
			cls.jarak = (mouse_pos[0] - width//2) * -1
			cls.tinggi = (mouse_pos[1] - height//2) * -1

class Bayangan:
	jarak = 0
	tinggi = 0

	@classmethod
	def update(cls):
		try:
			cls.jarak = int((Kartesius.fokus * Benda.jarak) / (Benda.jarak - Kartesius.fokus))
		except ZeroDivisionError:
			cls.jarak = 0
		else:
			try:
				cls.tinggi = int((cls.jarak / Benda.jarak) * Benda.tinggi)
			except ZeroDivisionError:
				cls.tinggi = 0

	@classmethod
	def draw(cls):
		# Kordinat Kartesius
		kt_x, kt_y = CvCoor.xy(Kartesius.x, Kartesius.y)

		# Kordinat Fokus
		if Kartesius.fokus_mirror:
			fokus = CvCoor.x(Kartesius.fokus * -1)
		else:
			fokus = CvCoor.x(Kartesius.fokus)

		# Kordinat Bayangan
		x, y = CvCoor.xy(cls.jarak * -1, cls.tinggi * -1)
		# Gambar Bayangan
		DDA((x, kt_y), (x, y))
		# warna
		color_awal = RED
		color_pantul = DEEPPINK

		# Sinar B ke garis kartesius
		x_b1, y_b1 = persamaan((kt_x, y), (0, y), Benda.panjang_sinar2)
		pygame.draw.line(SCREEN, color_pantul, (kt_x, y), (x_b1, y_b1))

		# Sinar B ke fokus
		x_b2, y_b2 = persamaan((kt_x, y), (fokus, kt_y), Benda.panjang_sinar1)
		pygame.draw.line(SCREEN, color_awal, (kt_x, y), (x_b2, y_b2))

		# Sinar C
		x_new, y_new = persamaan((kt_x, kt_y), (x, y), width)
		pygame.draw.line(SCREEN, DEEPSKYBLUE, (kt_x, kt_y), (x_new, y_new))

class UI:
	size = 22

	@classmethod
	def render_text(cls, teks, color, font=0):
		if not font:
			font = pygame.font.Font(None, cls.size)
		text_obj = font.render(str(teks), False, color)
		return text_obj

	@classmethod
	def display_text(cls, text_obj, xy):
		SCREEN.blit(text_obj, (xy[0], xy[1]))

	@classmethod
	def draw(cls):

		# FPS
		frameps = int(clock.get_fps())
		color = GREEN
		if frameps < 30:
			color = RED
		text_obj = cls.render_text(f"FPS = {frameps}", color)
		SCREEN.blit(text_obj, (width - 100, 20))

		# Night mode
		font = pygame.font.Font(None, 48)
		text_obj = cls.render_text("N", bg_color, font)
		SCREEN.blit(text_obj, (width - 75, 60))

class Button:
	night_mode = True

	def __init__(self, x, y, w, h, color):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.rect = pygame.Rect((x, y), (w, h))
		self.color = color

	def draw(self):
		pygame.draw.rect(SCREEN, self.color, self.rect, 0, 15)

	@staticmethod
	def check_collisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
		return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)


class Menu:
	pilihan = {
		"menu": True,
		"cembung": False,
		"cekung": False,
	}

	@staticmethod
	def menu(mouse_pressed):
		# Judul
		x, y = width//8, height//5
		font = pygame.font.Font(None, 100)
		text_obj = UI.render_text("Pembiasan Cahaya", fg_color, font)
		SCREEN.blit(text_obj, (x, y))

		# Cembung
		x, y = width//7, height//2
		w, h = 300, 100
		lensa_cembung = Button(x, y, w, h, fg_color)

		# Cekung
		x, y = width//7 + width//3, height//2
		w, h = 300, 100
		cermin_cekung = Button(x, y, w, h, fg_color)

		# Handle click
		mouse_pos = pygame.mouse.get_pos()
		if Button.check_collisions(mouse_pos[0], mouse_pos[1], 3, 3, lensa_cembung.x, lensa_cembung.y, lensa_cembung.w, lensa_cembung.h):
			lensa_cembung.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["menu"] = False
				Menu.pilihan["cembung"] = True

		if Button.check_collisions(mouse_pos[0], mouse_pos[1], 3, 3, cermin_cekung.x, cermin_cekung.y, cermin_cekung.w, cermin_cekung.h):
			cermin_cekung.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["menu"] = False
				Menu.pilihan["cekung"] = True

		# Draw
		lensa_cembung.draw()
		cermin_cekung.draw()

		# Text Cembung
		font = pygame.font.Font(None, 45)
		text_obj = UI.render_text("Lensa Cembung", bg_color, font)
		text_rect = text_obj.get_rect(center=lensa_cembung.rect.center)
		SCREEN.blit(text_obj, text_rect)
		# Cekung
		text_obj = UI.render_text("Cermin Cekung", bg_color, font)
		text_rect = text_obj.get_rect(center=cermin_cekung.rect.center)
		SCREEN.blit(text_obj, text_rect)

	@staticmethod
	def cembung(key_pressed, mouse_pressed):
		# Handle Movement
		Benda.handle_movement(key_pressed, mouse_pressed)
		Kartesius.handle_movement(key_pressed, mouse_pressed)

		# Back button
		x, y = 10, 70
		w, h = 50, 30
		back = Button(x, y, w, h, fg_color)

		mouse_pos = pygame.mouse.get_pos()
		if Button.check_collisions(mouse_pos[0], mouse_pos[1], 3, 3, back.x, back.y, back.w, back.h):
			back.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["cembung"] = False
				Menu.pilihan["menu"] = True

		# Handle Bayangan
		Bayangan.update()

		# Handle Mirror
		Kartesius.handle_mirror()
		Benda.handle_mirror()

		# ===== Draw
		# Kartesius
		Kartesius.draw()
		Kartesius.draw_fokus()

		# Benda
		Benda.draw()

		# Bayangan
		Bayangan.draw()

		# Gambar info
		w, h = 370, 70
		base = pygame.Surface((w, h), pygame.SRCALPHA)
		pygame.draw.rect(base, DARK_GRAY, base.get_rect(), 0, 15)
		SCREEN.blit(base, (-10, -10))

		text_obj = UI.render_text("W A S D / Left Click : Menggerakkan Benda", fg_color)
		SCREEN.blit(text_obj, (10, 10))
		text_obj = UI.render_text("Q E / Right Click : Menggerakkan Titik Fokus", fg_color)
		SCREEN.blit(text_obj, (10, 30))

		# Gambar teks
		w, h = 220, 170
		base = pygame.Surface((w, h), pygame.SRCALPHA)
		pygame.draw.rect(base, DARK_GRAY2, base.get_rect(), 0, 15)
		SCREEN.blit(base, (-20, height - base.get_height() + 20))

		value = [
			Bayangan.tinggi,
			Bayangan.jarak,
			Benda.jarak,
			Benda.tinggi,
			Kartesius.fokus,
		]

		# Ambil dalam kotak
		x_text, y_text = 150, height - 30

		# Perulangan gambar teks
		for t, v in zip(teks, value):
			text_obj = UI.render_text(t, fg_color)
			text_rect = text_obj.get_rect(topright=(x_text, y_text))
			SCREEN.blit(text_obj, text_rect)

			val_obj = UI.render_text(str(v), fg_color)
			SCREEN.blit(val_obj, (x_text, y_text))
			y_text -= 25

		# Back
		back.draw()
		text_obj = UI.render_text("Back", bg_color)
		text_rect = text_obj.get_rect(center=back.rect.center)
		SCREEN.blit(text_obj, text_rect)

	@staticmethod
	def cekung():
		pass


teks = [
	f"Tinggi Bayangan = ",
	f"Jarak Bayangan = ",
	f"Jarak Benda = ",
	f"Tinggi Benda = ",
	f"Titik Fokus = ",
]

# Bagian utama
def main():
	global fg_color, bg_color, width, height
	run = True

	fg_color = WHITE
	bg_color = BLACK

	# Event Handler
	while run:
		width = SCREEN.get_width()
		height = SCREEN.get_height()

		# Night mode
		x, y = width - 90, 50
		w, h = 50, 50
		night_mode = Button(x, y, w, h, WHITE)

		# Get Input
		key_pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()

		# Handle night mode
		mouse_pos = pygame.mouse.get_pos()
		if Button.check_collisions(mouse_pos[0], mouse_pos[1], 3, 3, night_mode.x, night_mode.y, night_mode.w, night_mode.h):
			night_mode.color = GRAY
			if mouse_pressed[0]:
				if Button.night_mode:
					night_mode.color = WHITESMOKE
					bg_color = WHITESMOKE
					fg_color = BLACK
					Button.night_mode = False
					pygame.time.wait(250)
				else:
					night_mode.color = BLACK
					bg_color = BLACK
					fg_color = WHITE
					Button.night_mode = True
					pygame.time.wait(250)
		else:
			if Button.night_mode:
				night_mode.color = WHITESMOKE
			else:
				night_mode.color = BLACK

		# Background
		SCREEN.fill(bg_color)

		# Button
		night_mode.draw()
		
		# User Interface
		UI.draw()

		if Menu.pilihan['menu']:
			Menu.menu(mouse_pressed)
		if Menu.pilihan['cembung']:
			Menu.cembung(key_pressed, mouse_pressed)

		# Tampilkan apa yg sudah digambar
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
		clock.tick(FPS)

	pygame.quit()

if __name__ == "__main__":
	main()
