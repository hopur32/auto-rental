from Domain.Graph import Piechart, Histogram, Linegram
from Data.Data import Data, ID

from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, DropdownList, TextBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene
from datetime import datetime
import sys
import os


graph_list=list()
order_list=list()
customer_list=list()
car_list=list()


def get_info():
    vehicletable = Data(
        'Vehicles.txt',
        ['License Plate', 'Manufacturer', 'Model', 'Year', 'Location', 'Category'],
        [str, str, str, int, str, str]
    )
    ordertable = Data(
        'Orders.txt',
        ['Order ID', 'Customer', 'Vehicle', 'Start Date', 'End Date', 'Extra Insurance', 'GPS'],
        [ID, str, str, datetime, datetime, bool, bool]
    )

    for item in ordertable.get_rows():
        order_list.append(item.values())
    for item in vehicletable.get_rows():
        car_list.append(item.values())



def make_graph_list():
    sizes = [0] * 4
    for row in car_list:
        if row[5].lower() in ['small', 'small car']:     sizes[0] += 1
        elif row[5].lower() in ['medium', 'medium car']: sizes[1] += 1
        elif row[5].lower() in ['large', 'large car']:  sizes[2] += 1
        elif row[5].lower() in ['jeep']:   sizes[3] += 1

    all_cars = Piechart(
        hight=7,
        stuff_in_piechart=[
            ('Small', sizes[0]),
            ('Medium', sizes[1]),
            ('Large', sizes[2]),
            ('Jeep', sizes[3])
        ], 
        name='Piechart of all cars in each size category'
    )
    all_cars.get_chart() 
    graph_list.append(all_cars)

    a,n=0,0
    for row in car_list:
        if row[6]==True:    a+=1
        else:               n+=1

    cars_availability = Piechart(
        hight=7,
        stuff_in_piechart=[
            ('Available', a),
            ('Out-rented', n)
        ],
        name='Piechart of availability of cars')
    cars_availability.get_chart() 
    graph_list.append(cars_availability)

    
    months = {}
    for i in range(1,13):
        months[i] = 0
    for row in order_list:
        try:
            months[row[3].month] += 1
        except IndexError:
            pass

    line_income=Linegram(
        name='Line graph of orders between months', 
        names_of_x=['Jan', 'Feb', 'Mars', 'April', 'May', 'June', 'July', 'Agu', 'Sept', 'Okt', 'Nov', 'Dec'],
        values=[item[1] for item in sorted(months.items())]
    )
    line_income.update_table()
    graph_list.append(line_income)

    s,m,l,j=0,0,0,0
    for row in car_list:
        if row[5]=='Small' and row[6]:     s+=1
        elif row[5]== 'Medium' and row[6]: m+=1
        elif row[5]== 'Large' and row[6]:  l+=1
        elif row[5]== 'Jeep'and row[6]:   j+=1

    car_available_graph=Histogram(
        name='Histogram of all available cars in each size category', 
        names_of_x=['Small', 'Medium', 'Large', 'Jeep'],
        values=[s,m,l,j]
    )
    car_available_graph.update_table()
    graph_list.append(car_available_graph)

    s,m,l,j=0,0,0,0
    for row in car_list:
        if row[5]=='Small' and not row[6]:     s+=1
        elif row[5]== 'Medium' and not row[6]: m+=1
        elif row[5]== 'Large' and not row[6]:  l+=1
        elif row[5]== 'Jeep' and not row[6]:   j+=1

    car_out_graph=Histogram(
        name='Histogram of all out rented cars in each size category', 
        names_of_x=['Small', 'Medium', 'Large', 'Jeep'],
        values=[s,m,l,j]
    )
    car_out_graph.update_table()
    graph_list.append(car_out_graph)


class GraphFrame(Frame):
    def __init__(self, screen, footer=dict(), scene_keybinds=None):
        super(GraphFrame, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=False,
            name="My Form"
        )

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        self.__scene_keybinds= scene_keybinds
        self._graph = TextBox(25, name='graph', as_string=True )
        self._graph.disabled = True     

        self._graph.custom_colour= 'label'

        self._list = DropdownList(dropdown_options, label= 'Pick a graph', name='dropdown')
        self._graph.value= str(graph_list[self._list.value])
        
        self._list._on_change = self.on_change
        
        footers = ['[{}] {}'.format(key, text) for key, text in footer.items()]
        default_footer_text = '[q] Quit'
        self.__footer= Label(' '.join(footers) + ' ' + default_footer_text)


        layout.add_widget(self._list)
        layout.add_widget(self._graph)
        layout.add_widget(self.__footer)

        self.set_theme('monochrome')

        self.fix()
 
    def on_change(self):
        self.save()
        n=self.data['dropdown']
        self._graph.value = str(graph_list[n])


    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if self.__scene_keybinds:
                for keybind, scene in self.__scene_keybinds.items():
                    if event.key_code in [ord(keybind.lower()), ord(keybind.upper())]:
                        raise NextScene(scene)
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        return super(GraphFrame, self).process_event(event)



make_graph_list()
get_info()
dropdown_options=[(graph_list[i].name, i) for i in range(len(graph_list))]
