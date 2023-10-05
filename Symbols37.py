import random
import os
#############
##Symbols37##
#############
import time
#############
##Symbols37##
#############


def Main():
    Again = "y"
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        #############
        ##Symbols37##
        #############
        Winner = MyPuzzle.AttemptPuzzle()
        if Winner == "Draw!":
            print(f"Puzzle finished. Game was a Draw!")
        else:
            print(f"Puzzle finished. Winner is {Winner}!")
        #############
        ##Symbols37##
        #############
        Again = input("Do another puzzle? ").lower()


class Puzzle():
    def __init__(self, *args):
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            #############
            ##Symbols37##
            #############
            self.__Score1 = 0
            self.__Score2 = 0
            self.__SymbolsLeft = 5
            #############
            ##Symbols37##
            #############
            self.__GridSize = args[0]
            self.__Grid = []
            #############
            ##Symbols37##
            #############
            self.__Grid2 = []
            #############
            ##Symbols37##
            #############
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                    #############
                    ##Symbols37##
                    #############
                    D = Cell()
                    #############
                    ##Symbols37##
                    #############
                else:
                    C = BlockedCell()
                    #############
                    ##Symbols35##
                    #############
                    D = BlockedCell()
                    #############
                    ##Symbols35##
                    #############
                self.__Grid.append(C)
                #############
                ##Symbols35##
                #############
                self.__Grid2.append(D)
                #############
                ##Symbols35##
                #############
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")


    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip()) #Set number of symbols and remove from text file
                for Count in range (1, NoOfSymbols + 1): 
                    self.__AllowedSymbols.append(f.readline().rstrip()) #Lines 2 and onwards display the allowed symbols to be placed depending on line 1 and remove from text file
                NoOfPatterns = int(f.readline().rstrip()) #Set number of possible patterns and remove from text file
                for Count in range(1, NoOfPatterns + 1): 
                    Items = f.readline().rstrip().split(",") #Split patterns into 2 by comma
                    P = Pattern(Items[0], Items[1]) #items[0] will be the symbol, items[1] will be the pattern sequence
                    self.__AllowedPatterns.append(P) #append to allowed patterns
                self.__GridSize = int(f.readline().rstrip()) #grid size set to line after pattern sequences (number on each axis)
                for Count in range (1, self.__GridSize * self.__GridSize + 1): #loop from 1 to (grid_size^2 +1) to create (gridSize^2) number of cells
                    Items = f.readline().rstrip().split(",") #split lines by comma
                    if Items[0] == "@": #if the items[0] is @, create a blocked cell and append to blocked cell
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell() #else, create a normal cell with no symbol
                        C.ChangeSymbolInCell(Items[0]) #change symbol in cell to the items[0], if blank will create a '-'
                        for CurrentSymbol in range(1, len(Items)): #loop from 1 to length of items (usually 1 or 2). Start at 1 so that will allow the second in the row to be added to not allowed list
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol]) #if there are 2 char in a row, append the second to not allowed list of symbols for that cell
                            #if there is 1 char in the row, no unallowed symbols will be added to that cell as looping 1 to 1 will not produce any loops
                        self.__Grid.append(C) #add that cell to the grid list
                self.__Score = int(f.readline().rstrip()) #score will be set to penultimate line
                self.__SymbolsLeft = int(f.readline().rstrip()) #symbols left will be the last line
        except:
            print("Puzzle not loaded")


    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            #############
            ##Symbols37##
            #############
            #User 1 go
            self.DisplayPuzzle1()
            print("USER 1 PUZZLE")
            print("User 1 Score: " + str(self.__Score1))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            CurrentCell = self.__GetCell1(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern1(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score1 += AmountToAddToScore
            self.DisplayPuzzle1()
            print("User 2 Score: " + str(self.__Score1))
            time.sleep(1)
            
            #User 2 go
            self.DisplayPuzzle2()
            print("USER 2 PUZZLE")
            print("User 2 Score: " + str(self.__Score2))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            CurrentCell = self.__GetCell2(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern2(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score2 += AmountToAddToScore
            self.DisplayPuzzle2()
            print("User 2 Score: " + str(self.__Score2))
            time.sleep(1)
            self.__SymbolsLeft -=1
            #############
            ##Symbols37##
            #############


            if self.__SymbolsLeft == 0:
                Finished = True


        #############
        ##Symbols37##
        #############
        print()
        self.DisplayPuzzle1()
        print("USER 1 PUZZLE")
        print("User 1 Score: " + str(self.__Score2))
        print()

        print()
        self.DisplayPuzzle2()
        print("USER 2 PUZZLE")
        print("User 2 Score: " + str(self.__Score2))
        print()

        if self.__Score1 > self.__Score2:
            return "User 1"
        elif self.__Score2 > self.__Score1:
            return "User 2"
        else:
            return "Draw!"

    def __GetCell1(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()
    
    def __GetCell2(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid2[Index]
        else:
            raise IndexError()
        

    def CheckforMatchWithPattern1(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell1(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell1(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell1(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell1(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell1(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell1(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell1(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell1(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell1(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell1(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell1(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell1(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0
    
    def CheckforMatchWithPattern2(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell2(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell2(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell2(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell2(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell2(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell2(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell2(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell2(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell2(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell2(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell2(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell2(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0
    
        #############
        ##Symbols37##
        #############

    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol
    

    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line
    
        #############
        ##Symbols37##
        #############
    def DisplayPuzzle1(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())


    def DisplayPuzzle2(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid2)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid2[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())
        #############
        ##Symbols37##
        #############

class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString


    def MatchesPattern(self, PatternString, SymbolPlaced):
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True
    

    def GetPatternSequence(self):
      return self.__PatternSequence
    

class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []


    def GetSymbol(self):
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    

    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False
        

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol


    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True
    

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

        
    def UpdateCell(self):
        pass


class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"


    def CheckSymbolAllowed(self, SymbolToCheck):
        return False
    

if __name__ == "__main__":
    Main()
