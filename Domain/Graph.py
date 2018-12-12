class Graph:

    def __init__(self, name='Name of graph',
                 names_of_x=['A', 'B', 'C'],
                 values=[17, 21, 35], yspace=2, size=15):

        self.names_of_x, self.values= names_of_x, values
        self.name=name

        self.size = size

        self.table = list()
        self.table.append(name + '\n' * yspace)

        self.maxvalue = max(values)

        whole_number = self.maxvalue // (self.size)
        self.maxlen = self.find_max_len()
        self.xspace = self.maxlen+1
        self.lentapel = (len(self.names_of_x)) * self.xspace * 2
    # Fspacesa hoppið
        if self.maxvalue==0:
            self.jump =1
        elif (whole_number) < (self.maxvalue / (self.size)):
            self.jump = whole_number + 1
        else:
            self.jump = whole_number

    def find_max_len(self):
        max0 = len(self.names_of_x[0])
        for i in self.names_of_x:
            if len(i) > max0:
                max0 = len(i)
        return max0

    def get_table(self):

        for i in range((self.size), -1, -1):
            line_str_in_tabel = '{:>5}│'.format(
                int(i * self.jump)) + ' ' * (self.lentapel)
            line_in_tabel = [[x]for x in line_str_in_tabel]
            self.table.append(line_in_tabel)

        self.table.append('▔' * (self.lentapel + self.xspace))
        line_with_x_names = ' ' * (self.xspace + 5)
    # Names of objects on X-axis
        for item in self.names_of_x:
            line_with_x_names += item.rjust(self.maxlen) + ' ' * self.xspace
        self.table.append(line_with_x_names)

    def __str__(self):
        string1 = ''
        for line in self.table:
            string0 = ''
            for letter in line:
                string0 += letter[0]
            string1 += string0 + '\n'
        return string1
    



class Histogram(Graph):

    '''
    60  |           55
    55  |           █
    50  |           █
    45  |           █
    35  |           █
    30  |           █
    25  |           █
    20  |           █
    15  |   11      █
    10  |   ▄       █
    5   |   █       █       5
    0   |   █       █       █
        ______________________________
            D      E       F
        '''

    def __init__(self, name='Name of graph',
                 names_of_x=['A', 'B', 'C'],
                 values=[10, 15, 10],
                 yspace=2, fill=False):
        Graph.__init__(self, name, names_of_x, values, yspace)

        self.fill = fill

    def get_top_block(self, num):
        if 0 <= num < 0.25:
            return ' '
        elif 0.25 <= num < 0.75:
            return '▄'
        elif 0.75 <= num < 1:
            return '█'
        else:
            raise ValueError('Number {} is not 0 <= x < 1'.format(num))

    def update_table(self):

        Graph.get_table(self)
        jump, size = self.jump, self.size
        spaces = 4
        if self.fill:
            width = self.maxlen + self.xspace
        else:
            width = 1

        for value in self.values:
            spaces += self.xspace + self.maxlen
            for i in range(size, 0, -1):
                if ((size + 1) * jump - value) <= (i * jump):
                    self.table[i + 1][spaces:(spaces + width)] = '█' * width
                else:
                    num = value % jump / jump
                    block = self.get_top_block(num)
                    self.table[i + 1][spaces:(spaces + width)] = block * width
                    break


class Linegram(Graph):

    '''
    60  |
    55  |
    50  |
    45  |               *
    35  |             _/ \
    30  |           _/    |
    25  |          /      \
    20  |    _____*  	   |
    15  |   *              |
    10  |  /        	   \
    5   | /                 |
    0   |/                   \
        ______________________________
            D     E     F     G
        '''

    '''
    60  |
    55  |
    50  |
    45  |               +
    35  |             ** *
    30  |           **    *
    25  |          *      *
    20  |    +****+  	   *
    15  |   *              *
    10  |  *        	   *
    5   | *                 *
    0   |*                   *
        ______________________________
            D     E     F     G
            🡒 🡑 🡓 🡔 🡕 🡖
        '''
    '''
    60  |
    55  |
    50  |
    45  |               *
    35  |              🡕 🡖
    30  |           🡒🡕    🡓
    25  |          🡕       🡖
    20  |    🡒🡒🡒*  	     🡓
    15  |   *               🡓
    10  |  🡕        	     🡖
    5   | 🡕                 🡓
    0   |🡕                   🡖
        ______________________________
            D     E     F     G
        '''

    def __init__(self, name='Name of graph',
                 type_of_line='A',
                 names_of_x=['A', 'B', 'C'],
                 values=[10, 15, 10],
                 yspace=2):
        r'''Type of line S= stars'*', A= arrows '- 🡕 🡖', L= lines '/\-' '''

        Graph.__init__(self, name, names_of_x, values, yspace)

        self.type_of_line = type_of_line.upper()

    def update_table(self):
        size = self.size
        jump = self.jump

        Graph.get_table(self)

        list_of_locations = list()
        spaces = 4
        for value in self.values:

            spaces += self.maxlen + self.xspace
            for i in range(size + 2):
                if ((size + 1) * jump - value) <= (i * jump):
                    self.table[i][spaces] = 'O'
                    list_of_locations.append((i, spaces))
                    break

        i1, spaces1 = list_of_locations.pop(0)

        for staðsetning in list_of_locations:
            i, spaces = staðsetning
            stepps = i1 - i
            i1, spaces1 = staðsetning
            slope = stepps / (self.maxlen + self.xspace)

            for j in range(1, self.xspace + self.maxlen):
                number = slope * j

            # Með örvum
                if self.type_of_line == 'A':
                    if int(number) > 0:
                        self.table[int(i + number)][spaces - j] = '🡕'
                    elif int(number) < 0:
                        self.table[int(i + number)][spaces - j] = "🡖"
                    elif int(number) == 0:
                        self.table[int(i + number)][spaces - j] = '━'

            # Með línum
                elif self.type_of_line == 'L':
                    if int(number) > 0:
                        self.table[int(i + number)][spaces - j] = '/'
                    elif int(number) < 0:
                        self.table[int(i + number)][spaces - j] = r"\ "
                    elif int(number) == 0:
                        self.table[int(i + number)][spaces - j] = '-'
            # Með stjörnum
                else:
                    self.table[int(i + number)][spaces - j] = '*'


class Piechart:
    def __init__(self, hight=3, length=50,
                 stuff_in_piechart=[('A', 10), ('B', 15), ('C', 10)],
                 character_list='░▒▓█▘╳╬♥♣♦♠#_XO',
                 name='Name of chart'):

        self.hight, self.length, self.stuff_in_piechart = hight, length, stuff_in_piechart
        self.character_list = character_list
        self.name=name
        self.table = name + '\n\n'

        list_length = [item[1] for item in self.stuff_in_piechart]
        self.length = sum(list_length)

    def get_chart(self):
        for num in range(len(self.stuff_in_piechart)):
            self.table += ('\t{} - {}\n'.format(
                self.character_list[num], self.stuff_in_piechart[num][0]))
        self.table += '\n'

        for i in range(self.hight):
            for num in range(len(self.stuff_in_piechart)):

                magn = self.stuff_in_piechart[num][1]
                tákn = self.character_list[num]
                if self.length != 0:
                    for j in range(int(magn * self.length / self.length)):
                        self.table += tákn

            self.table += '\n'

    def __str__(self):
        string0 = ''
        for item in self.table:
            string0 += item
        return string0

values = [4, 7.8, 3, 5.2, 1, 0.2, 9]
names = ['Four', 'B', 'Ullarpeysa', 'Hundaæði', 'Age star', 'SMALL', '__--!']
graph = Linegram(values=values, names_of_x=names)
graph.update_table()
print(graph)