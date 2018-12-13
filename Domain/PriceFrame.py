from asciimatics.widgets import Frame, Layout, Widget, Label, Text, TextBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys
import os

PRICE = {'Small Car':2900, 'Medium car': 3900, 'Large car': 4900, 'Jeep': 5900,
'Basic insurance': 0, 'Extra insurance': 850, 'GPS': 350}
PRICE_LIST= [[key, '{:,} ISK'.format(value ), '{:,} ISK'.format(value*7 ), '{:,} ISK'.format(value*30 ), 
'{:,} ISK'.format(value*182)] for key, value in PRICE.items()]
header='{:<20}\t{:>15} {:>15} {:>15} {:>15}\n'.format('', '1 day', '1 week', '1 month', '6 months')
price_string= ''
for line in PRICE_LIST:
    price_string+='{:<20}\t{:>15} {:>15} {:>15} {:>15}\n'.format(line[0], line[1], line[2], line[3], line[4])


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="My Form")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        self._price = TextBox(25, name='pricelist', as_string=True )
        self._price.value = price_string
        self._price.disabled = True
        layout.add_widget(Label('{:<20}\t{:>15} {:>15} {:>15} {:>15}\n'.format('', '1 day', '1 week', '1 month', '6 months')))     
        layout.add_widget(self._price)
        layout.add_widget(Label("Press Enter to select or `q` to quit."))

        self.set_theme('monochrome')

        self.fix()
 

def demo(screen, old_scene):
    screen.play([Scene([DemoFrame(screen)], -1)], stop_on_resize=True, start_scene=old_scene)





last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
