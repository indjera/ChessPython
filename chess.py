import math
import shelve
import sys
class point:
    ''' Извлича необходимата информация  от нотацията в удобна структура,
         разглежда различни случаи според дължината    '''
    def __init__(self,notation):
        n_len = len(notation)
        self.state = None
        if (n_len == 7) or (n_len == 8 and notation[7] in ['+','x']):
            self.x = int(notation[3]) - 1
            self.y = self._get_number(notation[2])
            self.z = int(notation[6]) - 1
            self.t = self._get_number(notation[5])
            self.kind = 'P'
            self.op = notation[4]
            if n_len == 8:
                self.state = notation[7]

        elif n_len > 7:
            self.x = int(notation[4]) - 1
            self.y = self._get_number(notation[3])
            self.z = int(notation[7]) - 1
            self.t = self._get_number(notation[6])
            self.kind = notation[2]
            self.op = notation[4]
            if n_len == 9:
                self.state = notation[8]
        else:
            raise  IOError       
    def _get_number(self,char):
        ''' Преобразува [a..h]->[1..8]'''
        return ord(char) - ord('a') 
    
class chess_table:
    def __init__(self):
        self.table=[]
        self.list_moves = []
        self.count = 32
        for i in range(8):
            if i == 1:
                self.table.append(['p','p','p','p','p','p','p','p'])
            elif i == 6:
                self.table.append(['P','P','P','P','P','P','P','P'])
            elif i == 0:
                self.table.append(['r','n','b','q','k','b','n','r'])  
            elif i == 7:
                self.table.append(['R','N','B','Q','K','B','N','R'])
            else:
                self.table.append([0,0,0,0,0,0,0,0])
           
    def print_t(self):
        print()
        print(" "," ",end = "")
        for i in range(65,73):
            print(chr(i),end =" ")
        for i in range(0,8):
            print()
            print(i+1,end ="| ")
            for j in range(8):
                print(self.table[i][j],end=" ")
        print()
        print()
        
    
    def _set(self,p):
        '''Безусловно отразява промените върху дъската
           ,грижи се единствено "да не вземаме собствени фигури '''
        if self.table[p.z][p.t] != 0:
            ok = ord(self.table[p.x][p.y]) <  91
            ok1 = ord(self.table[p.z][p.t]) < 91
            if (ok and ok1) or (not ok and not ok1):
                raise IOError   
            
        val = self.table[p.x][p.y]
        self.table[p.x][p.y] = 0            
        self.table[p.z][p.t] = val
                 
    def p_move(self,p):
        '''Реализира движението на пешката като прави необходимите проверки'''
        if p.y == p.t and self.table[p.x][p.y] in ['p','P']:
            if self.table[p.x][p.y] == 'p' and p.z - p.x == 1:
                self._set(p)
            elif self.table[p.x][p.y] == 'P' and p.x - p.z == 1:
                self._set(p)   
            elif p.x == 1 and  p.z - p.x == 2:
                self._set(p)
            elif p.x == 6 and  p.x - p.z == 2:
                self._set(p)
            else:
                raise IOError
        else:
            raise IOError   
        
    def r_move(self,p):
        '''Реализира движението на топа като прави необходимите проверки ,проверява дали всички полета
        между двете позиции са празни '''
        if self.table[p.x][p.y] in ['r','R','q','Q','k','K']:
            if p.y == p.t:
                ok = True
                for i in range(min(p.x,p.z) + 1 ,max(p.x,p.z)):
                    if self.table[i][p.y] != 0:
                        ok = False
                if ok:
                    self._set(p)
                else:
                    raise IOError    
            elif p.x == p.z:
                ok = True
                for i in range(min(p.y,p.t) + 1,max(p.y,p.t)):
                    if self.table[p.x][i] != 0:
                        ok = False
                if ok:
                    self._set(p)
                else:
                    raise IOError
            else:
                raise IOError
        else:
            raise IOError
    
    def b_move(self,p):
        ''' Реализира движението на офицера като прави необходимите проверки ,съобразява местоположението 
        и обхожда главния или второстепенния диагонал'''
         
        if self.table[p.x][p.y] in ['b','B','q','Q','k','K']:
            if math.fabs(p.x - p.z) == math.fabs(p.y - p.t):
                ok = True
                if p.x < p.z and p.y > p.t or p.x > p.z and p.y < p.t :
                    x =  min(p.x,p.z)
                    y =  max(p.y,p.t)
                    while x + 1 < max(p.x,p.z) and y -1 > min(p.y,p.t):
                        y = y - 1
                        x = x + 1
                        if self.table[x][y] != 0:
                            ok = False
                else:
                    x =  max(p.x,p.z)
                    y =  max(p.y,p.t)
                    while x - 1 > min(p.x,p.z) and y -1 > min(p.y,p.t):
                        y = y - 1
                        x = x - 1
                        if self.table[x][y] != 0:
                            ok = False
                if ok:                  
                    self._set(p)
                else:
                    raise IOError
            else:
                raise IOError     
        else:
            raise IOError    
    def q_move(self,p):
        '''Реализира движението на царицата посредством топа и офицера'''
        if self.table[p.x][p.y] in ['q','Q','k','K']:
            try:
                self.b_move(p)
            except IOError:                
                self.r_move(p)
        else:
            raise IOError    
        
    def k_move(self,p):
        '''Реализира движението на царя посредством царицата'''
        if self.table[p.x][p.y] in ['k','K']:
            if math.fabs(p.x - p.z) == 1  and  math.fabs(p.y - p.t) == 1:
                self.q_move(p)
            elif math.fabs(p.x - p.z) == 1  and  math.fabs(p.y - p.t) == 0:
                self.q_move(p)
            elif math.fabs(p.x - p.z) == 0  and  math.fabs(p.y - p.t) == 1:
                self.q_move(p)
            else:
                raise IOError
        else:
            raise IOError
        
    def n_move(self,p):
        '''Реализира движението на коня'''
        if self.table[p.x][p.y] in ['n','N']:
            if math.fabs( p.x- p.z) == 1 and math.fabs(p.y - p.t) == 2:
                self._set(p)
            elif math.fabs( p.x- p.z) == 2 and math.fabs(p.y - p.t) == 1:
                self._set(p)
            else:
                raise IOError
        else:
            raise IOError
        
    def castling(self):
        '''Малко рокадо'''
        if self.table[0][0] == 'r' and self.table[0][4] == 'k':
            self.r_move(point("1.Ra1-d1"))
            self._set(point("1.Ke1-c1"))
        elif self.table[7][0] == 'R' and self.table[7][4] == 'K':
            self.r_move(point("1.Ra8-d8"))
            self._set(point("1.Ke8-c8"))
        else:
            raise IOError
        
    def castling_l(self):
        '''Голямо рокадо'''
        if self.table[0][7] == 'r' and self.table[0][4] == 'k':
            self.r_move(point("1.Rh1-f1"))
            self._set(point("1.Ke1-g1")) 
        elif self.table[7][7] == 'R' and self.table[7][4] == 'K':
            self.r_move(point("1.Rh8-f8"))
            self._set(point("1.Ke8-g8"))
        else:
            raise IOError
    def show(self,notation):
        '''Показва конкретния ход за кой фигури се отнася бели или черни'''
        p = point(notation)
        if ord(self.table[p.x][p.y]) > 91 :
            return True
        else:
            return False
         
    def save(self,savename):
        mydb = shelve.open("mydb.db")
        mydb[savename] = self.list_moves
        mydb.close()
        
    def clean(self):
        mydb = shelve.open("mydb.db")
        mydb.clear()
        mydb.close()
                
    def load(self,savename):
            mydb = shelve.open("mydb.db")
            self.list_moves = mydb[savename]
            mydb.close()
            for i in range(len(self.list_moves)):
                self.move(self.list_moves[i])
                   
    def _get_x_y(self,f):
        '''Връща местоположението на даден тип фигури'''
        k = []
        for i in range(8):
            for j in range(8):
                if self.table[i][j] == f:
                    k.append([i,j])
        return k
    def try_move(self,p):
        '''Изпълнява даден ход след което връща дъската в първоначалния си вид'''
        val =  self.table[p.z][p.t]
        self.move(p)
        p.x,p.y,p.z,p.t = p.z,p.t,p.x,p.y
        self._set(p)
        self.table[p.x][p.y] = val
    
    def chess(self,p):
        '''При обявен шах проверява дали това наистина е така ползва try_move'''
        p.state = None
        ok = True
        if ord(self.table[p.z][p.t]) <= 91:
            (p.z,p.t) =self._get_x_y('K')[0]
            for i in range(8):
                for j in range(8):
                    if self.table[i][j] != 0 and ord(self.table[i][j]) < 91:
                        p.kind = self.table[i][j].upper()
                        p.x = i
                        p.y = j
                        try:
                            self.try_move(p)
                            ok = False
                        except IOError :
                            pass  
        else:
            (p.z,p.t) =self._get_x_y('K')[0]
            ok = True
            for i in range(8):
                for j in range(8):
                    if self.table[i][j] != 0 and ord(self.table[i][j]) > 91:
                        p.kind = self.table[i][j].upper()
                        p.x = i
                        p.y = j
                        try:
                            self.try_move(p)
                            ok = False
                        except IOError :
                            pass
        if ok: raise IOError    
        
    def get_figures(self):
        '''Връща текущото местоположение на всички фигури'''
        return [[self.table[i][j],i,j] for i in range(8) for j in range(8) if self.table[i][j] != 0]
    
    def move(self,notation):
        ''' Управляващата функция грижи се за извикването на подходящите фунции съответстващи на фигурите
        както и за натрупване на успешните ходове'''
        ok = True
        try:
            p = point(notation)
        except Exception:
            p = notation 
            ok = False
        if notation == "0-0-0":
            self.castling()
            self.list_moves.append(notation)
        elif notation == "0-0":
            self.castling_l()
            self.list_moves.append(notation)
        elif p:
            if all(map(lambda x: x in range(8),[p.x,p.y,p.z,p.t])):
                if p.kind == 'P':
                    self.p_move(p)
                elif p.kind == 'R':
                    self.r_move(p)
                elif p.kind == 'N':
                    self.n_move(p)
                elif p.kind == 'B':
                    self.b_move(p)
                elif p.kind == 'K':
                    self.k_move(p)
                elif p.kind == 'Q':
                    self.q_move(p)
                else:
                    raise IOError
                if p.state :
                    if p.state == 'x':pass
                    if p.state == '+': self.chess(p)
                if ok :
                    self.list_moves.append(notation)
                    if p.op == ':' :
                        self.count = self.count - 1
                        
            else:
                raise IOError
        else:
            raise IOError
        
def last_3(list_f):
    '''Проста проверка за изхода на играта при последните 3 фигури'''
    k = list(filter(lambda x:x[0] not in ['k','K'],list_f))[0]
    if k[0] in ['q','Q','r','R']:
        if ord(k[0]) > 91:
            return 1
        else: return 2
    elif k[0] in ['n','N','b','B']:
        return 0   
    else:
        if ord(k[0]) > 91: 
            king = list(filter(lambda x: ord(x[0]) < 91 ,list_f))[0]
            if k[1] - king[1] >= 2:
                return 1
            elif (7 - k[1]) < math.fabs(king[2] - k[2]) :
                return 1
            else:
                return 0
        else:
            king =  filter(lambda x: ord(x[0]) > 91 ,list_f)[0] 
            if  king[1] - k[1] > 1:
                return 2
            elif  k[1] < math.fabs(king[2] - k[2]):
                return 2
            else:
                return 0 
            
def playchess():
    turn = True
    print("New game: 1",end= "  ")
    print("Load game: 2",end="  ")
    print("Save game: 3",end = "  ")
    print("Exit: 4")
    print()
    while  True:
        try:
            notation = sys.stdin.readline().rstrip()
            if notation == '1':
                table = chess_table()
                table.print_t()
                continue
            elif notation == '2':
                table = chess_table()
                print("Load:")
                table.load(sys.stdin.readline().rstrip()) 
                table.print_t()
                continue
            elif notation == '3':
                print("Save:")
                table.save(sys.stdin.readline().rstrip())                
                continue  
            elif notation == '4':
                if table.count == 32:
                    exit()
                print("Save y/n:")
                notation = sys.stdin.readline().rstrip()
                if notation == 'y':
                    print("Save:")
                    table.save(sys.stdin.readline().rstrip()) 
                    exit()
                else:
                    exit()
            if table:
                if table.show(notation) != turn:
                    print("Isn't your turn")
                else:
                    table.move(notation)
                    if turn == False:
                        turn = True
                    else:
                        turn = False
                table.print_t()  
                if table.count < 4:
                    print('Winner: ',last_3(table.get_figures()))
        except KeyboardInterrupt as mess:
            print(mess)
        except IOError :
            print("Incorrect notation")
       
if __name__ == '__main__':
    playchess()