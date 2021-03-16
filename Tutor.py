import pygame
from pygame import gfxdraw

pygame.init()
# Bikin window
SCREEN = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
# Buat title
pygame.display.set_caption("Pembiasan Cahaya - Lensa Cembung")

# Color
WHITE = (255,255,255)
BLACK = (0,0,0)

RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)

jarak_benda = 180
tinggi_benda = 100
fokus = 100

"""
RUMUS
Jarak Bayangan = (Fokus * Jarak Benda) / (Jarak Benda - Fokus)
Tinggi Bayangan = (Jarak Bayangan / Jarak Benda) * Tinggi Benda
"""

# Konfersi kordinat titik
def cv_coor(x, y):
	# Kuadran ke 2
	x = SCREEN.get_width()//2 + x * -1
	y = SCREEN.get_height()//2 + y * -1
	return x, y

# DDA
"""
	ALGORITMA untuk membuat garis dengan titik
1. titik awal, titik akhir
2. (10, 10), (35, 42)
	panjang_x = x2 - x1 (35 - 10) = 25
	panjang_y = y2 - y1 (42 - 10) = 32
3. step = max(panjang_x, panjang_y) = 32
4. penaikan_x = panjang_x / step = 25/32 = 0.7
	penaikan_y = panjang_y / step = 32/32 = 1
5.	x ,  y
	10, 10
	11  11     10.7
	11  12      11.4
	12 13		12.1

	35  42
"""

def DDA(xy1, xy2, color):
	# Variabel lokal [0, 1] (x, y)
	x = xy1[0]
	y = xy1[1]

	# Ambil Panjangnya kordinat
	dx = xy2[0] - xy1[0]
	dy = xy2[1] - xy1[1]

	# Ambil kordinat ter-panjang
	step = max(abs(dx), abs(dy))

	# Ambil butuh brapa increment untuk x dan y
	xinc = dx/step
	yinc = dy/step

	# Gambar garisnya
	for i in range(step):
		x += xinc
		y += yinc
		gfxdraw.pixel(SCREEN, round(x), round(y), color)

# atur gerakan
def atur_gerakan(keys):
	global jarak_benda, tinggi_benda, fokus
	if keys[pygame.K_RIGHT]:
		jarak_benda -= 1
	if keys[pygame.K_LEFT]:
		jarak_benda += 1
	if keys[pygame.K_UP]:
		tinggi_benda += 1
	if keys[pygame.K_DOWN]:
		tinggi_benda -= 1
	
	if keys[pygame.K_RCTRL]:
		fokus -= 1
	if keys[pygame.K_RALT]:
		fokus += 1


# Awal
def main():

	run = True


	while run:
		# Gambar Background
		SCREEN.fill(BLACK)

		# Buat bayangan
		jarak_bayangan = ((fokus * jarak_benda) / (jarak_benda - fokus)) * -1
		tinggi_bayangan = (jarak_bayangan / jarak_benda) * tinggi_benda

		# Garis x
		x1, y1 = 0, SCREEN.get_height()//2
		x2, y2 = SCREEN.get_width(), SCREEN.get_height()//2
		DDA((x1, y1), (x2, y2), WHITE)

		# Garis y
		x1, y1 = SCREEN.get_width()//2, 0
		x2, y2 = SCREEN.get_width()//2, SCREEN.get_height()
		DDA((x1, y1), (x2,y2), WHITE)

		# Buat benda
		x1, y1 = cv_coor(jarak_benda, 0)
		x2, y2 = cv_coor(jarak_benda, tinggi_benda)
		DDA((x1, y1), (x2,y2), WHITE)

		# Buat titik fokus 1 kiri
		x1, y1 = cv_coor(fokus, 0)
		x2, y2 = cv_coor(fokus, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))

		# titik fokus 2 kiri
		x1, y1 = cv_coor(fokus * 2, 0)
		x2, y2 = cv_coor(fokus * 2, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))

		# Buat titik fokus 1 kanan
		x1, y1 = cv_coor(fokus * -1, 0)
		x2, y2 = cv_coor(fokus * -1, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))

		# titik fokus 2 kanan
		x1, y1 = cv_coor(fokus * 2 * -1, 0)
		x2, y2 = cv_coor(fokus * 2 * -1, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))


		# Benda
		# Buat sinar 1 ke tengah
		x1, y1 = cv_coor(jarak_benda, tinggi_benda)
		x2, y2 = cv_coor(0, tinggi_benda)
		DDA((x1, y1), (x2,y2), BLUE)

		# Buat sinar 1 ke fokus
		x1, y1 = cv_coor(0, tinggi_benda)
		x2, y2 = cv_coor(fokus * -1, 0)
		pygame.draw.line(SCREEN, BLUE, (x1, y1), (x2,y2))

		# Buat sinar 1 ke bayangan
		x1, y1 = cv_coor(fokus * -1, 0)
		x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
		pygame.draw.line(SCREEN, BLUE, (x1, y1), (x2,y2))


		# Buat bayangan
		x1, y1 = cv_coor(jarak_bayangan, 0)
		x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))

		# Buat sinar 2 ke tengah
		x1, y1 = cv_coor(jarak_bayangan, tinggi_bayangan)
		x2, y2 = cv_coor(0, tinggi_bayangan)
		pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2,y2))

		# Buat sinar 2 ke fokus
		x1, y1 = cv_coor(0, tinggi_bayangan)
		x2, y2 = cv_coor(fokus, 0)
		pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2,y2))

		# Buat sinar 2 ke benda
		x1, y1 = cv_coor(fokus, 0)
		x2, y2 = cv_coor(jarak_benda, tinggi_benda)
		pygame.draw.line(SCREEN, GREEN, (x1, y1), (x2,y2))

		# Buat ngambil key yang ditekan
		keys = pygame.key.get_pressed()
		atur_gerakan(keys)



		# nampilin apa yg sudah di gambar
		pygame.display.flip()

		# event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

if __name__ == "__main__":
	main()
	pygame.quit()
