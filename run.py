import pygame
from pygame import gfxdraw

if not pygame.font:
	print("Font gak ada")

pygame.init()
size = width, height = 1000, 640
SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption("Pembiasan Cahaya - Lensa Positif")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.Font(None, 24)

FPS = 60

fg_color = WHITE
bg_color = BLACK


"""
LENSA POSITIF/CEMBUNG
CERMIN CEKUNG

- [x] JARAK BENDA
- [x] TITIK FOKUS
- [x] UKURAN BENDA
- JARAK BAYANGAN
- UKURAN BAYANGAN

"""


# Pembulatan
def rf_round(num):
	num = "%.1f" % num
	if num[-1] >= "5":
		return int(num[:-2]) + 1
	return int(num[:-2])

# Algorithm DDA // Mengembalikan xinc dan yinc
def DDA(x1, y1, x2, y2):
	# Variabel lokal
	x = x1
	y = y1

	# Ambil Panjangnya kordinat
	dx = x2 - x1
	dy = y2 - y1

	# Ambil jarak terjauh dari nilai absolut dx atau dy
	step = max(abs(dx), abs(dy))

	# Ambil butuh brapa increment untuk x dan y
	xinc = dx/step
	yinc = dy/step

	# Gambar garisnya
	# for i in range(step):
	# 	x += xinc
	# 	y += yinc
	# 	gfxdraw.pixel(SCREEN, rf_round(x), rf_round(y), WHITE)
	# pygame.display.flip()

	# Kembalikan xinc dan yinc
	return xinc, yinc

# Mencari Persamaan garis
def persamaan(x1, y1, x2, y2, m):
	gradien = (y2 - y1) / (x2 - x1)
	x = m
	y = y2 + gradien * (x - x2)
	return x, y

# Convert Kordinat
def cv_coor(what:str, **coor):
	if what == "x":
		return coor["x"] + (width // 2)
	elif what == "y":
		return coor["y"] + (height // 2)
	elif what == "xy":
		x = coor["x"] + (width // 2)
		y = coor["y"] + (height // 2)
		return (x, y)

# Invert koordinat
def invert_coor(what:str, **coor):
	if what == "x":
		return coor["x"] * -1
	elif what == "y":
		return coor["y"] * -1
	elif what == "xy":
		x = coor["x"] * -1
		y = coor["y"] * -1
		return (x, y)

# Kartesius system
class Kartesius(object):
	x = 0
	y = 0
	def __init__(self):
		x, y = cv_coor("xy", x=self.x, y=self.y)
		self.lensa = pygame.Rect(x, 0, 1, height) # Rectangle untuk lensa

		self.fokus = 100
	
	def get_fokus2(self):
		return self.fokus * 2

	def draw(self):
		# Convert coordinates
		x, y = cv_coor("xy", x=self.x, y=self.y)

		# Vertikal versi Rectangle
		pygame.draw.rect(SCREEN, fg_color, self.lensa)

		# Draw Line
		# pygame.draw.line(SCREEN, fg_color, (x, 0), (x, height))  # Vertikal
		pygame.draw.line(SCREEN, fg_color, (0, y), (width, y)) # Horizontal

	def draw_fokus(self):
		# Konvert F
		x, y = cv_coor("xy", x=self.fokus, y=self.y)

		# F mirror
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("F", x, y)

		# Invers F
		x = invert_coor("x", x=self.fokus)
		x = cv_coor("x", x=x)

		# F
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("F", x, y)


		# Konvert 2F
		x = cv_coor("x", x=self.get_fokus2())

		# 2F mirror
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("2F", x, y)

		# Invers 2F
		x = invert_coor("x", x=self.get_fokus2())
		x = cv_coor("x", x=x)

		# 2F
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("2F", x, y)

	def draw_text(self, teks, x, y):
		text = FONT.render(teks, 1, fg_color)
		textpos = text.get_rect(centerx=x, centery=y - 20)
		SCREEN.blit(text, textpos)


	@classmethod
	def get_x(cls):
		return cv_coor("x", x=cls.x)

	@classmethod
	def get_y(cls):
		return cv_coor("y", y=cls.y)


# Benda
class Benda(object):
	def __init__(self):
		self.tinggi = 100
		self.jarak = 150
		self.c_sinar1 = GREEN
		self.c_sinar2 = RED
		self.c_sinar3 = BLUE

	def draw(self):
		ky = Kartesius.get_y()
		x, y = invert_coor("xy", x=self.jarak, y=self.tinggi)
		x, y = cv_coor("xy", x=x, y=y)
		pygame.draw.line(SCREEN, fg_color, (x, ky), (x, y), 3) # Benda

	def draw_sinar(self, kart):
		# Invers dan Konversi titik benda
		x, y = invert_coor("xy", x=self.jarak, y=self.tinggi)
		x, y = cv_coor("xy", x=x, y=y)

		# Ambil titik fokus asli dan mirror
		fx1= cv_coor("x", x=kart.fokus) # Mirror
		fx2 = invert_coor("x", x=kart.fokus)
		fx2 = cv_coor("x", x=fx2) # Asli

		# Ambil titik tengah
		x_middle, y_middle = cv_coor("xy", x=kart.x, y=kart.y)

		# minimum value
		min_value = 0
		max_value = width

		######## --- SINAR A
		# Pembuatan line && mengambil xinc dan yinc
		# xinc dan yinc dari titik 0 ke width
		line = (0, y, width, y)
		xinc, yinc = DDA(line[0], line[1], line[2], line[3])
		pygame.draw.line(SCREEN, self.c_sinar1, (x, y), (0, y))

		# Kalau collision dengan lensa
		clipped_line = kart.lensa.clipline(line)
		x_cross, y_cross = clipped_line[0]

		# Penggambaran line
		x_a, y_a = x, y
		while x_a < width and y_a < height:
			x_a += xinc
			y_a += yinc
			gfxdraw.pixel(SCREEN, rf_round(x_a), rf_round(y_a), self.c_sinar1)

			# Sinar ketemu lensa
			if x_a == x_cross and y_a == y_cross:
				xinc, yinc = DDA(x_a, y_a, fx1, y_middle)


		######## --- SINAR B
		# Persamaan garis ke belakang
		x_b, y_b = persamaan(fx2, y_middle, x, y, min_value)
		pygame.draw.line(SCREEN, self.c_sinar2, (x, y), (x_b, y_b), 1)

		# Persamaan garis ke depan
		x_b, y_b = persamaan(fx2, y_middle, x, y, max_value)
		# pygame.draw.line(SCREEN, self.c_sinar2, (x, y), (x_b, y_b), 1)

		# Pembuatan line && mengambil xinc dan yinc
		# xinc dan yinc dari titik benda ke persamaan garisnya
		line2 = (x, y, x_b, y_b)
		xinc, yinc = DDA(line2[0], line2[1], line2[2], line2[3])

		# Kalau collision dengan lensa
		clipped_line = kart.lensa.clipline(line2)
		x_cross, y_cross = clipped_line[0]

		# Penggambaran line
		x_b, y_b = x, y
		while x_b < width and y_b < height:
			x_b += xinc
			y_b += yinc
			gfxdraw.pixel(SCREEN, rf_round(x_b), rf_round(y_b), self.c_sinar2)

			# Sinar ketemu lensa
			if x_b == x_cross and y_b == y_cross:
				xinc, yinc = DDA(x_cross, y_cross, width, y_cross)


		######## --- SINAR C
		# Persamaan garis ke belakang
		x_c, y_c = persamaan(x_middle, y_middle, x, y, min_value)
		pygame.draw.line(SCREEN, self.c_sinar3, (x, y), (x_c, y_c), 1)

		# Persamaan garis ke depan
		x_c, y_c = persamaan(x_middle, y_middle, x, y, max_value)
		# pygame.draw.line(SCREEN, self.c_sinar3, (x, y), (x_c, y_c), 1)

		# Pembuatan line && mengambil xinc dan yinc
		# xinc dan yinc dari titik benda ke persamaan garisnya
		line3 = (x, y, x_c, y_c)
		xinc, yinc = DDA(line3[0], line3[1], line3[2], line3[3])

		# Kalau collision dengan lensa
		clipped_line = kart.lensa.clipline(line3)
		x_cross, y_cross = clipped_line[0]

		# Penggambaran line
		x_c, y_c = x, y
		while x_c < width and y_c < height:
			x_c += xinc
			y_c += yinc
			gfxdraw.pixel(SCREEN, rf_round(x_c), rf_round(y_c), self.c_sinar3)

		pygame.display.flip()


# Bagian penggambaran screen
def draw_screen(kart, benda):
	# Background
	SCREEN.fill(bg_color)

	# Anything
	kart.draw()
	kart.draw_fokus()
	benda.draw()
	benda.draw_sinar(kart)

	# Update
	pygame.display.update()


# Bagian utama
def main():

	clock = pygame.time.Clock()
	run = True
	
	kart = Kartesius()
	benda = Benda()

	# Event Handler
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
		draw_screen(kart, benda)
	
	pygame.quit()


if __name__ == "__main__":
	main()
