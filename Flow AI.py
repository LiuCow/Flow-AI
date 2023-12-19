# Final Python Original Version : 8/22/23 : Victor Liu
# Program to generate solutions for classic Flow levels using deep learning/reinforcement concepts
# In brief, the program uses PyGame for the visuals, and computes solutions to puzzles by
# calculating all reasonable solutions between the start and end points of a color within the grid,
# then slowly overlaying random solutions and choosing the most probable color in each square,
# a more precise solution is developed over many iterations

# Imports used to run necessary components of solver
import copy
import random
import pygame

# Global game grid size
size = 5

# Global variable, shows debugger print code if False
clientMode = False

""""""""""""""""""""""""""""""""
# PyGame used to visualize game
# Defines colors of game functionality
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Defines constants of game path colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Colors for the percentage texts
LIGHT_BLUE = (173, 216, 230)
LIGHT_RED = (255, 114, 118)
DARK_YELLOW = (246, 190, 0)
LIGHT_GREEN = (144, 238, 144)
LIGHT_ORANGE = (255, 213, 128)

# Defines window game size, and block size
windowSize = 800
MARGIN = 5
WIDTH = (windowSize - (MARGIN * (size + 1))) / (size)
HEIGHT = (windowSize - (MARGIN * (size + 1))) / (size)
TEXT_DISPLAY_HEIGHT = 100
WINDOW_SIZE = [windowSize, windowSize + TEXT_DISPLAY_HEIGHT]

# First creates game, then runs flow game and updates each time
# Initializes pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Sets title of pygame
pygame.display.set_caption("Flow AI")

# Sets font information
font = pygame.font.SysFont("Open Sans", 18, False, False)
boldFont = pygame.font.SysFont("Open Sans", 30, True, False)

# Fills the screen black
screen.fill(BLACK)

# Creates additional display below game
pygame.draw.rect(screen, BLACK, [0, windowSize, windowSize, TEXT_DISPLAY_HEIGHT])

# Renders game
pygame.display.flip()

# Sets boolean for if game is over
gameOver = False

# Sets clock in order for refresh rate
clock = pygame.time.Clock()

""""""""""""""""""""""""""""""""

# Class for overall flow game details
class flowGame:
    # Global color array, level point indicies
    colorsArray = ["blue", "red", "yellow", "green", "orange"]

    # Variable for displaying level of Flow
    flowLevel = 0

    # Dictionary of levels from Flow Free - Classic Pack - 5x5 (uses only 5 color levels, but can be modified for 4 colors)
    # Levels offered: 1, 3, 8, 12, 13, 14, 21, 22, 25, 28, 29
    flowLevels = {
        "pointIndexesLevel1" : [[3, 2, 3, 5], [1, 1, 2, 5], [5, 1, 4, 4], [3, 1, 2, 4], [5, 2, 4, 5]], 
        "pointIndexesLevel3" : [[3, 1, 1, 5], [3, 3, 4, 2], [1, 4, 2, 1], [4, 1, 4, 5], [4, 4, 3, 5]],
        "pointIndexesLevel8" : [[1, 1, 2, 5], [2, 4, 4, 1], [4, 2, 3, 3], [3, 5, 5, 4], [5, 1, 3, 4]],
        "pointIndexesLevel12" : [[3, 2, 2, 4], [4, 1, 1, 3], [4, 4, 5, 5], [4, 2, 5, 1], [1, 4, 5, 4]],
        "pointIndexesLevel13" : [[4, 3, 5, 5], [1, 3, 4, 5], [2, 1, 4, 1], [1, 1, 4, 4], [3, 3, 5, 1]],
        "pointIndexesLevel14" : [[5, 1, 5, 4], [4, 4, 5, 5], [4, 1, 1, 5], [3, 1, 1, 3], [2, 5, 4, 3]],
        "pointIndexesLevel21" : [[1, 5, 2, 4], [3, 2, 4, 4], [5, 2, 1, 4], [2, 2, 3, 5], [5, 3, 4, 5]],
        "pointIndexesLevel22" : [[3, 3, 4, 2], [1, 3, 2, 1], [1, 5, 2, 3], [2, 5, 5, 5], [2, 2, 3, 4]],
        "pointIndexesLevel25" : [[1, 5, 4, 4], [2, 1, 5, 1], [3, 5, 5, 4], [1, 1, 5, 3], [1, 4, 4, 3]],
        "pointIndexesLevel28" : [[2, 4, 4, 5], [2, 2, 4, 2], [1, 3, 1, 5], [2, 5, 4, 4], [1, 2, 5, 2]],
        "pointIndexesLevel29" : [[1, 4, 4, 4], [2, 2, 4, 2], [1, 5, 5, 4], [1, 1, 5, 3], [1, 2, 4, 3]]
    }

    # Gives starting and end points of a level, copy and paste from above for any level
    if clientMode: 
        flowLevel = input("Please input the level from Flow you would like to solve: ")
    else: 
        flowLevel = 1
    pointIndexesOfSelectedLevel = flowLevels["pointIndexesLevel" + str(flowLevel)]

    # Maximum path length search
    pathLengthLimit = 8

    # puzzleSolutionFound variable
    puzzleSolutionFound = False
    
    # Initialization function
    def __init__(self):
        # Creates game array grid of given size
        self.gameArray = [[0 for x in range(size)] for y in range(size)]
        # Sets entire grid to 0's
        self.setGrid()

        # Creates array used to count solutions
        self.allSolutionCountGrid = [[0 for x in range(size)] for y in range(size)]

        # Creates 5 color path objects, passes an color ID and the path length limit
        self.color1 = colorPath(1, self.pathLengthLimit)
        self.color2 = colorPath(2, self.pathLengthLimit)
        self.color3 = colorPath(3, self.pathLengthLimit)
        self.color4 = colorPath(4, self.pathLengthLimit)
        self.color5 = colorPath(5, self.pathLengthLimit)

        # Defines each color path's starting and ending points, passes the game array so it may return and update overall game array
        self.gameArray = self.color1.definePoints(self.gameArray)
        self.gameArray = self.color2.definePoints(self.gameArray)
        self.gameArray = self.color3.definePoints(self.gameArray)
        self.gameArray = self.color4.definePoints(self.gameArray)
        self.gameArray = self.color5.definePoints(self.gameArray)

        # Prints starting array and initializes pygame display
        if not clientMode: 
            print("Starting gameArray is: ")
            self.printAnyArray(self.gameArray)
        self.startingPyGamePoints()

        # Calculates each color's solution using the passed overall game array, no return
        self.color1.findPathSolutions(self.gameArray)
        self.color2.findPathSolutions(self.gameArray)
        self.color3.findPathSolutions(self.gameArray)
        self.color4.findPathSolutions(self.gameArray)
        self.color5.findPathSolutions(self.gameArray)

        iterationCount = 0
        # Iterates until solution found and while iterationCount is less than 150, goes through each color and sums 1 random solution
        while not self.puzzleSolutionFound and iterationCount < 150:
            # Allows pygame to interact with OS so window dosen't crasah
            pygame.event.get()

            # Randomly adds one random solution of each color
            self.color1.calculateSolutionCountGrid()
            self.color2.calculateSolutionCountGrid()
            self.color3.calculateSolutionCountGrid()
            self.color4.calculateSolutionCountGrid()
            self.color5.calculateSolutionCountGrid()

            # Defines the shared all solution count grid
            self.defineAllSolutionCountGrid(self.color1, self.color2, self.color3, self.color4, self.color5)

            # Increments iterationCount and updates pygame screen
            iterationCount += 1
            self.updatePyGameScreen(True, iterationCount)
            
        # Prints the total summed solutions of each color path    
        if not clientMode:
            print("\nBlue line: ")
            self.printAnyArray(self.color1.solutionCountArray)
            print("\nRed line: ")
            self.printAnyArray(self.color2.solutionCountArray)
            print("\nYellow line: ")
            self.printAnyArray(self.color3.solutionCountArray)
            print("\nGreen line: ")
            self.printAnyArray(self.color4.solutionCountArray)
            print("\nOrange line: ")
            self.printAnyArray(self.color5.solutionCountArray)    

        # Prints whether or not a solution was found
        if (self.puzzleSolutionFound):
            print("\nSolution to puzzle found! :)")
        else:
            print("\nNo solution found to puzzle :(")

    # Function that sets all values in grid to 0
    def setGrid(self):
        for y in range(len(self.gameArray)) :
            for x in range(len(self.gameArray[y])) :
                self.gameArray[y][x] = 0

    # Prints the contents of any given grid
    def printAnyArray(self, anyGameArray):
        for y in range(len(anyGameArray)) :
            for x in range(len(anyGameArray[y])) :
                print(anyGameArray[y][x], end=" ")
            print()
        print("\n\n")

    # Function that sets allSolutionCountGrid array to be filled with the ID's of the most probable color for each point
    def defineAllSolutionCountGrid(self, color1, color2, color3, color4, color5):
        for y in range(len(self.allSolutionCountGrid)) :
            for x in range(len(self.allSolutionCountGrid[y])) :
                self.allSolutionCountGrid[y][x] = self.getMostProbableColor(color1, color2, color3, color4, color5, y, x)
        
    # Compares all colors solution counts for a given point, then returns the colorID of the max solution count color
    def getMostProbableColor(self, color1, color2, color3, color4, color5, currentY, currentX):
        color1SolutionCount = color1.solutionCountArray[currentY][currentX]
        color2SolutionCount = color2.solutionCountArray[currentY][currentX]
        color3SolutionCount = color3.solutionCountArray[currentY][currentX]
        color4SolutionCount = color4.solutionCountArray[currentY][currentX]
        color5SolutionCount = color5.solutionCountArray[currentY][currentX]

        maxColorSolution = max(color1SolutionCount, color2SolutionCount, color3SolutionCount, color4SolutionCount, color5SolutionCount)

        if maxColorSolution == color1SolutionCount:
            return color1.colorID
        elif maxColorSolution == color2SolutionCount:
            return color2.colorID
        elif maxColorSolution == color3SolutionCount:
            return color3.colorID
        elif maxColorSolution == color4SolutionCount:
            return color4.colorID
        elif maxColorSolution == color5SolutionCount:
            return color5.colorID

    # Function that displays the starting grid points
    def startingPyGamePoints(self):
        # In range of the entire game array
        for row in range(size):
            for column in range(size):
                # Originally set to black, and if array are certain values, then change color
                color = WHITE
                if self.gameArray[row][column] == 1:
                    color = BLUE
                elif self.gameArray[row][column] == 2:
                    color = RED
                elif self.gameArray[row][column] == 3:
                    color = YELLOW
                elif self.gameArray[row][column] == 4:
                    color = GREEN
                elif self.gameArray[row][column] == 5:
                    color = ORANGE

                # Draws colored rectangles in respective spots with the color determined above
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        pygame.display.flip()
        clock.tick(8)

    # Function that returns game status as a string
    def getGameStatus(self):
        if self.puzzleSolutionFound == True:
            return "Solution Found!"
        elif self.puzzleSolutionFound == False:
            return "No Solution Found"

    # Function that runs the recursive colorPathCheck function for each individual color
    def puzzleSolvedCheck(self):
        # Runs color path checkers
        self.color1.colorPathCheck(self.color1.startingXPosition, self.color1.startingYPosition, self.allSolutionCountGrid, 0, 0)
        self.color2.colorPathCheck(self.color2.startingXPosition, self.color2.startingYPosition, self.allSolutionCountGrid, 0, 0)
        self.color3.colorPathCheck(self.color3.startingXPosition, self.color3.startingYPosition, self.allSolutionCountGrid, 0, 0)
        self.color4.colorPathCheck(self.color4.startingXPosition, self.color4.startingYPosition, self.allSolutionCountGrid, 0, 0)
        self.color5.colorPathCheck(self.color5.startingXPosition, self.color5.startingYPosition, self.allSolutionCountGrid, 0, 0)

        # Gets the status of each color
        color1Status = self.color1.colorPathFound
        color2Status = self.color2.colorPathFound
        color3Status = self.color3.colorPathFound
        color4Status = self.color4.colorPathFound
        color5Status = self.color5.colorPathFound

        # If all colors are solved, set puzzleSolutionFound to true which will stop solver
        if (color1Status and color2Status and color3Status and color4Status and color5Status):
            self.puzzleSolutionFound = True

    # Function that repeadily updates the board data
    def updatePyGameScreen(self, updatingIteration, iterationCount): 
        # In range of the entire game array
        for row in range(size):
            for column in range(size):
                # Originally set to black, and if array are certain values, then change color
                color = WHITE
                if self.allSolutionCountGrid[row][column] == 1:
                    color = BLUE
                elif self.allSolutionCountGrid[row][column] == 2:
                    color = RED
                elif self.allSolutionCountGrid[row][column] == 3:
                    color = YELLOW
                elif self.allSolutionCountGrid[row][column] == 4:
                    color = GREEN
                elif self.allSolutionCountGrid[row][column] == 5:
                    color = ORANGE

                # Draws colored rectangles in respective spots with the color determined above
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

                if not clientMode: 
                    # Calculates the actual percentages of solution grid
                    bluePercentage = str(round(self.color1.solutionCountArray[row][column] / self.color1.totalRandomSolutionsSummed, 2))
                    redPercentage = str(round(self.color2.solutionCountArray[row][column] / self.color2.totalRandomSolutionsSummed, 2))
                    yellowPercentage = str(round(self.color3.solutionCountArray[row][column] / self.color3.totalRandomSolutionsSummed, 2))
                    greenPercentage = str(round(self.color4.solutionCountArray[row][column] / self.color4.totalRandomSolutionsSummed, 2))
                    orangePercentage = str(round(self.color5.solutionCountArray[row][column] / self.color5.totalRandomSolutionsSummed, 2))

                    # Renders font in order to draw text into surface (paired with screen.blit)
                    blueText =  boldFont.render(bluePercentage, True, LIGHT_BLUE)
                    redText =  boldFont.render(redPercentage, True, LIGHT_RED)
                    yellowText = boldFont.render(yellowPercentage, True, DARK_YELLOW)
                    greenText =  boldFont.render(greenPercentage, True, LIGHT_GREEN)
                    orangeText = boldFont.render(orangePercentage, True, LIGHT_ORANGE)

                    # Prints the percentages onto the blocks
                    screen.blit(blueText, [(MARGIN + WIDTH) * column + MARGIN + WIDTH / 2.5, (MARGIN + HEIGHT) * row + MARGIN * 5])
                    screen.blit(redText, [(MARGIN + WIDTH) * column + MARGIN + WIDTH / 2.5, (MARGIN + HEIGHT) * row + MARGIN * 10])
                    screen.blit(yellowText, [(MARGIN + WIDTH) * column + MARGIN + WIDTH / 2.5, (MARGIN + HEIGHT) * row + MARGIN * 15])
                    screen.blit(greenText, [(MARGIN + WIDTH) * column + MARGIN + WIDTH / 2.5, (MARGIN + HEIGHT) * row + MARGIN * 20])
                    screen.blit(orangeText, [(MARGIN + WIDTH) * column + MARGIN + WIDTH / 2.5, (MARGIN + HEIGHT) * row + MARGIN * 25])

        # If we are updating with each iteration
        if updatingIteration:
            # Runs puzzle checker
            self.puzzleSolvedCheck()

            # Redraws display block
            pygame.draw.rect(screen, BLACK, [0, windowSize, windowSize, TEXT_DISPLAY_HEIGHT])

            # Creates and displays text of the game
            levelText = font.render("Flow Free Classic Pack - Level  " + str(self.flowLevel), True, WHITE)
            screen.blit(levelText, [300, windowSize + (TEXT_DISPLAY_HEIGHT / 2) - 30])       

            # Creates and displays text of the game
            gameText = font.render("Puzzle Status: " + self.getGameStatus(), True, WHITE)
            screen.blit(gameText, [305, windowSize + (TEXT_DISPLAY_HEIGHT / 2)])

            if not clientMode: 
                # Creates and displays text of the current iteration
                iterationText = font.render("Iteration: " + str(iterationCount), True, WHITE)
                screen.blit(iterationText, [720, windowSize])

                # Creates and displays all five color path's statuses
                color1StatusText = font.render("Blue: " + str(self.color1.colorPathFound), True, self.color1.getStatusColor())
                color2StatusText = font.render("Red: " + str(self.color2.colorPathFound), True, self.color2.getStatusColor())
                color3StatusText = font.render("Yellow: " + str(self.color3.colorPathFound), True, self.color3.getStatusColor())
                color4StatusText = font.render("Green: " + str(self.color4.colorPathFound), True, self.color4.getStatusColor())
                color5StatusText = font.render("Orange: " + str(self.color5.colorPathFound), True, self.color5.getStatusColor())

                screen.blit(color1StatusText, [5, windowSize + (18 * (self.color1.colorID - 1))])
                screen.blit(color2StatusText, [5, windowSize + (18 * (self.color2.colorID - 1))])
                screen.blit(color3StatusText, [5, windowSize + (18 * (self.color3.colorID - 1))])
                screen.blit(color4StatusText, [5, windowSize + (18 * (self.color4.colorID - 1))])
                screen.blit(color5StatusText, [5, windowSize + (18 * (self.color5.colorID - 1))])         

        # Updates pygame display at a maximum rate of 8 frames per second
        pygame.display.flip()
        clock.tick(8)

# Class for colorPath, child class of flowGame
class colorPath(flowGame):
    # Initialilzation function, takes 2 arguments of colorID and pathLengthLimit
    # Sets colorID, goalColorID, pathLengthLimit, defines goalColorID, etc. also sets entire solutionCountArray to 0
    def __init__(self, colorID, pathLengthLimit):
        # All variables, arrays here are specific to this colorPath object, they are not shared by all objects of the class
        self.colorID = colorID
        self.goalColorID = self.colorID + 0.1
        self.pathLengthLimit = pathLengthLimit
        self.arrayOfPathSolutions = []
        self.colorPathFound = False

        self.combinationsCheckedForPath = 0
        self.solutionsFoundForPath = 0

        self.startingXPosition = 0
        self.startingYPosition = 0
        self.endingXPosition = 0
        self.endingYPosition = 0

        self.solutionCountArray = [[0 for x in range(size)] for y in range(size)]
        self.totalRandomSolutionsSummed = 0

        for y in range(len(self.solutionCountArray)) :
            for x in range(len(self.solutionCountArray[y])) :
                self.solutionCountArray[y][x] = 0

    # Function called after colorPath objects created, used to set 2 new points
    def definePoints(self, gameArray): 
        gameArray = self.setNewPoint(gameArray, 1)
        gameArray = self.setNewPoint(gameArray, 2)
        
        return gameArray

    # Function that takes input to set the starting and ending points of a color
    def setNewPoint(self, gameArray, pointID):
        # columnInput = input("Enter column for ", super().colorsArray[self.colorID - 1], ": ")
        # rowInput = input("Enter row for", super().colorsArray[self.colorID - 1], ": ")

        # column = int(columnInput) - 1
        # row = int(rowInput) - 1

        # NOTE row and column are inverted when inputting
        # gameArray[row][column] = self.colorID

        if (pointID == 1):
            # self.startingXPosition = column
            # self.startingYPosition = row
            self.startingXPosition = super().pointIndexesOfSelectedLevel[self.colorID - 1][0] - 1
            self.startingYPosition = super().pointIndexesOfSelectedLevel[self.colorID - 1][1] - 1
            gameArray[self.startingYPosition][self.startingXPosition] = self.colorID
        if (pointID == 2):
            # self.endingXPosition = column
            # self.endingYPosition = row
            self.endingXPosition = super().pointIndexesOfSelectedLevel[self.colorID - 1][2] - 1
            self.endingYPosition = super().pointIndexesOfSelectedLevel[self.colorID - 1][3] - 1
            gameArray[self.endingYPosition][self.endingXPosition] = self.colorID

        return gameArray
    
    # Function that is called to find the solutions for a given color
    def findPathSolutions(self, gameArray):
        # Prints the starting grid and the starting and ending points of the color
        if not clientMode:
            print("Current color is", super().colorsArray[self.colorID - 1])
            print("startingX, startingY: (", self.startingXPosition + 1, ",", self.startingYPosition + 1, ")")
            print("endingX, endingY: (", self.endingXPosition + 1, ",", self.endingYPosition + 1, ")")
            print("Depth limit is:", self.pathLengthLimit)
            print("Color path ID is:", self.colorID, " and Goal Color path ID is:", self.goalColorID)
        

        # Sets ending point to the goalColorID so the searcher can identify when it has reached its target
        gameArray[self.endingYPosition][self.endingXPosition] = self.goalColorID

        # newBlock function called to brute force determine all solutions
        self.newBlock(gameArray, self.startingYPosition, self.startingXPosition, 0)

        # Prints total solutions found for the color
        if not clientMode:
            print("Total solutions for the", super().colorsArray[self.colorID - 1]," line were: ", self.solutionsFoundForPath, " while the total combinations checked were ", self.combinationsCheckedForPath, "\n\n")
        
        # Resets end point to regular colorID
        gameArray[self.endingYPosition][self.endingXPosition] = self.colorID

    # Recursive function that brute force determines all path solutions
    def newBlock(self, gameArray, temporaryYPosition, temporaryXPosition, currentPathLength):
        # Allows pygame to interact with OS so window dosen't crasah
        pygame.event.get()

        #print("Combinations checked: ", self.combinationsCheckedForPath, "\n Current path length: ", currentPathLength)
        # First test if the given point is adjacent to end point, if so no need to add another block to path and end (minimize redundancy and time) 
        if self.testGameArray(gameArray, temporaryYPosition, temporaryXPosition):
            print("", end = "")
        # Else, if current block isn't adjacent to end point, then
        else:
            # Save current block (to reset to as path finder explores), takes copy of current array
            resetGameArray = copy.deepcopy(gameArray)

            # For all 4 possible moves, do x
            for box in range(4) :
                # Reset game array to the last known block before exploration, also resets currentXPosition currentYPosition variables
                gameArray = copy.deepcopy(resetGameArray)
                currentXPosition = temporaryXPosition
                currentYPosition = temporaryYPosition
                callNewBlock = False
                # For each iteration, check if exploration block is a valid block via function, and only if so explore there 
                if box == 0 and self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength): 
                    gameArray[currentYPosition + 1][currentXPosition] = self.colorID
                    currentYPosition += 1
                    callNewBlock = True
                elif box == 1 and self.checkValidBlock(gameArray, currentYPosition -1, currentXPosition, currentPathLength):
                    gameArray[currentYPosition - 1][currentXPosition] = self.colorID
                    currentYPosition -= 1
                    callNewBlock = True
                elif box == 2 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength):
                    gameArray[currentYPosition][currentXPosition + 1] = self.colorID
                    currentXPosition += 1
                    callNewBlock = True
                elif box == 3 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength):
                    gameArray[currentYPosition][currentXPosition - 1] = self.colorID
                    currentXPosition -= 1
                    callNewBlock = True
                else:
                    continue
                # After all for statements, recursive function calls itself to explore new block if callNewBlock is true (both if statements ran true)
                if callNewBlock:
                    self.newBlock(gameArray, currentYPosition, currentXPosition, currentPathLength + 1)

    # Checks if the next block is avaiable 
    def checkValidBlock(self, gameArray, yPosition, xPosition, currentPathLength):
        # Checks that new block is within grid bounds, within depth bounds, newBlock is empty, and calls checkAdjacentBlocks to check adjacent blocks
        #print("current yposotion and xposition are: ", yPosition, ", ", xPosition)
        #print("checkwithinBounds returns: ")
        #print("currentPathLength and self.pathLengthLimit: ", currentPathLength, " and ", self.pathLengthLimit)
        #print("gamearray[y][x], ", gameArray[yPosition][xPosition])
        #print("self.checkAdjacentBlocks returns: ", str(self.checkAdjacentBlocks(gameArray, yPosition, xPosition)))
        #print("The exploration block that is being checked if valid is y and x: (", yPosition, ", ", xPosition, ")")

        if self.checkWithinBounds(yPosition, xPosition) and \
        currentPathLength < self.pathLengthLimit and \
        gameArray[yPosition][xPosition] == 0 and \
        self.checkAdjacentBlocks(gameArray, yPosition, xPosition):
            # Returns true if all checks are good
            return True
        else:
            # Function returns false if any checks are bad
            return False

    # Checks if a given block is within bounds of grid
    def checkWithinBounds(self, yPosition, xPosition):
        # Assures no out of bounds or index errors, just makes sure positions are within bounds
        #print("current yposotion and xposition are: ", yPosition, ", ", xPosition)
        if (yPosition < size and yPosition >= 0) and (xPosition < size and xPosition >= 0):
            #print(" ran true ")
            return True
        else:
            #print(" ran faslse ")
            return False
        
    # Checks if new block is a valid block by assuring that only one adjascent block is path
    def checkAdjacentBlocks(self, gameArray, yPosition, xPosition):
        numberOfAdjacentBlocks = 0
        #print("current yposotion and xposition are: ", yPosition, ", ", xPosition)
        # Checks each adjacent block, increments if adjacent block is own path and is not the end point
        if self.checkWithinBounds(yPosition + 1, xPosition) and gameArray[yPosition + 1][xPosition] == self.colorID and gameArray[yPosition + 1][xPosition] != self.goalColorID:
            numberOfAdjacentBlocks += 1
        if self.checkWithinBounds(yPosition - 1, xPosition) and gameArray[yPosition - 1][xPosition] == self.colorID and gameArray[yPosition - 1][xPosition] != self.goalColorID:
            numberOfAdjacentBlocks += 1 
        if self.checkWithinBounds(yPosition, xPosition + 1) and gameArray[yPosition][xPosition + 1] == self.colorID and gameArray[yPosition][xPosition + 1] != self.goalColorID:
            numberOfAdjacentBlocks += 1
        if self.checkWithinBounds(yPosition, xPosition - 1) and gameArray[yPosition][xPosition - 1] == self.colorID and gameArray[yPosition][xPosition - 1] != self.goalColorID:
            numberOfAdjacentBlocks += 1         

        # Function returns true if only one adjacent block, else returns false
        if numberOfAdjacentBlocks == 1:
            return True
        else: 
            return False 
        
    # Function used to test if current block is adjascent to end point, returns boolean
    def testGameArray(self, gameArray, currentYPosition, currentXPosition):
        # Increments the combinations checked for a given color
        self.combinationsCheckedForPath += 1

        # Checks for four scenarios that one adjascent block is end point, if true, then 
        if (currentYPosition + 1 < size and gameArray[currentYPosition + 1][currentXPosition] == self.goalColorID) or \
            (currentYPosition - 1 >= 0 and gameArray[currentYPosition - 1][currentXPosition] == self.goalColorID) or \
            (currentXPosition + 1 < size and gameArray[currentYPosition][currentXPosition + 1] == self.goalColorID) or \
            (currentXPosition - 1 >= 0 and gameArray[currentYPosition][currentXPosition - 1] == self.goalColorID):
        
            # Increment solutions found for given color path
            self.solutionsFoundForPath += 1
            # Takes a copy of the current solution array
            currentSolutionArray = copy.deepcopy(gameArray)
            # Resets the end point value (currentl set to goalColorID ex. 1.1) back to original color ID like 1
            currentSolutionArray[self.endingYPosition][self.endingXPosition] = self.colorID
            # Stores the current solution array to the colors arrayOfPathSolutions array
            self.arrayOfPathSolutions.append(currentSolutionArray)
            # Returns true
            return True
        # Otherwise, if current block is not adjacent to end block then 
        else :
            # Return false
            return False

    # Function that when called, chooses one random solution grid for that color/object, and copies that object's specific solution path to it's solutionCountArray by incrementing all indexes of the path
    def calculateSolutionCountGrid(self):
        # Increments the total number of randomSolutionsSummed variable
        self.totalRandomSolutionsSummed += 1
        # Calculates a random index between 0 and the length of the array that holds all solution arrays of the color path
        randomIndex = random.randint(0, len(self.arrayOfPathSolutions) - 1)
        # With the random index, grabs one of the random solution arrays
        randomSolution = self.arrayOfPathSolutions[randomIndex]

        # For each point, if the value at that point matches the colorID (is a part of the given solution), then increment the same point in the shared SolutionCountArray
        for y in range(len(randomSolution)) :
            for x in range(len(randomSolution[y])) :
                if randomSolution[y][x] == self.colorID:
                    self.solutionCountArray[y][x] += 1

    # Recursive function that simply checks if a color path is solved            
    def colorPathCheck(self, currentXPosition, currentYPosition, allSolutionCountGrid, lastMoveID, count):
        # Increment count, reassures that recursive function is not indefinite
        count += 1
        # Base case, if the function is still running and current grid position equals ending grid point, then puzzle is solved 
        if (currentXPosition == self.endingXPosition and currentYPosition == self.endingYPosition):
            # If our current grid position reaches our ending grid point, then path is successful and we set colorPathFound to true
            self.colorPathFound = True
        # Break clause of recursive function, prevents going forever
        elif (count <= self.pathLengthLimit + 1):
            # Check each adjascent block, if any is of the same color then call function again after changing current grid position, lastMoveID assures the movement is not opposite to last move (becomes stuck)
            if (currentXPosition + 1 < size and allSolutionCountGrid[currentYPosition][currentXPosition + 1] == self.colorID and lastMoveID != 2):
                self.colorPathCheck(currentXPosition + 1, currentYPosition, allSolutionCountGrid, 1, count)
            elif (currentXPosition - 1 >= 0 and allSolutionCountGrid[currentYPosition][currentXPosition - 1] == self.colorID and lastMoveID != 1):
                self.colorPathCheck(currentXPosition - 1, currentYPosition, allSolutionCountGrid, 2, count)
            elif (currentYPosition + 1 < size and allSolutionCountGrid[currentYPosition + 1][currentXPosition] == self.colorID and lastMoveID != 4):
                self.colorPathCheck(currentXPosition, currentYPosition + 1, allSolutionCountGrid, 3, count)
            elif (currentYPosition - 1 >= 0 and allSolutionCountGrid[currentYPosition - 1][currentXPosition] == self.colorID and lastMoveID != 3):
                self.colorPathCheck(currentXPosition, currentYPosition - 1, allSolutionCountGrid, 4, count)
            else:
                # If not valid adjascent block / move, then set colorPathFound to be false
                self.colorPathFound = False

    # Returns a color based on the status of a given color path 
    def getStatusColor(self):
        if self.colorPathFound:
            return LIGHT_GREEN
        else: 
            return LIGHT_RED

""""""""""""""""""""""""""""""""

# Creates newGame object, runs game
newGame = flowGame()

""""""""""""""""""""""""""""""""
# While the game is not over
while not gameOver:
    # onEvent in pyGame, if quit button is hit, then exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    # Repeatidly calls updatePyGameScreen() function while game runs
    newGame.updatePyGameScreen(False, 0)

    # Updates the screen
    # pygame.display.flip()
    # clock.tick(60)

# Terminates once quit button is hit
pygame.quit()

""""""""""""""""""""""""""""""""