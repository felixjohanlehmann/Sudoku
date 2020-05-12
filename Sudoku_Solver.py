import numpy as np

class Sudoku:
    def __init__(self, input_matrix):
        self.input_matrix = input_matrix
        self.solution = self.input_matrix.copy()
        self.candidates = np.ones((9,9,9))
        
        #initial update of all candidates
        self.update_all_candidates()
        
        #try to solve sudoku
        self.solve_sudoku()
    
    
    def update_candidates(self, row, column):          
        #remove candidate from same column            
        for r in range(9):
            self.candidates[r, column, self.solution[row, column] - 1] = 0
        
        #remove candidate from same row
        for c in range(9):
            self.candidates[row, c, self.solution[row, column] - 1] = 0
            
        #remove candidate from same quadrant            
        for r in range((row//3) * 3, (row//3) * 3 + 3):
            for c in range((column//3) * 3, (column//3) * 3 + 3):
                self.candidates[r, c, self.solution[row, column] - 1] = 0


    def update_all_candidates(self):
        for r in range(9):
            for c in range(9):
                if self.solution[r, c] != 0:
                    self.update_candidates(r, c)  

                    
    def solve_sudoku(self):
        # loop till solution is not changed any more 
        updating = 1
        while updating > 0:
            updating = 0
            # update solution if a single candidate is left for any field
            for r in range(9):
                for c in range(9):
                    if self.solution[r,c] == 0:
                        if np.sum(self.candidates[r,c]) == 1:
                            self.solution[r,c] = np.where(self.candidates[r,c] == 1)[0][0] + 1
                            self.update_candidates(r,c)
                            updating = 1
                            
                            
            # update solution if a single candidate is left in a row or column
            for cipher in range(9):
                for r in range(9):
                    if np.sum(self.candidates[r,:,cipher]) == 1:
                        column_identified = np.where(self.candidates[r,:,cipher] == 1)[0][0]
                        if self.solution[r,column_identified] == 0:
                            self.solution[r,column_identified] = cipher + 1
                            self.update_candidates(r,column_identified)
                            updating = 1
                for c in range(9):
                    if np.sum(self.candidates[:,c,cipher]) == 1:
                        row_identified = np.where(self.candidates[:,c,cipher] == 1)[0][0]
                        if self.solution[row_identified,c] == 0:
                            self.solution[row_identified,c] = cipher + 1
                            self.update_candidates(row_identified,c)
                            updating = 1    
                # update solution if a single candidate is left in a quadrant
                for index1 in range(3):
                    for index2 in range(3):
                        if np.sum(self.candidates[(index1 * 3):(index1 * 3) + 3,
                                                  (index2 * 3):(index2 * 3) + 3,
                                                  cipher]) == 1:
                            row_identified = np.where(self.candidates[(index1 * 3):(index1 * 3) + 3,
                                                  (index2 * 3):(index2 * 3) + 3,
                                                  cipher] == 1)[0][0]
                            column_identified = np.where(self.candidates[(index1 * 3):(index1 * 3) + 3,
                                                  (index2 * 3):(index2 * 3) + 3,
                                                  cipher] == 1)[0][1] 
                            if self.solution[row_identified,column_identified] == 0:
                                self.solution[row_identified,column_identified] = cipher + 1
                                self.update_candidates(row_identified,column_identified)
                                updating = 1
               







matrix = np.array([[0,0,2,9,3,0,4,0,6],
               [1,0,6,0,0,0,5,3,7],
               [0,5,0,1,6,7,0,0,0],
               [6,0,0,0,0,9,0,8,0],
               [9,7,0,2,0,8,0,5,1],
               [0,4,0,5,0,0,0,0,3],
               [0,0,0,4,5,3,0,2,0],
               [5,0,1,0,0,0,7,0,8],
               [4,0,9,0,8,1,3,0,0]])

sudoku_string1 = "504670103000000004090008670007800009005030800800006300083900050400000000106023708"
sudoku_string2 = "000000080097000006800500329020301040060020070030608090386005004100000930040000000"

def string_to_matrix(sudoku_as_simple_string):
    assert len(sudoku_as_simple_string) == 81
    sudoku_as_list = []
    for cipher in sudoku_as_simple_string:
        sudoku_as_list.append(int(cipher))
    chunks = [sudoku_as_list[x:x+9] for x in range(0, len(sudoku_as_list), 9)]    
    sudoku_matrix = np.array(chunks)    
    return sudoku_matrix

if __name__ == '__main__':    
   #test_sudoku = Sudoku(matrix)
   test_sudoku = Sudoku(string_to_matrix(sudoku_string2))
   print(test_sudoku.input_matrix)
   print(test_sudoku.solution)
