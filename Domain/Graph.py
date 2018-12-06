class Graph:

    def __init__(self,names_of_x=   ['Jan', 'Feb', 'Mars', 'April', 'May', 'June', 'July', 'Agu', 'Sept', 'Okt','Nov', 'Dec'], 
                    values=         [   17,   21,   35,      21,      0,         46,     29,    77,    77,     23,   98,    102], 
                    xspace=5,yspace=2):
        
        'Names of x can not bee longer than 5 characters'
        
        self.names_of_x, self.values, self.xspace=names_of_x, values,xspace

        self.size=15
        self.taple=list()
        self.taple.append('\n'*yspace)
        self.maxvalue=max(values)

        heiltölu=self.maxvalue//(self.size)
        self.maxlen=self.find_max_len()
        self.lentapel=(len(self.names_of_x))*self.xspace*2
    #Finna hoppið
        if (heiltölu)<(self.maxvalue/(self.size)):    self.jump=heiltölu+1
        else:                                         self.jump=heiltölu



    def find_max_len(self):
        max0=len(self.names_of_x[0])
        for i in self.names_of_x:
            if len(i)>max0:  max0=len(i)
        return max0
    
    def get_taple(self):
    

        for i in range((self.size),-1,-1):
            line_str_in_tapel='{:>5}│'.format(i*self.jump)+' '*(self.lentapel)
            line_in_tapel=[[x]for x in line_str_in_tapel]
            self.taple.append(line_in_tapel)


        self.taple.append('▔'*(self.lentapel+self.xspace+4))
        line_with_x_names=' '*(self.xspace+5)
    #Nöfn viðfangsefna á X-ás
        for item in self.names_of_x:
            line_with_x_names+='{:<5}'.format(item)+' '*self.xspace
        self.taple.append(line_with_x_names)


    def __str__(self):
        string1=''
        for line in self.taple:
            string0=''
            for letter in line:
                string0+=letter[0]
            string1+=string0+'\n'
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

    def __init__(self):
        Graph.__init__(self)
    def update_taple(self):

        Graph.get_taple(self)
        jump, size=self.jump, self.size
        inn=0

        for value in self.values:
            inn+=5+self.xspace
            for i in range(size+1,0,-1):
                if ((size+1)*jump-value)<=(i*jump):   
                    self.taple[i][inn]='█'
                elif value%jump> jump/2: 
                    self.taple[i][inn]='▄'
                    break
class Columgraph(Graph):

    '''
    60  |    
    55  |    █
    50  |    █
    45  |    █
    35  |    █
    30  |    █ 
    25  |    █       
    20  |    █  	    
    15  |    █       
    10  |   ▄█       
    5   |   ██
    0   |   ███
        _________
            DEF      
        '''

    def __init__(self):
        Graph.__init__(self)
    def update_taple(self):

        Graph.get_taple(self)
        jump, size=self.jump, self.size
        inn=0

        for value in self.values:
            inn+=self.maxlen+self.xspace
            for i in range(size+1,0,-1):
                if ((size+1)*jump-value)<=(i*jump):   
                    self.taple[i][inn:(inn+self.maxlen+self.xspace)]='█'*(self.maxlen+self.xspace)
                elif value%jump> jump/2: 
                    self.taple[i][inn:(inn+self.maxlen+self.xspace)]='▄'*(self.maxlen+self.xspace)
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

    def __init__(self, type_of_line='A'):
        '''Type of line S= stars'*', A= arrowes '🡒 🡕 🡖', L= lines '/\-' '''

        Graph.__init__(self)
        self.type_of_line= type_of_line.upper()

    def update_taple(self):
        size=self.size
        jump=self.jump

        Graph.get_taple(self)

        listi_staðsettninga=list()
        inn=0
        for value in self.values:

            inn+=5+self.xspace
            for i in range(size+2):
                if ((size+1)*jump-value)<=(i*jump):   
                    self.taple[i][inn]='O'
                    listi_staðsettninga.append((i,inn))
                    break

        i1,inn1=listi_staðsettninga.pop(0)
        #listi_staðsettninga.remove(listi_staðsettninga[-1])
        
        for staðsetning in listi_staðsettninga:
            i,inn= staðsetning
            stepps= i1-i 
            i1,inn1= staðsetning 
            hallatala=stepps/(self.maxlen+self.xspace)

            for j in range(1,self.xspace+self.maxlen):
                tala=hallatala*j

            #Með örvum
                if self.type_of_line=='A':
                    if int(tala)>0:
                        self.taple[int(i+tala)][inn-j]='🡕'
                    elif int(tala)<0:
                        self.taple[int(i+tala)][inn-j]="🡖"
                    elif int(tala)==0:
                        self.taple[int(i+tala)][inn-j]='━'

            #Með línum
                elif self.type_of_line=='L':
                    if int(tala)>0:
                        self.taple[int(i+tala)][inn-j]='/'
                    elif int(tala)<0:
                        self.taple[int(i+tala)][inn-j]="\ "
                    elif int(tala)==0:
                        self.taple[int(i+tala)][inn-j]='-'
            #Með stjörnum
                else:
                    self.taple[int(i+tala)][inn-j]='*'

class Piechart:
    def __init__(self, hight=3, lenth=50, stuff_in_piechart=[('Small Cars', '#', 0.55),('Medium Cars', 'o', 0.14), 
                                                             ('Large Cars', 'X', 0.31)]):            
            self.hight, self.lenth, self.stuff_in_piechart= hight, lenth, stuff_in_piechart
            self.taple=''

    
    def get_chart(self):
        for item in self.stuff_in_piechart:     self.taple+=('\t{} - {}\n'.format(item[1], item[0]))
        self.taple+='_'*(self.lenth+len(self.stuff_in_piechart)+2)+'\n'
        for i in range(self.hight): 
            for item in self.stuff_in_piechart:
                self.taple+='|'
                magn=item[2]
                tákn=item[1]
                for j in range(int(magn*self.lenth)):
                    self.taple+= tákn
                self.taple+='|'
            self.taple+= '\n'
        self.taple+='▔'*(self.lenth+len(self.stuff_in_piechart)+1)            
    
    def __str__(self):
        string0=''
        for item in self.taple: string0+=item
        return string0	  

            



        
    
# linurit=Linegram(type_of_line=	'S')
# linurit.update_taple()
# print(str(linurit))
# linurit=Linegram(type_of_line=	'L')
# linurit.update_taple()
# print(str(linurit))


linurit=Linegram()
linurit.update_taple()
print(str(linurit))


súlurit=Histogram()
súlurit.update_taple()
print(str(súlurit))

staplarit=Columgraph()
staplarit.update_taple()
print(str(staplarit))

skífurit=Piechart()
skífurit.get_chart()
print(str(skífurit))