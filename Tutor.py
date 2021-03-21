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

FONT = pygame.font.Font(None, 24)

def draw_text(teks, x, y):
	text = FONT.render(teks, False, WHITE)
	text_pos = text.get_rect(centerx=x, centery=y - 15)
	SCREEN.blit(text, text_pos)

# atur gerakan
def atur_gerakan():
	global jarak_benda, tinggi_benda, fokus, last_pos_mouse, mouse_gerak, benda1

	# Buat ngambil key yang ditekan
	keys = pygame.key.get_pressed()

	# Buat ngambil mouse yang ditekan
	mouse = pygame.mouse.get_pressed()
	mouse_pos = pygame.mouse.get_pos()

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


	if mouse[0] and collision(mouse_pos[0], mouse_pos[1], 3, 3, benda1.x, benda1.y, benda1.w, benda1.h):
		# print("masuk")
		jarak_benda = (mouse_pos[0] - SCREEN.get_width()//2) * -1
		tinggi_benda = (mouse_pos[1] - SCREEN.get_height()//2) * -1
		benda1.x, benda1.y = cv_coor(jarak_benda, tinggi_benda)
		benda1.x -= 10
		benda1.y -= 5
		benda1.h = tinggi_benda

	# if mouse[0]:
	# 	jarak_benda = (mouse_pos[0] - SCREEN.get_width()//2) * -1
	# 	tinggi_benda = (mouse_pos[1] - SCREEN.get_height()//2) * -1

def collision(x1, y1, width1, height1, x2, y2, width2, height2): # mouse, line
	if (x1 + width1) > x2 and (y1 + height1) > y2 and (x1 + width1) < (x2 + width2) and (y1 + height1) < (y2 + height2):
		return True

x_11, y_11 = cv_coor(jarak_benda, tinggi_benda)
benda1 = pygame.Rect(x_11 - 10, y_11 - 20, 20, tinggi_benda)

# Awal
def main():
	run = True

	while run:
		# Gambar Background
		SCREEN.fill(BLACK)

		# Buat bayangan
		try:
			jarak_bayangan = ((fokus * jarak_benda) / (jarak_benda - fokus)) * -1
		except:
			jarak_bayangan = 0
		else:
			try:
				tinggi_bayangan = (jarak_bayangan / jarak_benda) * tinggi_benda
			except:
				tinggi_bayangan = 0

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
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2, y2))


		# Buat titik fokus 1 kiri
		x1, y1 = cv_coor(fokus, 0)
		x2, y2 = cv_coor(fokus, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("F", x2, y2)

		# titik fokus 2 kiri
		x1, y1 = cv_coor(fokus * 2, 0)
		x2, y2 = cv_coor(fokus * 2, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("2F", x2, y2)

		# Buat titik fokus 1 kanan
		x1, y1 = cv_coor(fokus * -1, 0)
		x2, y2 = cv_coor(fokus * -1, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("F", x2, y2)

		# titik fokus 2 kanan
		x1, y1 = cv_coor(fokus * 2 * -1, 0)
		x2, y2 = cv_coor(fokus * 2 * -1, 10)
		pygame.draw.line(SCREEN, WHITE, (x1, y1), (x2,y2))
		draw_text("2F", x2, y2)

		# Box info
		teks = [
			f"Jarak Benda = ",
			f"Tinggi Benda = ",
			f"Titik Fokus = ",
			f"Jarak Bayangan = ",
			f"Tinggi Bayangan = ",
		]
		value = [
			jarak_benda,
			tinggi_benda,
			fokus,
			(int(jarak_bayangan)*-1),
			(int(tinggi_bayangan)*-1),
		]

		x1 = SCREEN.get_width() - 100
		y1 = 10
		for txt, val in zip(teks, value):
			teks_obj = FONT.render(txt, False, WHITE)
			teks_rect = teks_obj.get_rect(topright=(x1, y1))
			SCREEN.blit(teks_obj, teks_rect)

			value_obj = FONT.render(str(val), False, WHITE)
			SCREEN.blit(value_obj, (x1, y1))
			y1 += 20

		# Benda
		# Buat sinar 1 ke tengah
		x1, y1 = cv_coor(jarak_benda, tinggi_benda)
		x2, y2 = cv_coor(0, tinggi_benda)
		pygame.draw.line(SCREEN, BLUE, (x1, y1), (x2,y2))

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


		atur_gerakan()



		# nampilin apa yg sudah di gambar
		pygame.display.flip()

		# event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

if __name__ == "__main__":
	main()
	pygame.quit()
