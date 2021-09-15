#  Author: Alex Varano
#  Functions to display a range of facial expressions on an 8x8
#  max7219 LED matrix connected to the SPI  headers on a Rasberry Pi 4B

import time

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

virtual = viewport(device, width=200, height=100)

def neutral_eyes(draw):
	draw.rectangle((0, 0, 2, 2), outline="white", fill="black")
	draw.rectangle((5, 0, 7, 2), outline="white", fill="black")

def neutral_face():
	with canvas(virtual) as draw:
		neutral_eyes(draw)
		draw.line((1, 5, 6, 5), fill="white")
		draw.rectangle((1, 5, 6, 6), outline="white", fill="black")


def happy_face():
	with canvas(virtual) as draw:
		neutral_eyes(draw)
		draw.line((1, 5, 6, 5), fill="white")
		draw.point((2, 6, 3, 7, 4, 7, 5, 6), fill="white")

def sad_face():
	with canvas(virtual) as draw:
		neutral_eyes(draw)
		draw.line((2, 5, 5, 5), fill="white")
		draw.point((1, 6, 1, 7, 6, 6, 6, 7), fill="white")

def surprised_face():
	with canvas(virtual) as draw:
		neutral_eyes(draw)
		draw.ellipse((1, 4, 6, 7), outline="white", fill="black")

def angry_face():
	with canvas(virtual) as draw:
		neutral_eyes(draw)
		draw.ellipse((0, 4, 6, 7), outline="white", fill="black")
		draw.line((2, 5, 2, 6), fill="white")
		draw.line((4, 5, 4, 6), fill="white")

def scared_face():
	with canvas(virtual) as draw:
		neutral_eyes(draw)
		draw.line((2, 5, 5, 5), fill="white")
		draw.point((1, 6, 1, 7, 6, 6, 6, 7), fill="white")
		draw.line((2, 7,  5, 7), fill="white")



def main():
	x = 1
	while x == 1:
		virtual.set_position((0, 0))
		neutral_face()
		input("Neutral Face")
		surprised_face()
		input("Surprised Dace")
		happy_face()
		input("Happy Face")
		sad_face()
		input("Sad Face")
		angry_face()
		input("Angry Face")
		scared_face()
		input("Scared Face")

if __name__ == "__main__":
	main()




