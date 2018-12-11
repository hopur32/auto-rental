from Graph import Piechart, Histogram, Linegram
from Data.Data import Data

from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, DropdownList, TextBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from datetime import datetime
import sys
import os


graph_list=list()
order_list=list()
customer_list=list()
car_list=list()


def get_info():
    customertable = Data(
    'Customers.txt',
    ['Kennitala', 'First Name', 'Last name', 'Phone Nr.', 'Email', 'DOB', 'Credit Card', 'Expiration Date', 'Ethnicity'],
    [int, str, str, str, str, datetime, str, datetime, str]
    )
    vehicletable = Data(
        'Vehicles.txt',
        ['License Plate', 'Manufacturer', 'Model', 'Year', 'Location', 'Category', 'Available'],
        [str, str, str, int, str, str, bool]
    )
    ordertable = Data(
        'Orders.txt',
        ['ID', 'Customer', 'Vehicle', 'Start Date', 'End Date', 'Insurance', 'Extra Objects'],
        [str, str, str, datetime, datetime, str, str]
    )

    for item in ordertable.get_rows():
        order_list.append(item.values())
    for item in vehicletable.get_rows():
        car_list.append(item.values())
    for item in customertable.get_rows():
        customer_list.append(item.values())


def make_graph_list():
    s,m,l,j=0,0,0,0
    for row in car_list:
        if row[5]=='Small':     s+=1
        elif row[5]== 'Medium': m+=1
        elif row[5]== 'Large':  l+=1
        elif row[5]== 'Jeep':   j+=1

    all_cars = Piechart(hight=7, stuff_in_piechart=[('Small', s),('Medium', m), ('Large', l), ('Jeep', j)], 
    name='Piechart of all cars in each size category')
    all_cars.get_chart() 
    graph_list.append(all_cars)

    a,n=0,0
    for row in car_list:
        if row[6]==True:    a+=1
        else:               n+=1

    cars_availability = Piechart(hight=7, stuff_in_piechart=[('Available', a),('Out-rented', n)], name='Piechart of cars availability')
    cars_availability.get_chart() 
    graph_list.append(cars_availability)

    j,f,m,a,m1,j1,j2,a1,s,o,n,d=0,0,0,0,0,0,0,0,0,0,0,0
    for row in order_list:
        if row[3].month== 1:      j+=1
        elif row[3].month== 2:    f+=1
        elif row[3].month== 3:    m+=1
        elif row[3].month== 4:    a+=1
        elif row[3].month== 5:    m1+=1
        elif row[3].month== 6:    j1+=1
        elif row[3].month== 7:    j2+=1
        elif row[3].month== 8:    a1+=1
        elif row[3].month== 9:    s+=1
        elif row[3].month== 10:   o+=1
        elif row[3].month== 11:   n+=1
        elif row[3].month== 12:   d+=1


    line_income=Linegram(name='Line graph of orders between months', 
    names_of_x=['Jan', 'Feb', 'Mars', 'April', 'May', 'June', 'July', 'Agu', 'Sept', 'Okt', 'Nov', 'Dec'],
    values=[j,f,m,a,m1,j1,j2,a1,s,o,n,d])
    line_income.update_table()
    graph_list.append(line_income)

        #sleppa?
    # customers_graph=Histogram(name='Histogram of all customers between nations', 
    # names_of_x=['Is', 'Dk', 'USA'],
    # values=[1,2,3])
    # customers_graph.update_table()
    # graph_list.append(customers_graph)

    s,m,l,j=0,0,0,0
    for row in car_list:
        if row[5]=='Small' and row[6]:     s+=1
        elif row[5]== 'Medium' and row[6]: m+=1
        elif row[5]== 'Large' and row[6]:  l+=1
        elif row[5]== 'Jeep'and row[6]:   j+=1

    car_available_graph=Histogram(name='Histogram of all available cars in each size category', 
    names_of_x=['Small', 'Medium', 'Large', 'Jeep'],
    values=[s,m,l,j])
    car_available_graph.update_table()
    graph_list.append(car_available_graph)

    s,m,l,j=0,0,0,0
    for row in car_list:
        if row[5]=='Small' and not row[6]:     s+=1
        elif row[5]== 'Medium' and not row[6]: m+=1
        elif row[5]== 'Large' and not row[6]:  l+=1
        elif row[5]== 'Jeep' and not row[6]:   j+=1

    car_out_graph=Histogram(name='Histogram of all out rented cars in each size category', 
    names_of_x=['Small', 'Medium', 'Large', 'Jeep'],
    values=[s,m,l,j])
    car_out_graph.update_table()
    graph_list.append(car_out_graph)


class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="My Form")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        self._graph = TextBox(25, name='graph', as_string=True, )
        self._graph.disabled = True     

        self._graph.custom_colour= 'label'

        self._list = DropdownList(dropdown_options, label= 'Pick a grafh', name='dropdown')
        self._graph.value= str(graph_list[self._list.value])
        
        self._list._on_change = self.on_change
        

        layout.add_widget(self._list)
        layout.add_widget(self._graph)
        layout.add_widget(Label("Press Enter to select or `q` to quit."))

        self.set_theme('monochrome')

        self.fix()
 
    def on_change(self):
        self.save()
        n=self.data['dropdown']
        self._graph.value = str(graph_list[n])


    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord('q'), ord('Q'), Screen.ctrl("c")]:
                raise StopApplication("User quit")

        return super(DemoFrame, self).process_event(event)


def demo(screen, old_scene):
    screen.play([Scene([DemoFrame(screen)], -1)], stop_on_resize=True, start_scene=old_scene)


make_graph_list()
get_info()
dropdown_options=[(graph_list[i].name, i) for i in range(len(graph_list))]




last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
