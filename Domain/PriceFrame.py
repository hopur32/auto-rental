from asciimatics.widgets import Frame, Layout, Widget, Label, Text, TextBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys
import os

PRICE = {'Small Car':2900, 'Medium Car': 3900, 'Large Car': 4900, 'Jeep': 5900,
'Basic insurance': 0, 'Extra insurance': 850, 'GPS': 350}
PRICE_LIST= [[key, '{:,} ISK'.format(value ), '{:,} ISK'.format(value*7 ), '{:,} ISK'.format(value*30 ), 
'{:,} ISK'.format(value*182)] for key, value in PRICE.items()]
header='{:<20}\t{:>15} {:>15} {:>15} {:>15}\n'.format('', '1 day', '1 week', '1 month', '6 months')
price_string= ''
for line in PRICE_LIST:
    price_string+='{:<20}\t{:>15} {:>15} {:>15} {:>15}\n'.format(line[0], line[1], line[2], line[3], line[4])


class PriceFrame(Frame):
    def __init__(self, screen, footer=dict()):
        super(PriceFrame, self).__init__(
            screen, screen.height, screen.width, has_border=True, name="My Form")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        self._price = TextBox(25, name='pricelist', as_string=True )
        self._price.value = price_string
        self._price.disabled = True
        footers = ['[{}] {}'.format(key, text) for key, text in footer.items()]
        default_footer_text = '[q] Quit'
        self.__footer= Label(' '.join(footers) + ' ' + default_footer_text)

        layout.add_widget(Label('{:<20}\t{:>15} {:>15} {:>15} {:>15}'.format('', '1 day', '1 week', '1 month', '6 months')))   
        layout.add_widget(self._price)
        layout.add_widget(self.__footer)  

        self.set_theme('monochrome')

        self.fix()
 
