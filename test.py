import pygame
from pygame import gfxdraw

if not pygame.font:
	print("Font gak ada")

pygame.init()
SCREEN = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
pygame.display.set_caption("Pembiasan Cahaya - Lensa Positif/Cembung")

FPS = 60

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
	@staticmethod
	def x(x):
		return (SCREEN.get_width()//2) + x

	@staticmethod
	def y(y):
		return (SCREEN.get_height()//2) + y

	@staticmethod
	def xy(x, y):
		return CvCoor.x(x), CvCoor.y(y)

class Kartesius:
	x = 0
	y = 0
	fokus = 100

	@classmethod
	def handle_movement(cls, key_pressed, mouse_pressed):
		if key_pressed[pygame.K_q]:
			cls.fokus += 1
		if key_pressed[pygame.K_e]:
			cls.fokus -= 1
		
		if mouse_pressed[2]:
			mouse_pos = pygame.mouse.get_pos()
			cls.fokus = (mouse_pos[0] - width//2) * -1

	@classmethod
	def draw(cls):
		x, y = CvCoor.xy(cls.x, cls.y)
		DDA((0, y), (width, y)) # x
		DDA((x, 0), (x, height)) # y

	@classmethod
	def draw_fokus(cls):
		x, y = CvCoor.x(cls.fokus * -1), CvCoor.y(cls.y)
		DDA((x, y), (x, y - 10)) # F
		Kartesius.draw_text("F", x, y)
		
		x = CvCoor.x(cls.fokus)
		DDA((x, y), (x, y - 10)) # F Mirror
		Kartesius.draw_text("F", x, y)

		x = CvCoor.x(cls.fokus * 2 * -1)
		DDA((x, y), (x, y - 10)) # 2F
		Kartesius.draw_text("2F", x, y)

		x = CvCoor.x(cls.fokus * 2)
		DDA((x, y), (x, y - 10)) # 2F Mirror
		Kartesius.draw_text("2F", x, y)

	@staticmethod
	def draw_text(teks, x, y):
		font = pygame.font.Font(None, 24)
		text = font.render(teks, 1, fg_color)
		textpos = text.get_rect(centerx=x, centery=y - 20)
		SCREEN.blit(text, textpos)

class Benda:
	jarak = 200
	tinggi = 100

	@classmethod
	def draw(cls):
		# Kordinat Kartesius
		kt_x, kt_y = CvCoor.xy(Kartesius.x, Kartesius.y)
		# Kordinat Fokus
		fokus = CvCoor.x(Kartesius.fokus)
		# Kordinat Benda
		x, y = CvCoor.xy(cls.jarak * -1, cls.tinggi * -1)
		# Gambar Benda
		DDA((x, kt_y), (x, y))

		"""
			Algoritma Sinar A
		1. gambar garis dari titik x kartesius ke 0 (garis kebelakang)
		2. gambar garis dari titik x kartesius ke titik fokus seberang
		3. jika garis lebih dari titik x kartesius, balik gambarnya
		"""
		if x >= kt_x:
			x_new, y_new = persamaan((kt_x, y), (0, y), width)
		else:
			x_new, y_new = persamaan((kt_x, y), (0, y), 0)
		
		if Button.night_mode:
			pygame.draw.line(SCREEN, GREEN, (kt_x, y), (x_new, y_new)) # 1
		else:
			pygame.draw.line(SCREEN, DARK_GREEN, (kt_x, y), (x_new, y_new)) # 1

		x_new, y_new = persamaan((kt_x, y), (fokus, kt_y), width) # 2
		if Button.night_mode:
			pygame.draw.line(SCREEN, GREENYELLOW, (kt_x, y), (x_new, y_new))
		else:
			pygame.draw.line(SCREEN, GREEN2, (kt_x, y), (x_new, y_new))
		# Sinar C
		x_new, y_new = persamaan((kt_x, kt_y), (x, y), 0)
		pygame.draw.line(SCREEN, BLUE, (kt_x, kt_y), (x_new, y_new))

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
		kt_x, kt_y = CvCoor.xy(Kartesius.x, Kartesius.y)
		fokus = CvCoor.x(Kartesius.fokus * -1)
		x, y = CvCoor.xy(cls.jarak, cls.tinggi)
		DDA((x, kt_y), (x, y)) # Bayangan

		# Sinar B
		if x <= kt_x:
			x_new, y_new = persamaan((kt_x, y), (0, y), 0)
		else:
			x_new, y_new = persamaan((kt_x, y), (0, y), width)
		pygame.draw.line(SCREEN, DEEPPINK, (kt_x, y), (x_new, y_new)) # 1

		x_new, y_new = persamaan((kt_x, y), (fokus, kt_y), 0) # 2
		pygame.draw.line(SCREEN, RED, (kt_x, y), (x_new, y_new))

		# Sinar C
		x_new, y_new = persamaan((kt_x, kt_y), (x, y), width)
		pygame.draw.line(SCREEN, DEEPSKYBLUE, (kt_x, kt_y), (x_new, y_new))

class UI:
	size = 22

	@classmethod
	def render_text(cls, teks, color, font=0):
		if not font:
			font = pygame.font.Font(None, cls.size)
		text_obj = font.render(str(teks), True, color)
		return text_obj

	@classmethod
	def display_text(cls, text_obj, xy):
		SCREEN.blit(text_obj, (xy[0], xy[1]))

	@classmethod
	def draw(cls, clock):
		# Gambar info
		w, h = 370, 70
		base = pygame.Surface((w, h), pygame.SRCALPHA)
		pygame.draw.rect(base, DARK_GRAY, base.get_rect(), 0, 15)
		SCREEN.blit(base, (-10, -10))

		text_obj = cls.render_text("W A S D / Left Click : Menggerakkan Benda", fg_color)
		cls.display_text(text_obj, (10, 10))
		text_obj = cls.render_text("Q E / Right Click : Menggerakkan Titik Fokus", fg_color)
		cls.display_text(text_obj, (10, 30))

		# Gambar teks
		w, h = 220, 170
		base = pygame.Surface((w, h), pygame.SRCALPHA)
		pygame.draw.rect(base, DARK_GRAY2, base.get_rect(), 0, 15)
		SCREEN.blit(base, (-20, height - base.get_height() + 20))
		
		teks = [
			f"Tinggi Bayangan = {Bayangan.tinggi}",
			f"Jarak Bayangan = {Bayangan.jarak}",
			f"Jarak Benda = {Benda.jarak}",
			f"Tinggi Benda = {Benda.tinggi}",
			f"Titik Fokus = {Kartesius.fokus}",
		]

		# Ambil dalam kotak
		x_text, y_text = 15, height - 30

		# Perulangan gambar teks
		for t in teks:
			text_obj = cls.render_text(t, fg_color)
			cls.display_text(text_obj, (x_text, y_text))
			y_text -= 25

		# Ping
		ping = clock.tick(FPS)
		color = GREEN
		if ping > 100:
			color = RED
		text_obj = cls.render_text(f"PING = {ping}", color)
		cls.display_text(text_obj, (width - 100, 20))

		# Night mode
		font = pygame.font.Font(None, 48)
		text_obj = cls.render_text("N", bg_color, font)
		cls.display_text(text_obj, (width - 75, 60))

class Button:
	night_mode = True
	nm_color = WHITE

	@classmethod
	def draw(cls):
		# Night mode
		x, y = width - 90, 50
		w, h = 50, 50
		rect = pygame.Rect((x, y), (w, h))
		pygame.draw.rect(SCREEN, cls.nm_color, rect, 0, 15)

	@staticmethod
	def check_collisions(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
		return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)

	@classmethod
	def handle(cls, mouse_pressed):
		global bg_color, fg_color
		mouse_pos = pygame.mouse.get_pos()
		# Night mode click
		if cls.check_collisions(mouse_pos[0], mouse_pos[1], 3, 3, width - 90, 50, 50, 50):
			cls.nm_color = GRAY
			if mouse_pressed[0]:
				if cls.night_mode:
					cls.nm_color = WHITESMOKE
					bg_color = WHITESMOKE
					fg_color = BLACK
					cls.night_mode = False
					pygame.time.wait(250)
				else:
					cls.nm_color = BLACK
					bg_color = BLACK
					fg_color = WHITE
					cls.night_mode = True
					pygame.time.wait(250)
		else:
			if cls.night_mode:
				cls.nm_color = WHITESMOKE
			else:
				cls.nm_color = BLACK

# Bagian penggambaran screen
def draw_screen(clock):
	# Background
	SCREEN.fill(bg_color)

	# Kartesius
	Kartesius.draw()
	Kartesius.draw_fokus()

	# Benda
	Benda.draw()

	# Bayangan
	Bayangan.draw()

	# Button
	Button.draw()

	# User Interface
	UI.draw(clock)

# Bagian utama
def main():
	global fg_color, bg_color, width, height
	clock = pygame.time.Clock()
	run = True

	fg_color = WHITE
	bg_color = BLACK

	# Event Handler
	while run:
		width = SCREEN.get_width()
		height = SCREEN.get_height()

		# Get Input
		key_pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()

		# Handle Movement
		Benda.handle_movement(key_pressed, mouse_pressed)
		Kartesius.handle_movement(key_pressed, mouse_pressed)

		# Handle click
		Button.handle(mouse_pressed)

		# Handle Bayangan
		Bayangan.update()

		# Draw screen
		draw_screen(clock)

		# Tampilkan apa yg sudah digambar
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

if __name__ == "__main__":
	main()
	pygame.quit()
