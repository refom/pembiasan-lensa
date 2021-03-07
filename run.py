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

# Mencari Gradien/Slope
def gradien(x1, y1, x2, y2):
	m = (y2 - y1) / (x2 - x1)
	return m

# Mencari Persamaan garis
def persamaan(x1, y1, x2, y2, x):
	m = gradien(x1, y1, x2, y2)
	y = y2 + m * (x - x2)
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
		x = Kartesius.get_x()
		self.lensa = pygame.Rect(x, 0, 1, height) # Rectangle untuk lensa
		self.fokus = 100
	
	def get_fokus(self, inv:bool):
		x = self.fokus
		if inv:
			x = cv_coor("x", x=x)
			return x
		x = invert_coor("x", x=x)
		x = cv_coor("x", x=x)
		return x

	def get_fokus2(self, inv:bool):
		x = self.fokus * 2
		if inv:
			x = cv_coor("x", x=x)
			return x
		x = invert_coor("x", x=x)
		x = cv_coor("x", x=x)
		return x

	def draw(self):
		# Convert coordinates
		x, y = Kartesius.get_xy()

		# Vertikal versi Rectangle
		pygame.draw.rect(SCREEN, fg_color, self.lensa)

		# Draw Line
		# pygame.draw.line(SCREEN, fg_color, (x, 0), (x, height))  # Vertikal
		pygame.draw.line(SCREEN, fg_color, (0, y), (width, y)) # Horizontal

	def draw_fokus(self):
		# Ambil titik Fokus
		x, y = self.get_fokus(False), Kartesius.get_y()

		# F
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("F", x, y)

		# Invers F
		x = self.get_fokus(True)

		# F mirror
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("F", x, y)


		# Ambil titik Fokus 2
		x = self.get_fokus2(False)

		# 2F
		pygame.draw.line(SCREEN, fg_color, (x, y), (x, y - 10))
		self.draw_text("2F", x, y)

		# Invers 2F
		x = self.get_fokus2(True)

		# 2F mirror
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

	@classmethod
	def get_xy(cls):
		return cv_coor("xy", x=cls.x, y=cls.y)


# Benda
class Benda(object):
	def __init__(self):
		# Benda
		self.tinggi = 100
		self.jarak = 150

		# Bayangan
		self.x_shadow = 0
		self.y_shadow = 0

		# 2 titik garis Sinar
		self.pos_sinarA = []
		self.pos_sinarB = []
		self.pos_sinarC = []

		# Warna Sinar
		self.c_sinarA = GREEN
		self.c_sinarB = RED
		self.c_sinarC = BLUE

		# Panjang garis
		self.min_value = 0
		self.max_value = width

	# Ambil kordinat yang sudah di convert
	def get_x(self):
		x = invert_coor("x", x=self.jarak)
		x = cv_coor("x", x=x)
		return x

	def get_y(self):
		y = invert_coor("y", y=self.tinggi)
		y = cv_coor("y", y=y)
		return y

	def get_xy(self):
		x, y = invert_coor("xy", x=self.jarak, y=self.tinggi)
		x, y = cv_coor("xy", x=x, y=y)
		return x, y

	# Gambar gambar :")
	def draw(self):
		ky = Kartesius.get_y()
		x, y = self.get_xy()
		pygame.draw.line(SCREEN, fg_color, (x, ky), (x, y), 3) # Benda

	def draw_sinarA(self, kart):
		# Ambil titik benda
		x, y = self.get_xy()

		# Ambil titik fokus mirror
		fx= kart.get_fokus(True)

		# Ambil titik y kartesius
		y_middle = Kartesius.get_y()

		# Pembuatan line && mengambil xinc dan yinc
		# xinc dan yinc dari titik 0 ke width
		line = (0, y, width, y)
		xinc, yinc = DDA(line[0], line[1], line[2], line[3])
		pygame.draw.line(SCREEN, self.c_sinarA, (x, y), (0, y))

		# Kalau collision dengan lensa
		clipped_line = kart.lensa.clipline(line)
		x_cross, y_cross = clipped_line[0]

		# Penggambaran line
		while x < width and y < height:
			x += xinc
			y += yinc
			gfxdraw.pixel(SCREEN, rf_round(x), rf_round(y), self.c_sinarA)

			# Sinar ketemu lensa
			if x == x_cross and y == y_cross:
				xinc, yinc = DDA(x, y, fx, y_middle)

		self.pos_sinarA = [(x_cross, y_cross), (x, y)]

	def draw_sinarB(self, kart):
		# Invers dan Konversi titik benda
		x, y = self.get_xy()
		
		# Ambil titik fokus asli
		fx = kart.get_fokus(False)

		# Ambil titik y kartesius
		y_middle = Kartesius.get_y()

		# Persamaan garis ke belakang
		x_b, y_b = persamaan(fx, y_middle, x, y, self.min_value)
		pygame.draw.line(SCREEN, self.c_sinarB, (x, y), (x_b, y_b), 1)

		# Persamaan garis ke depan
		x_b, y_b = persamaan(fx, y_middle, x, y, self.max_value)
		# pygame.draw.line(SCREEN, self.c_sinarB, (x, y), (x_b, y_b), 1)

		# Pembuatan line && mengambil xinc dan yinc
		# xinc dan yinc dari titik benda ke persamaan garisnya
		line = (x, y, x_b, y_b)
		xinc, yinc = DDA(line[0], line[1], line[2], line[3])

		# Kalau collision dengan lensa
		clipped_line = kart.lensa.clipline(line)
		x_cross, y_cross = clipped_line[0]

		# Penggambaran line
		while x < width and y < height:
			x += xinc
			y += yinc
			gfxdraw.pixel(SCREEN, rf_round(x), rf_round(y), self.c_sinarB)

			# Sinar ketemu lensa
			if x == x_cross and y == y_cross:
				xinc, yinc = DDA(x, y, width, y_cross)
		
		self.pos_sinarB = [(x_cross, y_cross), (x, y)]

	def draw_sinarC(self, kart):
		# Invers dan Konversi titik benda
		x, y = self.get_xy()

		# Ambil titik y kartesius
		x_middle, y_middle = Kartesius.get_xy()
		
		# Persamaan garis ke belakang
		x_c, y_c = persamaan(x_middle, y_middle, x, y, self.min_value)
		pygame.draw.line(SCREEN, self.c_sinarC, (x, y), (x_c, y_c), 1)

		# Persamaan garis ke depan
		x_c, y_c = persamaan(x_middle, y_middle, x, y, self.max_value)
		pygame.draw.line(SCREEN, self.c_sinarC, (x, y), (x_c, y_c), 1)

		# Pembuatan line && mengambil xinc dan yinc
		# xinc dan yinc dari titik benda ke persamaan garisnya
		# line = (x, y, x_c, y_c)
		# xinc, yinc = DDA(line[0], line[1], line[2], line[3])

		# Penggambaran line
		# while x < width and y < height:
		# 	x += xinc
		# 	y += yinc
		# 	gfxdraw.pixel(SCREEN, rf_round(x), rf_round(y), self.c_sinarC)

	# Handle Bayangan // Intersection of Two Lines
	def handle_bayangan(self):
		sinarA = self.pos_sinarA
		sinarB = self.pos_sinarB

		# Cari gradien dari 2 garis
		m = gradien(sinarA[0][0], sinarA[0][1], sinarA[1][0], sinarA[1][1])
		m1 = gradien(sinarB[0][0], sinarB[0][1], sinarB[1][0], sinarB[1][1])

		# Cari titik potongnya
		x = (sinarB[0][1] - sinarA[0][1]) / (m - m1)
		y = sinarA[0][1] + m * x

		self.x_shadow = x
		self.y_shadow = y

	def draw_bayangan(self):
		ky = Kartesius.get_y()
		x = cv_coor("x", x=self.x_shadow)
		y = self.y_shadow
		pygame.draw.line(SCREEN, WHITE, (x, y), (x, ky), 3)

# Bagian penggambaran screen
def draw_screen(kart, benda):
	# Background
	SCREEN.fill(bg_color)

	# Penggambaran
	kart.draw()
	kart.draw_fokus()
	benda.draw()
	benda.draw_sinarA(kart)
	benda.draw_sinarB(kart)
	benda.draw_sinarC(kart)

	# Gambar bayangan
	benda.handle_bayangan()
	benda.draw_bayangan()

	# Tampilkan apa yg sudah digambar
	pygame.display.flip()

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
