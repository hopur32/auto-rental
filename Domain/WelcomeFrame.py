from copy import deepcopy
import sys
from asciimatics.exceptions import ResizeScreenError
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Sprite, Effect, BannerText

class BannerText(Effect):
    """
    Special effect to scroll some text (from a Renderer) horizontally like a
    banner.
    """

    def __init__(self, screen, renderer, y, colour, bg=Screen.COLOUR_BLACK,
                 **kwargs):
        """
        :param screen: The Screen being used for the Scene.
        :param renderer: The renderer to be scrolled
        :param y: The line (y coordinate) for the start of the text.
        :param colour: The default foreground colour to use for the text.
        :param bg: The default background colour to use for the text.
        Also see the common keyword arguments in :py:obj:`.Effect`.
        """
        super(BannerText, self).__init__(screen, **kwargs)
        self._renderer = renderer
        self._y = y
        self._colour = colour
        self._bg = bg
        self._text_pos = None
        self._scr_pos = None

    def reset(self):
        self._text_pos = 0
        self._scr_pos = self._screen.width

    def _update(self, frame_no):
        if self._scr_pos == 0 and self._text_pos < self._renderer.max_width:
            self._text_pos += 3

        if self._scr_pos > 0:
            self._scr_pos -= 3

        image, colours = self._renderer.rendered_text
        for (i, line) in enumerate(image):
            line += " "
            colours[i].append((self._colour, 2, self._bg))
            end_pos = min(
                len(line),
                self._text_pos + self._screen.width - self._scr_pos)
            self._screen.paint(line[self._text_pos:end_pos],
                               self._scr_pos,
                               self._y + i ,
                               self._colour,
                               bg=self._bg,
                               colour_map=colours[i][self._text_pos:end_pos])

    @property
    def stop_frame(self):
        return self._start_frame + self._renderer.max_width + self._screen.width



def demo(screen):
    scenes = []
    centre = (screen.width // 2, screen.height // 2)

    effects = [
        BannerText(screen,
                   ColourImageFile(screen, "car.png", 10, 0, True),
                   (screen.height - 16) // 2,
                   Screen.COLOUR_WHITE),
        Print(screen,
              StaticRenderer(images=["Auto-Car-Rental:"
                                     " Árni Dagur, Bertinna Vass, Emil Trausti, Eva Ósk, Viktor Máni"]),
              screen.height - 1)
    ]
    scenes.append(Scene(effects))
 



    effects = [
        Print(screen, FigletText("Auto-Car-Rental", font='big'), screen.height // 3),
        Print(screen,
              StaticRenderer(images=["< Press enter to continue >"]),
              screen.height - 1)
    ]
    scenes.append(Scene(effects, 0,1))

    screen.play(scenes, stop_on_resize=True, repeat=False)


if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(demo)
            sys.exit(0)
        except ResizeScreenError:
            pass
