import unittest
from chess import *

class SimpleTests(unittest.TestCase):
    def test_last_3_1(self):
        self.assertEqual(last_3([['k',1,5],['r',4,3],['K',8,4]]), 1)
    def test_last_3_2(self):
        self.assertEqual(last_3([['k',2,3],['n',2,3],['K',7,7]]), 0)
    def test_last_3_3(self):
        self.assertEqual(last_3([['k',1,1],['p',5,3],['K',7,7]]), 1)
    def test_last_3_4(self):
        self.assertEqual(last_3([['k',1,1],['p',6,7],['K',7,7]]), 0)
    def test_table_count(self):
        self.assertEqual(len(chess_table().table) , 8)
       
    def test_move(self):
        table = chess_table()
        table.move('1.b2-b3')
        table.move('1.e7-e5')
        table.move('2.Bc1-b2')
        table.move('2.Nb8-c6')
        table.move('3.Nb1-c3')
        table.move('3.Ng8-f6')
        table.move('4.e2-e3')
        table.move('4.Bf8-b4')
        table.move('5.Qd1-f3')
        table.move('5.a7-a6')
        table.move('0-0-0')
        table.move('6.Qd8-e7')
        table1 = [[ 0 ,0, 'k', 'r', 0 ,'b', 'n', 'r' ],[ 'p', 'b', 'p', 'p', 0 ,'p', 'p', 'p' ],[ 0 ,'p', 'n', 0, 'p', 'q', 0, 0 ],[ 0 ,'B', 0, 0, 0, 0, 0, 0 ]
                  ,[ 0, 0, 0, 0, 'P', 0, 0, 0 ],[ 'P', 0, 'N', 0, 0, 'N', 0, 0 ],[ 0 ,'P', 'P', 'P', 'Q', 'P', 'P', 'P' ],[ 'R', 0 ,'B', 0 ,'K', 0, 0, 'R' ]]        
        for i in range(8):
            for j in range(8):
                self.assertEqual(table.table[i][j],table1[i][j])
    def test_load(self):
        table = chess_table()
        table.move('1.b2-b3')
        table.move('1.e7-e5')
        table.move('2.Bc1-b2')
        table.move('2.Nb8-c6')
        table.move('3.Nb1-c3')
        table.move('3.Ng8-f6')
        table.move('4.e2-e3')
        table.move('4.Bf8-b4')
        table.move('5.Qd1-f3')
        table.move('5.a7-a6')
        table.move('0-0-0')
        table.move('6.Qd8-e7')
        table.save('test')
        table1=table.table
        table = chess_table()
        table.load('test')
        table.print_t()
        for i in range(8):
            for j in range(8):
                self.assertEqual(table.table[i][j],table1[i][j])
        
        
if __name__ == "__main__":
    unittest.main()