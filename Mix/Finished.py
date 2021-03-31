import pygame

from utility import CvCoor
from utama import *

pygame.init()
pygame.display.set_caption("Pembiasan Cahaya")
SCREEN = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 120



x, y = SCREEN.get_width()//2, SCREEN.get_height() + SCREEN.get_height()//4
font_judul = pygame.font.Font(None, 100)
font_h2 = pygame.font.Font(None, 80)
font_h3 = pygame.font.Font(None, 70)
font_nama = pygame.font.Font(None, 50)
font_space1 = 80
font_space2 = 60
font_space_jump = 400
font_space_jump_high = 650
credits_list = [
	[[x, y], "GRAFIKA KOMPUTER - B", font_judul, font_space1],
	[[x, y], "Projek 1 - Pembiasan Cahaya", font_h2, font_space2],
	[[x, y], " ", font_h2, font_space_jump],
	[[x, y], " =  Brought by Group 8  = ", font_h3, font_space1],
	[[x, y], " ", font_h2, font_space_jump],
	[[x, y], "-- Our Group Member's --", font_h3, font_space1],
	[[x, y], "Alyusufi Bima Rizki Utama - 11191008", font_nama, font_space2],
	[[x, y], "Muhammad Rafliadi - 11191052", font_nama, font_space2],
	[[x, y], "Rani Meliyana Putri - 11191062", font_nama, font_space2],
	[[x, y], "Yashmine Hapsari - 11181083", font_nama, font_space2],
	[[x, y], " ", font_h2, font_space_jump_high],
	[[x, y], "Made with love <3", font_nama, 50],
	[[x, y], "   - Reforms     ", font_nama, font_space2],
	[[x, y], " ", font_h2, font_space_jump_high],
]

for crd in credits_list:
	crd[0][1] = y
	y += crd[3]

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

# Credits
x, y = SCREEN.get_width() - 110, SCREEN.get_height() - 50
w, h = 100, 40
credits_btn = Button(x, y, w, h, WHITE)
Button.all_button.remove(credits_btn)

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
		CvCoor.update(width, height)


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
		night_mode.rect.x = width - 90
		night_mode.draw()
		
		# User Interface
		UI.draw()

		if Menu.pilihan['menu']:
			Menu.menu(mouse_pressed)
		elif Menu.pilihan['cembung']:
			Menu.cembung(mouse_pressed)
		elif Menu.pilihan['cekung']:
			Menu.cekung(mouse_pressed)
		elif Menu.pilihan['credits']:
			Menu.credits(mouse_pressed)

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
