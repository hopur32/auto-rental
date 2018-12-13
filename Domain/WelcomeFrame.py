import sys
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Effect, BannerText

def demo(screen):
    scenes = []

    logo='''
         ░░░░░░░░░░░░░░░░░░░
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
       ▒▒▒▒    ╱ o o ╲    ▒▒▒▒
   ▓▓▓ ▒▒▒▒    ╲_╰─╯_╱    ▒▒▒▒ ▓▓▓
      ╲▒▒▒▒     ╱   ╲     ▒▒▒▒╱
       ░░░░░░░░░░░░░░░░░░░░░░░
       ▓▓╳╳▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╳╳▓▓
       ▓▓▓▓▓═╣╠═╣╠═╣╠═╣╠═▓▓▓▓▓
       ▓▓▓▓╠═╣╠═╣╠═╣╠═╣╠═╣▓▓▓▓
       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
          ╿___╿       ╿___╿'''

    Welcome='Welcome to this program\npress enter to continue'

    effects = [
        BannerText(screen,       #Nafn myndar, hæð myndar, background litur(Svartur), Fill image), staðsettning
                   ColourImageFile(screen, "car.png", 10, 0, True),
                   (screen.height-8), Screen.COLOUR_WHITE),
        Print(screen, StaticRenderer(images=[logo]), 2),
        Print( screen, FigletText('Car Rental', font= 'big'), 14),
        Print( screen, FigletText('The BEST!', font= 'small'), 20, colour=Screen.COLOUR_GREEN),
        Print(screen,
              StaticRenderer(images=[Welcome]), 25) ]
    scenes.append(Scene(effects, 0))

    screen.play(scenes, stop_on_resize=True, repeat=True)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
