import pygame, time, os, random

from pygame.math import Vector2
from utility import COLORS, FontText, Button, CvCoor, InputBox, Tema
from comp import Kartesius, Benda, Bayangan
from particle import Particle

class Window:
	def __init__(self, screen_size):
		pygame.init()
		self.size = screen_size

		# Display Screen
		pygame.display.set_caption("Pembiasan Cahaya")
		self.surface = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

		# clock
		self.clock = pygame.time.Clock()
		self.FPS = 120

	def update(self):
		self.size = (self.surface.get_width(), self.surface.get_height())
		CvCoor.update(self.size)

		self.clock.tick(self.FPS)

		if Tema.curr_bg:
			bg = pygame.transform.scale(Tema.curr_bg, self.surface.get_size())
			self.surface.blit(bg, (0,0))
		else:
			self.surface.fill(COLORS.bg_color)
		
		Menu.render_all()

	def set_caption(self, title):
		pygame.display.set_caption(title)

	def blit(self, surface, pos):
		self.surface.blit(surface, pos)

def main():
	global menu, window, night_mode, partikel, box_info
	global jarak_box, tinggi_box, fokus_box, back

	menu = Menu()
	window = Window((1000, 640))

	# Default Benda
	Tema.add_chr(os.path.join(os.getcwd(), "data", "img", "cactus.png"))
	Tema.set_default()

	# Tema 1
	Tema.add_bg(os.path.join(os.getcwd(), "data", "img", "desert.png"))
	Tema.add_chr(os.path.join(os.getcwd(), "data", "img", "cactus.png"))
	Tema.set_theme([1, 1])

	# Tema 2
	Tema.add_bg(os.path.join(os.getcwd(), "data", "img", "planet.jpeg"))
	Tema.add_chr(os.path.join(os.getcwd(), "data", "img", "rocket.png"))
	Tema.set_theme([2, 2])

	# Tema 3
	Tema.add_bg(os.path.join(os.getcwd(), "data", "img", "night_moon.jpeg"))
	Tema.set_theme([3, 2])

	# Font
	FontText.title = os.path.join(os.getcwd(), "data", "font", "title.otf")
	FontText.normal = os.path.join(os.getcwd(), "data", "font", "normal.ttf")
	FontText.update()

	# Night Mode Button
	night_mode = Button((0,0), (50, 50), "N", statik=True, font=FontText.font_normal)
	night_mode.on = True

	# Back Button
	back = Button((0,0), (70, 35), "back", statik=True, font=FontText.font_normal)

	# Particle
	partikel = Particle()

	# Box info
	box_info = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "box_info.png"))

	# Input Box
	jarak_box = InputBox((0, 0), (50, 24), Benda.jarak, Benda.set_jarak, Benda.get_jarak)
	tinggi_box = InputBox((0, 0), (50, 24), Benda.tinggi, Benda.set_tinggi, Benda.get_tinggi)
	fokus_box = InputBox((0, 0), (50, 24), Kartesius.fokus, Kartesius.set_fokus, Kartesius.get_fokus)

	while menu.run:
		
		if menu.menu:
			window.set_caption("Pembiasan Cahaya")
			menu.render_menu()
		elif menu.cembung:
			window.set_caption("Cermin Cembung")
			menu.render_cembung()
		elif menu.cekung:
			window.set_caption("Cermin Cekung")
			menu.render_cekung()
		elif menu.credits:
			window.set_caption("Credits")
			menu.render_credits()

	pygame.quit()

class Menu:
	def __init__(self):
		self.menu = True
		self.cembung = False
		self.cekung = False
		self.credits = False
		self.run = True

	@staticmethod
	def render_all():
		# Fps
		x, y = window.size[0] - 50, 30
		fps = int(window.clock.get_fps())
		color = COLORS.green_shade
		if fps < 35:
			color = COLORS.red
		text = FontText.font_22.render(f"FPS = {fps}", True, color)
		window.blit(text, text.get_rect(center=(x, y)))

		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()

		# Night Mode
		if night_mode.check_collisions(mouse_pos) and mouse_pressed[0]:
			night_mode.on = not night_mode.on
			pygame.time.delay(250)

		if night_mode.on:
			COLORS.fg_color = COLORS.white
			COLORS.bg_color = COLORS.black
		else:
			COLORS.fg_color = COLORS.black
			COLORS.bg_color = COLORS.whitesmoke

		night_mode.pos.xy = (window.size[0] - 50, 75)
		night_mode.render(window.surface, mouse_pos)

		# Particle
		partikel.handle_click(mouse_pressed)
		partikel.emit(window.surface)

	def render_menu(self):
		# Button
		wh = (300, 80)
		btn_cembung = Button((0,0), wh, "Lensa Cembung")
		btn_cekung = Button((0,0), wh, "Cermin Cekung")
		btn_credits = Button((0,0), wh, "Credits")

		title_white = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "title_white.png"))
		title_black = pygame.image.load(os.path.join(os.getcwd(), "data", "img", "title_black.png"))

		btn_theme = Button((0,0), (150, 50), "Change Theme", font=FontText.font_semi_normal, shade=False)

		while self.menu:
			events = pygame.event.get()
			mouse_pos = pygame.mouse.get_pos()

			for event in events:
				if event.type == pygame.QUIT:
					self.menu = False
					self.run = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.menu = False
						self.run = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if btn_cembung.check_collisions(event.pos):
						self.menu = False
						self.cembung = True
						pygame.time.delay(250)
					if btn_cekung.check_collisions(event.pos):
						self.menu = False
						self.cekung = True
						pygame.time.delay(250)
					if btn_credits.check_collisions(event.pos):
						self.menu = False
						self.credits = True
					if btn_theme.check_collisions(event.pos):
						Tema.change_theme()

			window.update()

			# Judul
			x, y = window.size[0]//2, window.size[1]//2 - window.size[1]//4
			# FontText.render(window, FontText.font_title, (x + 4, y + 4), "Pembiasan Cahaya", True, COLORS.gray)
			# FontText.render(window, FontText.font_title, (x, y), "Pembiasan Cahaya", True, COLORS.fg_color)
			img = title_black
			if night_mode.on:
				img = title_white
			img = pygame.transform.scale(img, [600, 400])
			img_rect = img.get_rect(center=(x,y))
			window.blit(img, img_rect)

			# Button
			x, y = window.size[0]//2, window.size[1]//3 + 100
			for btn in range(3):
				Button.all_buttons[btn].pos.xy = (x, y)
				Button.all_buttons[btn].render(window.surface, mouse_pos)
				y += 100

			# Background Button
			x, y = 100, window.size[1] - 40
			btn_theme.pos.xy = (x, y)
			btn_theme.render(window.surface, mouse_pos)

			pygame.display.flip()
		
		Button.clear_all()

	def render_cembung(self):
		while self.cembung:
			events = pygame.event.get()

			for event in events:
				if event.type == pygame.QUIT:
					self.cembung = False
					self.run = False
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.menu = True
						self.cembung = False
						return
				if event.type == pygame.MOUSEBUTTONDOWN:
					if back.check_collisions(event.pos):
						self.menu = True
						self.cembung = False
						return

			window.update()

			self.render_sama(events)

			Benda.render_cembung(window.surface)
			Bayangan.render_cembung(window.surface)

			pygame.display.flip()

	def render_cekung(self):
		while self.cekung:
			events = pygame.event.get()

			for event in events:
				if event.type == pygame.QUIT:
					self.cekung = False
					self.run = False
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.menu = True
						self.cekung = False
						return
				if event.type == pygame.MOUSEBUTTONDOWN:
					if back.check_collisions(event.pos):
						self.menu = True
						self.cekung = False
						return

			window.update()

			self.render_sama(events)

			Benda.render_cekung(window.surface)
			Bayangan.render_cekung(window.surface)

			pygame.display.flip()

	def render_credits(self):
		x, y = window.size[0]//2, window.size[1] + window.size[1]//4
		font_space1 = 100
		font_space2 = 80
		font_space_jump_high = 650
		# [0] = (x, y) | [1] = text | [2] = font | [3] = font space
		credits_list = [
			[[x, y], "GRAFIKA KOMPUTER - B", FontText.font_title, font_space1],
			[[x, y], "Projek 1 - Pembiasan Cahaya", FontText.font_h1, font_space2],
			[[x, y], " ", FontText.font_h2, font_space_jump_high],
			[[x, y], " =  Brought by Group 8  = ", FontText.font_h2, font_space2],
			[[x, y], " ", FontText.font_h2, font_space_jump_high],
			[[x, y], "-- Our Group Member's --", FontText.font_h2, font_space2],
			[[x, y], "Alyusufi Bima Rizki Utama - 11191008", FontText.font_h3, font_space2],
			[[x, y], "Muhammad Rafliadi - 11191052", FontText.font_h3, font_space2],
			[[x, y], "Rani Meliyana Putri - 11191062", FontText.font_h3, font_space2],
			[[x, y], "Yashmine Hapsari - 11181083", FontText.font_h3, font_space2],
			[[x, y], " ", FontText.font_h2, font_space_jump_high],
			[[x, y], "Made with love <3", FontText.font_normal, 50],
			[[x, y], "   - Reforms     ", FontText.font_normal, font_space2],
			[[x, y], " ", FontText.font_h2, font_space_jump_high],
		]

		for crd in credits_list:
			crd[0][1] = y
			y += crd[3]

		speed_up = False

		while self.credits:
			events = pygame.event.get()

			for event in events:
				if event.type == pygame.QUIT:
					self.credits = False
					self.run = False
					return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.menu = True
						self.credits = False
						return
					if event.key == pygame.K_SPACE:
						speed_up = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						speed_up = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					if back.check_collisions(event.pos):
						self.menu = True
						self.credits = False
						return

			window.update()

			# Roket Congrats
			x, y = 50, window.size[1]//2 + 50
			direction = [random.randint(0, 50) / 10 - 2.5, random.randint(0, 50) / 10 - 4]
			partikel.add_particle(xy=[x, y], rad=[3, 8], direct=direction)

			x, y = window.size[0] - 50, window.size[1]//2 + 50
			direction = [random.randint(0, 50) / 10 - 2.5, random.randint(0, 50) / 10 - 4]
			partikel.add_particle(xy=[x, y], rad=[3, 8], direct=direction)

			if speed_up:
				speed = 3
			else:
				speed = 0.7

			# Roll And Show Credits
			for crd in credits_list:
				text = crd[2].render(crd[1], True, COLORS.fg_color)
				window.surface.blit(text, text.get_rect(center=crd[0]))
				crd[0][0] = window.size[0]//2
				crd[0][1] -= speed
				if crd[0][1] < 0:
					crd[0][1] = credits_list[-1][0][1] + credits_list[-1][3]
					item = credits_list.pop(0)
					credits_list.append(item)

			# Back
			back.pos.xy = 50, 30
			back.render(window.surface, pygame.mouse.get_pos())

			pygame.display.flip()

	@staticmethod
	def render_sama(events):
		mouse_pos = pygame.mouse.get_pos()
		mouse_pressed = pygame.mouse.get_pressed()
		key_pressed = pygame.key.get_pressed()

		Kartesius.handle_movement(key_pressed, mouse_pressed, mouse_pos)
		Kartesius.handle_mirror()
		
		Benda.handle_movement(key_pressed, mouse_pressed, mouse_pos)
		Benda.handle_mirror()

		Bayangan.update()
		Bayangan.handle_mirror(menu)

		Kartesius.render(window.surface, menu)

		if night_mode.on:
			Benda.color_awal = COLORS.green
			Benda.color_pantul = COLORS.greenyellow
		else:
			Benda.color_awal = COLORS.dark_green
			Benda.color_pantul = COLORS.green2

		InputBox.handle_event(events)

		InputBox.update_box()

		# Box info 1
		x, y = 20, window.size[1] - 20
		box_copy = pygame.transform.scale(box_info, (270, 170))
		rect = box_copy.get_rect(bottomleft=(x,y))
		window.blit(box_copy, rect)

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
			tinggi_box,
			jarak_box,
			fokus_box,
		]

		x, y = 220, window.size[1] - 70
		color = COLORS.black
		for t, v in zip(teks, value):
			text = FontText.font_normal.render(t, True, color)
			window.blit(text, text.get_rect(topright=(x,y)))

			if type(v) == int:
				text = FontText.font_normal.render(str(v), True, color)
				window.blit(text, (x, y))
			else:
				v.rect.x, v.rect.y = x, y
				v.render(window.surface)

			y -= 24

		# Box info 2
		x, y = 10, 10
		box_copy = pygame.transform.scale(box_info, (350, 60))
		window.blit(box_copy, (x, y))

		x, y = x + 30, y + 10
		text = FontText.font_small.render("W A S D / Left Click : Menggerakkan Benda", True, color)
		window.blit(text, (x, y))
		text = FontText.font_small.render("Q E / Right Click : Menggerakkan Titik Fokus", True, color)
		window.blit(text, (x, y + 20))

		# Back
		back.pos.xy = 70, 100
		back.render(window.surface, mouse_pos)


if __name__ == "__main__":
	main()

