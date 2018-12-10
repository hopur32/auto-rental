from asciimatics.event import KeyboardEvent
from asciimatics.widgets import Frame, Layout, FileBrowser, Widget, Label, PopUpDialog, Text, DropdownList, TextBox
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
import sys
import os
from Graph import Piechart
from Graph import Histogram
from Graph import Linegram
graph_list=list()

def make_graph_list():

    all_cars = Piechart(hight=7, stuff_in_piechart=[('Small', 5),('Medium', 10), ('Large', 5)], 
    name='Piechart of all cars in each size category')
    all_cars.get_chart() 
    graph_list.append(all_cars)

    cars_availability = Piechart(hight=7, stuff_in_piechart=[('Available', 5),('Out-rented', 10)], name='Piechart of cars availability')
    cars_availability.get_chart() 
    graph_list.append(cars_availability)

    line_income=Linegram(name='Line graph of income between months', 
    names_of_x=['Jan', 'Feb', 'Mars', 'April', 'May', 'June', 'July', 'Agu', 'Sept', 'Okt', 'Nov', 'Dec'],
    values=[1,2,3,4,5,6,7,8,9,10,11,12])
    line_income.update_table()
    graph_list.append(line_income)

    customers_graph=Histogram(name='Histogram of all customers between nations', 
    names_of_x=['Is', 'Dk', 'USA'],
    values=[1,2,3])
    customers_graph.update_table()
    graph_list.append(customers_graph)

    car_available_graph=Histogram(name='Histogram of all available cars in each size category', 
    names_of_x=['Small', 'Medium', 'Large'],
    values=[1,2,3])
    car_available_graph.update_table()
    graph_list.append(car_available_graph)

    car_out_graph=Histogram(name='Histogram of all out rented cars in each size category', 
    names_of_x=['Small', 'Medium', 'Large'],
    values=[1,2,3])
    car_out_graph.update_table()
    graph_list.append(car_out_graph)





class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="My Form")

        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        self._graph = TextBox(25, name='graph', as_string=True)
        self._graph.disabled = True     

        self._graph.custom_colour= 'label'

        self._list = DropdownList(dropdown_options, label= 'Pick a grafh', name='dropdown')
        self._graph.value= str(graph_list[self._list.value])
        
        self._list._on_change = self.on_change
        

        layout.add_widget(self._list)
        layout.add_widget(self._graph)
        layout.add_widget(Label("Press Enter to select or `q` to quit."))

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
dropdown_options=[(graph_list[i].name, i) for i in range(len(graph_list))]




last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=False, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
