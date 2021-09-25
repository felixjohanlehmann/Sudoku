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
        for r in range((row//3) * 3, (row//3) * 3 + 2):
            for c in range((column//3) * 3, (column//3) * 3 + 2):
                self.candidates[r, c, self.solution[row, column] - 1] = 0
                
        #remove candidates where solution is already there
        for r in range(9):
            for c in range(9):
                if self.solution[r, c] != 0:
                    self.candidates[r, c, :] = 0


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
                    if self.solution[r, c] == 0:
                        if np.sum(self.candidates[r, c]) == 1:
                            self.solution[r, c] = np.where(self.candidates[r, c] == 1)[0][0] + 1
                            self.update_candidates(r, c)
                            updating = 1
                            
                            
            for cipher in range(9):
                # update solution if a single candidate is left in a row
                for r in range(9):
                    if np.sum(self.candidates[r, :, cipher]) == 1:
                        column_identified = np.where(self.candidates[r, :, cipher] == 1)[0][0]
                        if self.solution[r, column_identified] == 0:
                            self.solution[r, column_identified] = cipher + 1
                            self.update_candidates(r, column_identified)
                            updating = 1
                # update solution if a single candidate is left in a column
                for c in range(9):
                    if np.sum(self.candidates[:, c, cipher]) == 1:
                        row_identified = np.where(self.candidates[:, c, cipher] == 1)[0][0]
                        if self.solution[row_identified, c] == 0:
                            self.solution[row_identified, c] = cipher + 1
                            self.update_candidates(row_identified, c)
                            updating = 1    
                
                #debug: following block still buggy 
                # update solution if a single candidate is left in a quadrant
                # for index1 in range(3):
                #     for index2 in range(3):
                #         if np.sum(self.candidates[(index1 * 3):(index1 * 3) + 3,
                #                                   (index2 * 3):(index2 * 3) + 3,
                #                                   cipher]) == 1:
                #             row_identified = np.where(self.candidates[(index1 * 3):(index1 * 3) + 3,
                #                                   (index2 * 3):(index2 * 3) + 3,
                #                                   cipher] == 1)[0][0]
                            
                #             column_identified = np.where(self.candidates[(index1 * 3):(index1 * 3) + 3,
                #                                   (index2 * 3):(index2 * 3) + 3,
                #                                   cipher] == 1)[1][0] 
                #             if self.solution[row_identified, column_identified] == 0:
                #                 self.solution[row_identified, column_identified] = cipher + 1
                #                 self.update_candidates(row_identified, column_identified)
                #                 updating = 1
                            
                #debug: following block not tested yet            
                #http://www.ahr-sudoku.de/solving.php/technic/Block-Line%20Interaction
                # for r_quadrant in range(3):
                #     for c_quadrant in range(3):
                #         for row_index in range(3):
                #             if np.sum(self.candidates[r_quadrant * 3 + row_index, (c_quadrant * 3):(c_quadrant * 3 + 3), cipher]) > 1:
                #                 if np.sum(self.candidates[(r_quadrant * 3):(r_quadrant * 3 + 3), (c_quadrant * 3):(c_quadrant * 3 + 3), cipher]) == np.sum(
                #                         self.candidates[r_quadrant * 3 + row_index, (c_quadrant * 3):(c_quadrant * 3 + 3), cipher]):
                #                     if (np.sum(self.candidates[(r_quadrant * 3 + row_index), :(c_quadrant * 3), cipher]) + np.sum(
                #                             self.candidates[r_quadrant * 3 + row_index, (c_quadrant * 3 + 4):, cipher])) != 0: 
                #                         print("here1")
                #                         self.candidates[(r_quadrant * 3 + row_index), :(c_quadrant * 3), cipher] = 0
                #                         self.candidates[r_quadrant * 3 + row_index, (c_quadrant * 3 + 4):, cipher] = 0
                #                         updating = 1
                #         for column_index in range(3):
                #             if np.sum(self.candidates[(r_quadrant * 3):(r_quadrant * 3 + 3), c_quadrant * 3 + column_index, cipher]) > 1:
                #                 if np.sum(self.candidates[(r_quadrant * 3):(r_quadrant * 3 + 3), (c_quadrant * 3):(c_quadrant * 3 + 3), cipher]) == np.sum(
                #                         self.candidates[(r_quadrant * 3):(r_quadrant * 3 + 3), c_quadrant * 3 + column_index, cipher]):
                #                     if (np.sum(self.candidates[:(r_quadrant * 3), (c_quadrant * 3 + column_index), cipher]) + np.sum(
                #                             self.candidates[(r_quadrant * 3 + 4):, c_quadrant * 3 + column_index, cipher])) != 0: 
                #                         print("here2")
                #                         self.candidates[:(r_quadrant * 3), (c_quadrant * 3 + column_index), cipher] = 0
                #                         self.candidates[(r_quadrant * 3 + 4):, c_quadrant * 3 + column_index, cipher] = 0
                #                         updating = 1






matrix = np.array([[0,0,2,9,3,0,4,0,6],
               [1,0,6,0,0,0,5,3,7],
               [0,5,0,1,6,7,0,0,0],
               [6,0,0,0,0,9,0,8,0],
               [9,7,0,2,0,8,0,5,1],
               [0,4,0,5,0,0,0,0,3],
               [0,0,0,4,5,3,0,2,0],
               [5,0,1,0,0,0,7,0,8],
               [4,0,9,0,8,1,3,0,0]])

#very simple
sudoku_string1 = "407659380368012059520000461002594038000038200003267014230000875745081026906725140" #solved correctly
#simple
sudoku_string2 = "030800070200100003006035100002508017008000500390601400001980700400003001080004050" #solved correctly


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
   #print(test_sudoku.candidates)
   #print(test_sudoku.candidates[:,:,6]) 
   #print(test_sudoku.candidates[6,4,:]) 
