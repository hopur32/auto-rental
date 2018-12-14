import sys
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Effect, BannerText

def demoWelcome(screen):
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

    Welcome='Welcome to this program\npress x to continue'

    effects = [
        Print(screen, StaticRenderer(images=[logo]), 2),
        Print( screen, FigletText('Car Rental', font= 'big'), 14),
        Print( screen, FigletText('The BEST!', font= 'small'), 20, colour=Screen.COLOUR_GREEN),
        Print(screen,
              StaticRenderer(images=[Welcome]), 25) ]
    scenes.append(Scene(effects, 0))

    screen.play(scenes, stop_on_resize=True, repeat=True)
