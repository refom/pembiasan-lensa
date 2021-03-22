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
			cls.fokus += 1
		if key_pressed[pygame.K_e]:
			cls.fokus -= 1

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
		
		x = CvCoor.x(cls.fokus * 2)
		DDA((x, y), (x, y - 10)) # 2F
		Kartesius.draw_text("r", x, y)

		if Menu.pilihan["cembung"]:
			x = CvCoor.x(cls.fokus * -1)
			DDA((x, y), (x, y - 10)) # F Mirror
			Kartesius.draw_text("f", x, y)

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
	def draw_cembung(cls):
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
	def draw_cekung(cls):
		# Kordinat Kartesius
		kt_x, kt_y = CvCoor.xy(Kartesius.x, Kartesius.y)

		# Kordinat Fokus
		fokus = CvCoor.x(Kartesius.fokus)

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

		# Sinar A ke garis kartesius
		pygame.draw.line(SCREEN, color_awal, (kt_x, y), (x, y))

		# Sinar A ke fokus
		x_b2, y_b2 = CvCoor.xy(Bayangan.jarak, Bayangan.tinggi * -1)
		pygame.draw.line(SCREEN, color_awal, (kt_x, y), (x_b2, y_b2))

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

		if mouse_pressed[0] and not Button.check_mouse_col() and not InputBox.check_mouse_col():
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
	def draw_cembung(cls):
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

	@classmethod
	def draw_cekung(cls):
		# Kordinat Kartesius
		kt_x, kt_y = CvCoor.xy(Kartesius.x, Kartesius.y)

		# Kordinat Fokus
		fokus = CvCoor.x(Kartesius.fokus)

		# Kordinat Bayangan
		x, y = CvCoor.xy(cls.jarak, cls.tinggi * -1)
		# Gambar Bayangan
		DDA((x, kt_y), (x, y))
		# warna
		color_awal = RED
		color_pantul = DEEPPINK

		# Sinar B ke garis kartesius
		pygame.draw.line(SCREEN, color_pantul, (kt_x, y), (x, y))

		# Sinar B ke fokus
		x_b2, y_b2 = CvCoor.xy(Benda.jarak, Benda.tinggi)
		pygame.draw.line(SCREEN, color_awal, (kt_x, y), (x_b2, y_b2))

class UI:
	size = 22

	@classmethod
	def render_text(cls, teks, color, font=0):
		if not font:
			font = pygame.font.Font(None, cls.size)
		text_obj = font.render(str(teks), False, color)
		return text_obj

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
	all_button = []

	def __init__(self, x, y, w, h, color):
		self.rect = pygame.Rect((x, y), (w, h))
		self.color = color
		self.all_button.append(self)

	def draw(self):
		pygame.draw.rect(SCREEN, self.color, self.rect, 0, 15)

	def check_collisions(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			return True

	@classmethod
	def check_mouse_col(cls):
		if cls.all_button:
			for btn in cls.all_button:
				if btn.check_collisions():
					return True

class InputBox:
	all_input_box = []

	def __init__(self, x, y, w, h, value):
		self.rect = pygame.Rect(x, y, w, h)
		self.value = value
		self.text = str(value)
		self.active = False
		self.change = False
		self.all_input_box.append(self)

	def handle_event(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.rect.collidepoint(event.pos):
					self.active = not self.active
				else:
					self.active = False

			if event.type == pygame.KEYDOWN:
				if self.active:
					if event.key == pygame.K_RETURN:
						try:
							self.value = int(self.text)
						except:
							self.value = 100
						self.active = False
						self.change = True
					elif event.key == pygame.K_BACKSPACE:
						self.text = self.text[:-1]
					else:
						self.text += event.unicode

	def draw(self):
		if self.active:
			text_obj = UI.render_text(str(self.text), GREEN)
		else:
			self.text = str(self.value)
			text_obj = UI.render_text(str(self.text), fg_color)
		SCREEN.blit(text_obj, (self.rect.x + 5, self.rect.y + 5))

	def check_collisions(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			return True

	@classmethod
	def check_mouse_col(cls):
		if cls.all_input_box:
			for box in cls.all_input_box:
				if box.check_collisions():
					return True

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

		# Handle click
		lensa_cembung.rect.x, lensa_cembung.rect.y = SCREEN.get_width()//7, SCREEN.get_height()//2
		cermin_cekung.rect.x, cermin_cekung.rect.y = SCREEN.get_width()//7 + SCREEN.get_width()//3, SCREEN.get_height()//2

		mouse_pos = pygame.mouse.get_pos()
		if lensa_cembung.check_collisions():
			lensa_cembung.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["menu"] = False
				Menu.pilihan["cembung"] = True
		else:
			lensa_cembung.color = fg_color

		if cermin_cekung.check_collisions():
			cermin_cekung.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["menu"] = False
				Menu.pilihan["cekung"] = True
		else:
			cermin_cekung.color = fg_color

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
	def both(key_pressed, mouse_pressed, events):
		# Handle Movement
		Benda.handle_movement(key_pressed, mouse_pressed)
		Kartesius.handle_movement(key_pressed, mouse_pressed)

		input_fokus.handle_event(events)
		input_jarak.handle_event(events)
		input_tinggi.handle_event(events)

		# Fokus
		if input_fokus.change:
			Kartesius.fokus = input_fokus.value
			input_fokus.change = False
		else:
			input_fokus.value = Kartesius.fokus

		# Jarak Benda
		if input_jarak.change:
			Benda.jarak = input_jarak.value
			input_jarak.change = False
		else:
			input_jarak.value = Benda.jarak

		# Tinggi Benda
		if input_tinggi.change:
			Benda.tinggi = input_tinggi.value
			input_tinggi.change = False
		else:
			input_tinggi.value = Benda.tinggi

		# Handle Bayangan
		Bayangan.update()

		# ==== Draw
		# Kartesius
		Kartesius.draw()
		Kartesius.draw_fokus()

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

		teks = [
			f"Tinggi Bayangan = ",
			f"Jarak Bayangan = ",
			f"Tinggi Benda = ",
			f"Jarak Benda = ",
			f"Titik Fokus = ",
		]
		value = [
			Bayangan.tinggi,
			Bayangan.jarak,
			input_tinggi,
			input_jarak,
			input_fokus,
		]

		# Ambil dalam kotak
		x_text, y_text = 150, height - 30

		# Perulangan gambar teks
		for t, v in zip(teks, value):
			text_obj = UI.render_text(t, fg_color)
			text_rect = text_obj.get_rect(topright=(x_text, y_text))
			SCREEN.blit(text_obj, text_rect)

			if type(v) == int:
				val_obj = UI.render_text(str(v), fg_color)
				SCREEN.blit(val_obj, (x_text, y_text))
			else:
				v.rect.x, v.rect.y = x_text, y_text
				v.draw()
			y_text -= 25

		# Back
		back.draw()
		text_obj = UI.render_text("Back", bg_color)
		text_rect = text_obj.get_rect(center=back.rect.center)
		SCREEN.blit(text_obj, text_rect)

	@staticmethod
	def cembung(mouse_pressed):
		mouse_pos = pygame.mouse.get_pos()
		if back.check_collisions():
			back.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["cembung"] = False
				Menu.pilihan["menu"] = True
		else:
			back.color = fg_color

		# Handle Mirror
		Kartesius.handle_mirror()
		Benda.handle_mirror()

		# ===== Draw
		# Benda
		Benda.draw_cembung()

		# Bayangan
		Bayangan.draw_cembung()

	@staticmethod
	def cekung(mouse_pressed):
		mouse_pos = pygame.mouse.get_pos()
		if back.check_collisions():
			back.color = GRAY
			if mouse_pressed[0]:
				Menu.pilihan["cekung"] = False
				Menu.pilihan["menu"] = True
		else:
			back.color = fg_color

		# ===== Draw
		# Benda
		Benda.draw_cekung()

		# Bayangan
		Bayangan.draw_cekung()


# Night mode
x, y = SCREEN.get_width() - 90, 50
w, h = 50, 50
night_mode = Button(x, y, w, h, WHITE)

# Cembung
x, y = SCREEN.get_width()//7, SCREEN.get_height()//2
w, h = 300, 100
lensa_cembung = Button(x, y, w, h, WHITE)
Button.all_button.remove(lensa_cembung)

# Cekung
x, y = SCREEN.get_width()//7 + SCREEN.get_width()//3, SCREEN.get_height()//2
cermin_cekung = Button(x, y, w, h, WHITE)
Button.all_button.remove(cermin_cekung)

# Back button
x, y = 10, 70
w, h = 50, 30
back = Button(x, y, w, h, WHITE)

# fokus
input_fokus = InputBox(0, 0, 100, 24, Kartesius.fokus)
input_jarak = InputBox(0, 0, 100, 24, Benda.jarak)
input_tinggi = InputBox(0, 0, 100, 24, Benda.tinggi)


# Bagian utama
def main():
	global fg_color, bg_color, width, height
	run = True

	fg_color = WHITE
	bg_color = BLACK

	# Event Handler
	while run:
		events = pygame.event.get()

		width = SCREEN.get_width()
		height = SCREEN.get_height()

		night_mode.rect.x = width - 90

		# Get Input
		key_pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()

		# Handle night mode
		mouse_pos = pygame.mouse.get_pos()
		if night_mode.check_collisions():
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
		elif Menu.pilihan['cembung']:
			Menu.cembung(mouse_pressed)
		elif Menu.pilihan['cekung']:
			Menu.cekung(mouse_pressed)

		if Menu.pilihan['cembung'] or Menu.pilihan['cekung']:
			Menu.both(key_pressed, mouse_pressed, events)

		# Tampilkan apa yg sudah digambar
		pygame.display.update()

		for event in events:
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
		clock.tick(FPS)

	pygame.quit()

if __name__ == "__main__":
	main()
