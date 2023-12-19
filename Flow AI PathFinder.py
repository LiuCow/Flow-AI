# Final Pathfinder Version : 7/20/23 : Victor Liu
# Simply a supplamental program for the main Flow AI 
# Test program used to explore path finding algorithms and optimizations
# in order to efficiently compute paths to individual colors in Flow
# Optimization methods include, assuring within bounds, limiting length, 
# checking for an empty block, no simplifiable paths (multiple adjacent blocks),
# and avoiding dead end scenarios where no solution could exist

# Imports for program
import copy
import random
import pygame

# Global game grid size
size = 8

""""""""""""""""""""""""""""""""
   
# PyGame used to visualize game
# Defines colors of game functionality
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Defines constants of game path colors
BLUE = (0, 0, 255)

# Colors for the percentage texts
LIGHT_BLUE = (85, 145, 255)
LIGHT_RED = (255, 114, 118)
LIGHT_GREEN = (144, 238, 144)

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

# Sets icon of pygame
# flowIcon = pygame.image.load('flowIcon.png')
# pygame.display.set_icon(flowIcon)

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
    colorsArray = ["blue"]

    # Gives starting and end points of a level, copy and paste from above for any level
    # Small 5x5 grid [[4, 3, 5, 5]]
    # Large 8x8 grid [[4, 2, 7, 7]]
    # Large 8x8 grid [[3, 3, 8, 4]]
    pointIndexesOfSelectedLevel = [[4, 1, 6, 6]]

    # Maximum path length search
    pathLengthLimit = 100

    # puzzleSolutionFound variable
    puzzleSolutionFound = False
    
    # Initialization function
    def __init__(self):
        # Creates game array grid of given size
        self.gameArray = [[0 for x in range(size)] for y in range(size)]
        # Sets entire grid to 0's
        self.setGrid()

        # Creates 5 color path objects, passes an color ID and the path length limit
        self.color1 = colorPath(1, self.pathLengthLimit)

        # Defines each color path's starting and ending points, passes the game array so it may return and update overall game array
        self.gameArray = self.color1.definePoints(self.gameArray)
        
        print("Starting gameArray is: ")
        self.printAnyArray(self.gameArray)
        self.startingPyGamePoints(self.gameArray)

        # Calculates each color's solution using the passed overall game array, no return
        self.color1.findPathSolutions(self.gameArray)
            
        # Prints the total summed solutions of each color path    
        #print("\nBlue line: ")
        #self.printAnyArray(self.color1.solutionCountArray)   

    # Function that sets all values in grid to 0
    def setGrid(self):
        for y in range(len(self.gameArray)) :
            for x in range(len(self.gameArray[y])) :
                self.gameArray[y][x] = 0

    # Prints the contents of any given grid
    def printAnyArray(self, anyGameArray):
        for y in range(len(anyGameArray)) :
            for x in range(len(anyGameArray[y])) :
                if (anyGameArray[y][x] == 0):
                    print(anyGameArray[y][x], end="0 ")
                elif anyGameArray[y][x] - 10 < 0:
                    print("0", anyGameArray[y][x], end=" ", sep = "")
                else:
                    print(anyGameArray[y][x], end=" ")
            print()
        print("\n\n")

    # Function that displays the starting grid points
    def startingPyGamePoints(self, startingArray):
        # In range of the entire game array
        for row in range(size):
            for column in range(size):
                # Originally set to black, and if array are certain values, then change color
                color = WHITE

                if startingArray[row][column] == 1:
                    color = BLUE

                # Draws colored rectangles in respective spots with the color determined above
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
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
        self.lastMoveID = 0

        #self.pathMovement = [4, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1]
        self.pathMovement = []

        self.combinationsCheckedForPath = 0
        self.solutionsFoundForPath = 0

        self.startingXPosition = 0
        self.startingYPosition = 0
        self.endingXPosition = 0
        self.endingYPosition = 0

        self.checkedInvalidBlocks = [[0 for x in range(size)] for y in range(size)]

        for y in range(len(self.checkedInvalidBlocks)) :
            for x in range(len(self.checkedInvalidBlocks[y])) :
                self.checkedInvalidBlocks[y][x] = 0

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

        # NOTE THAT ROW AND COLUMN ARE INVERTED WHEN INPUTTING
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
        print("Total solutions for the", super().colorsArray[self.colorID - 1]," line were: ", self.solutionsFoundForPath, " while the total combinations checked were ", self.combinationsCheckedForPath, "\n\n")
        
        # Resets end point to regular colorID
        gameArray[self.endingYPosition][self.endingXPosition] = self.colorID

    # Recursive function that brute force determines all path solutions
    def newBlock(self, gameArray, currentYPosition, currentXPosition, currentPathLength):
        # Allows pygame to interact with OS so window dosen't crasah
        pygame.event.get()

        # Update screen
        self.updatePyGameScreen(False, True, gameArray)

        # Exploration bias
        explorationBias = 1

        # Valid move found 
        validMove = False

        #print("Combinations checked: ", self.combinationsCheckedForPath, "\n Current path length: ", currentPathLength)
        # First test if the given point is adjacent to end point, if so no need to add another block to path and end (minimize redundancy and time) 
        if self.testGameArray(gameArray, currentYPosition, currentXPosition):
            print("", end = "")
        # Else, if current block isn't adjacent to end point, then
        else:
            # Random percentage chooses between exploration and going towards end (based on exploration bias)
            randomPercentage = random.randrange(1, 101)
            # If statement for moving towards end
            if randomPercentage <= (1 - explorationBias) * 100:
                print("Block #", currentPathLength + 1, " is moving towards end")
                # While validMove not found
                while not validMove:
                    # Calculate moving towards end
                    moveSelection = self.moveTowardsEnd(gameArray, currentYPosition, currentXPosition, currentPathLength)
                    # If initially valid, then set true and exit while loop and execute
                    if moveSelection == 1 or moveSelection == 2 or moveSelection == 3 or moveSelection == 4:
                        validMove = True
                    # Else, reverse reverse, get last move ID and revert steps, shorten path length by 1
                    """
                    else:
                        print("1 REVERSE REVERSE: currentYposition and currentXposition: ", currentYPosition, ", ", currentXPosition)
                        super().printAnyArray(gameArray)
                        revertMoveID = self.revertStep(gameArray, currentYPosition, currentXPosition)
                        if revertMoveID == 1:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentYPosition += 1
                        elif revertMoveID == 2:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentYPosition -= 1
                        elif revertMoveID == 3:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentXPosition += 1
                        elif revertMoveID == 4:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentYPosition -= 1
                        currentPathLength -= 1
                        print("2 REVERSE REVERSE: currentYposition and currentXposition: ", currentYPosition, ", ", currentXPosition)
                        super().printAnyArray(gameArray)
                    """
                    
            # If exploring, completley randomly choose next move
            else:
                print("\n\nBlock #", currentPathLength + 1, " is exploring randomly")
                # For all 4 possible moves, do x
                count = 0
                while not validMove:
                    # Randomly choose next move, keep choosing until valid move is found
                    # moveSelection = random.randrange(1, 5)
                    if count == 0 and len(self.pathMovement) != 0:
                        moveSelection = self.pathMovement[currentPathLength]
                        count += 1
                    else:
                        print("DEVIATED")
                        moveSelection = random.randrange(1, 5)

                    if self.lastMoveID != 2 and moveSelection == 1 and self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength, 1):
                        validMove = True
                    elif self.lastMoveID != 1 and moveSelection == 2 and self.checkValidBlock(gameArray, currentYPosition - 1, currentXPosition, currentPathLength, 2):
                        validMove = True
                    elif self.lastMoveID != 4 and moveSelection == 3 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength, 3):
                        validMove = True
                    elif self.lastMoveID != 3 and moveSelection == 4 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength, 4):
                        validMove = True
                    
                    """
                    if not self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength) and \
                    not self.checkValidBlock(gameArray, currentYPosition - 1, currentXPosition, currentPathLength) and \
                    not self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength) and \
                    not self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength):
                        revertMoveID = self.revertStep(gameArray, currentYPosition, currentXPosition)
                        if revertMoveID == 1:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentYPosition += 1
                        elif revertMoveID == 2:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentYPosition -= 1
                        elif revertMoveID == 3:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentXPosition += 1
                        elif revertMoveID == 4:
                            gameArray[currentYPosition][currentXPosition] = 0
                            currentYPosition -= 1
                        currentPathLength -= 1
                    """

            # Takes and performs the given steps based on the calcualted moveSelection
            if moveSelection == 1:
                gameArray[currentYPosition + 1][currentXPosition] = currentPathLength + 1
                currentYPosition += 1
            elif moveSelection == 2:
                gameArray[currentYPosition - 1][currentXPosition] = currentPathLength + 1
                currentYPosition -= 1
            elif moveSelection == 3:
                gameArray[currentYPosition][currentXPosition + 1] = currentPathLength + 1
                currentXPosition += 1
            elif moveSelection == 4:
                gameArray[currentYPosition][currentXPosition - 1] = currentPathLength + 1
                currentXPosition -= 1

            # Recrusive function, sends in new parameters for next block
            self.newBlock(gameArray, currentYPosition, currentXPosition, currentPathLength + 1)

    # Function that reverts adjascent block back to 0, returns grid (helps exit dead ends)
    def revertStep(self, gameArray, currentYPosition, currentXPosition):
        if self.checkWithinBounds(currentYPosition + 1, currentXPosition) and gameArray[currentYPosition + 1][currentXPosition] != 0:
            return 1
        elif self.checkWithinBounds(currentYPosition - 1, currentXPosition) and gameArray[currentYPosition - 1][currentXPosition] != 0:
            return 2
        elif self.checkWithinBounds(currentYPosition, currentXPosition + 1) and gameArray[currentYPosition][currentXPosition + 1] != 0:
            return 3
        elif self.checkWithinBounds(currentYPosition, currentXPosition - 1) and gameArray[currentYPosition][currentXPosition - 1] != 0:
            return 4

    # Function that is called to move towards end
    def moveTowardsEnd(self, gameArray, currentYPosition, currentXPosition, currentPathLength):
        pygame.event.get()
        
        # First calculates the x and y distance between current position and goal position
        xDistanceToEnd = self.endingXPosition - currentXPosition
        yDistanceToEnd = self.endingYPosition - currentYPosition

        # If x and y distances are equal, then
        if abs(yDistanceToEnd) == abs(xDistanceToEnd):
            # Randomly choose between x and y movement
            randomXOrYMovement = random.randrange(1, 3)
            # If y movement, then if positive movement, then do that, if returns false or invalid, then try negative movement, if not, then try x's
            if randomXOrYMovement == 1:
                if yDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength, 1):
                    return 1
                elif yDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition - 1, currentXPosition, currentPathLength, 2):
                    return 2
                elif xDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength, 3):
                    return 3
                elif xDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength, 4):
                    return 4
            # If x movement, then try x movement's first, if invalid then do y's
            elif randomXOrYMovement == 2:
                if xDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength, 3):
                    return 3
                elif xDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength, 4):
                    return 4
                elif yDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength, 1):
                    return 1
                elif yDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition - 1, currentXPosition, currentPathLength, 2):
                    return 2

        # Similar decision making, but moves path by choosing the to minimize the greatest distance first (if y>x then first minimize y)
        if abs(yDistanceToEnd) > abs(xDistanceToEnd):
            if yDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength, 1):
                return 1
            elif yDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition - 1, currentXPosition, currentPathLength, 2):
                return 2
            elif xDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength, 3):
                return 3
            elif xDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength, 4):
                return 4

        # If x>y distance, do this
        if abs(xDistanceToEnd) > abs(yDistanceToEnd):
            if xDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition + 1, currentPathLength, 3):
                return 3
            elif xDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition, currentXPosition - 1, currentPathLength, 4):
                return 4
            elif yDistanceToEnd > 0 and self.checkValidBlock(gameArray, currentYPosition + 1, currentXPosition, currentPathLength, 1):
                return 1
            elif yDistanceToEnd < 0 and self.checkValidBlock(gameArray, currentYPosition - 1, currentXPosition, currentPathLength, 2):
                return 2
        
        # Returns 5 if no valid move is found, 5 acts as a broken number (reverse ID)
        return 5

    # Checks if the next block is avaiable 
    def checkValidBlock(self, gameArray, yPosition, xPosition, currentPathLength, lastMoveID):
        # Checks that new block is within grid bounds, within depth bounds, newBlock is empty, and calls checkAdjacentBlocks to check adjacent blocks
        #print("current yposotion and xposition are: ", yPosition, ", ", xPosition)
        #print("checkwithinBounds returns: ")
        #print("currentPathLength and self.pathLengthLimit: ", currentPathLength, " and ", self.pathLengthLimit)
        #print("gamearray[y][x], ", gameArray[yPosition][xPosition])
        #print("self.checkAdjacentBlocks returns: ", str(self.checkAdjacentBlocks(gameArray, yPosition, xPosition)))

        print("The exploration block that is being checked if valid is y and x: (", yPosition, ", ", xPosition, ")")

        if self.checkWithinBounds(yPosition, xPosition) and \
        currentPathLength < self.pathLengthLimit and \
        gameArray[yPosition][xPosition] == 0 and \
        self.checkAdjacentBlocks(gameArray, yPosition, xPosition) and \
        self.checkDeadEnds(gameArray, yPosition, xPosition, lastMoveID):
            # print("Passed all other checks, checking for dead ends now: ")
            # time.sleep(1)
            # Returns true if all checks are good
            return True
        else:
            if self.checkWithinBounds(yPosition, xPosition):
                self.checkedInvalidBlocks[yPosition][xPosition] = -1

            # Function returns false if any checks are bad
            return False
        

    # Checks if new exploration block is a valid block by checking adjascent blocks and seeing if any of them result in dead ends
    def checkDeadEnds(self, gameArray, yPosition, xPosition, lastMoveID):
        # Variable to keep track of the number of dead ends
        numberOfDeadEnds = 0

        # checkDeadEndAdjacentBlocks returns true if there is a calculated dead end, so if true, increment dead ends
        if lastMoveID != 2 and self.checkWithinBounds(yPosition + 1, xPosition) and self.checkDeadEndAdjacentBlocks(gameArray, yPosition + 1, xPosition, 1):
            numberOfDeadEnds += 1
            print("PREVENTED DEAD END AT (", yPosition, ", ", xPosition, ")")
        if lastMoveID != 1 and numberOfDeadEnds == 0 and self.checkWithinBounds(yPosition - 1, xPosition) and self.checkDeadEndAdjacentBlocks(gameArray, yPosition - 1, xPosition, 2):
            numberOfDeadEnds += 1
            print("PREVENTED DEAD END AT (", yPosition, ", ", xPosition, ")")
        if lastMoveID != 4 and numberOfDeadEnds == 0 and self.checkWithinBounds(yPosition, xPosition + 1) and self.checkDeadEndAdjacentBlocks(gameArray, yPosition, xPosition + 1, 3):
            numberOfDeadEnds += 1
            print("PREVENTED DEAD END AT (", yPosition, ", ", xPosition, ")")
        if lastMoveID != 3 and numberOfDeadEnds == 0 and self.checkWithinBounds(yPosition, xPosition - 1) and self.checkDeadEndAdjacentBlocks(gameArray, yPosition, xPosition - 1, 4):
            numberOfDeadEnds += 1
            print("PREVENTED DEAD END AT (", yPosition, ", ", xPosition, ")")

        # If dead ends is not 0 (ie. one exists) then return false and exploration block check fails
        if numberOfDeadEnds != 0:
            print("Exploration block failed dead end check")
            #time.sleep(1)
            return False
        else:
            return True

    # Function soley ran, called, and used to check for dead ends in adjascent blocks of the current exploratory block check
    def checkDeadEndAdjacentBlocks(self, gameArray, yPosition, xPosition, lastMoveID):
        pygame.event.get()
        numberOfInvalidAdjacentBlocks = 0

        print("Adjacent block to exploration block: (", yPosition, ",", xPosition, "), lastMoveID was ", lastMoveID)
        
        # Change != to self.colorID once revert back to pygame draft
        # Checks each adjacent block, increments if adjacent block is out of bounds or if adjacent block is not empty and is not a goal point for another color
        #time.sleep(1)
        ### NEED TO CHANGE CONDITIONS, own color start point needs to avoid
        if not self.checkWithinBounds(yPosition + 1, xPosition) or \
            (lastMoveID != 2 and ((gameArray[yPosition + 1][xPosition] != 0 and not self.checkStartOrEndPoint(yPosition + 1, xPosition, 2)) or self.checkStartOrEndPoint(yPosition + 1, xPosition, 1))):
            print("Check 1:")
            numberOfInvalidAdjacentBlocks += 1
            print("Adjacent block to exploration block: (", yPosition, ",", xPosition, ") but the adjacent block (", yPosition + 1, ",", xPosition, ") failed the adjacetnDeadEnd check")

        #time.sleep(1)
        if not self.checkWithinBounds(yPosition - 1, xPosition) or \
            (lastMoveID != 1 and ((gameArray[yPosition - 1][xPosition] != 0 and not self.checkStartOrEndPoint(yPosition - 1, xPosition, 2)) or self.checkStartOrEndPoint(yPosition - 1, xPosition, 1))):
            print("Check 2:")
            numberOfInvalidAdjacentBlocks += 1
            print("Adjacent block to exploration block: (", yPosition, ",", xPosition, ") but the adjacent block (", yPosition - 1, ",", xPosition, ") failed the adjacetnDeadEnd check")

        #time.sleep(1)
        if not self.checkWithinBounds(yPosition, xPosition + 1) or \
            (lastMoveID != 4 and ((gameArray[yPosition][xPosition + 1] != 0 and not self.checkStartOrEndPoint(yPosition, xPosition + 1, 2)) or self.checkStartOrEndPoint(yPosition, xPosition + 1, 1))):
            print("Check 3:")
            numberOfInvalidAdjacentBlocks += 1
            print("Adjacent block to exploration block: ((", yPosition, ",", xPosition, ") but the adjacent block (", yPosition, ",", xPosition + 1, ") failed the adjacetnDeadEnd check")

        #time.sleep(1)
        if not self.checkWithinBounds(yPosition, xPosition - 1) or ((numberOfInvalidAdjacentBlocks >= 1) and \
            (lastMoveID != 3 and ((gameArray[yPosition][xPosition - 1] != 0 and not self.checkStartOrEndPoint(yPosition, xPosition - 1, 2)) or self.checkStartOrEndPoint(yPosition, xPosition - 1, 1)))):
            print("Check 4:")
            """
            print("the bounds condition: ", self.checkWithinBounds(yPosition, xPosition - 1))
            print("the numberofinvalidadjacentblocks condition: ", numberOfInvalidAdjacentBlocks >= 1)
            print("the lastmoveid condition: ", lastMoveID != 3)
            print("gamearray is != 0 condition: ", gameArray[yPosition][xPosition - 1] != 0)
            print("the end point condition: ", self.checkStartOrEndPoint(yPosition, xPosition - 1, 2))
            print("the start condition: ", self.checkStartOrEndPoint(yPosition, xPosition - 1, 1))
            """
            numberOfInvalidAdjacentBlocks += 1
            print("Adjacent block to exploration block: (", yPosition, ",", xPosition, ") but the adjacent block (", yPosition, ",", xPosition - 1, ") failed the adjacetnDeadEnd check")

        # Function returns true if only one adjacent block, else returns false
        if numberOfInvalidAdjacentBlocks >= 2:
            print("There are more than two invalid blocks adjacent to (", yPosition, ", ", xPosition, ") which is adjacent to the exploratory block (not included)")
            return True
        else: 
            return False  

    # Checks if new block is a valid block by assuring that only one adjascent block is path
    def checkAdjacentBlocks(self, gameArray, yPosition, xPosition):
        numberOfAdjacentBlocks = 0
        #print("current yposotion and xposition are: ", yPosition, ", ", xPosition)
        # Change != 0 to == to self.colorID once revert back to pygame draft (right now grid is of the block numbers not of color ID's)
        # Checks each adjacent block, increments if adjacent block is own path and is not the end point
        if self.checkWithinBounds(yPosition + 1, xPosition) and gameArray[yPosition + 1][xPosition] != 0 and gameArray[yPosition + 1][xPosition] != self.goalColorID:
            numberOfAdjacentBlocks += 1
        if self.checkWithinBounds(yPosition - 1, xPosition) and gameArray[yPosition - 1][xPosition] != 0 and gameArray[yPosition - 1][xPosition] != self.goalColorID:
            numberOfAdjacentBlocks += 1 
        if self.checkWithinBounds(yPosition, xPosition + 1) and gameArray[yPosition][xPosition + 1] != 0 and gameArray[yPosition][xPosition + 1] != self.goalColorID:
            numberOfAdjacentBlocks += 1
        if self.checkWithinBounds(yPosition, xPosition - 1) and gameArray[yPosition][xPosition - 1] != 0 and gameArray[yPosition][xPosition - 1] != self.goalColorID:
            numberOfAdjacentBlocks += 1         

        # Function returns true if only one adjacent block, else returns false
        if numberOfAdjacentBlocks == 1:
            return True
        else: 
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

    # Checks if a given point is a start or end point of a given color path
    # startOrEndID 1 means check start point, 2 means check end point, 3 means check both
    def checkStartOrEndPoint(self, yPosition, xPosition, startOrEndID):
        # print("y position and x position: ", yPosition, ", ", xPosition)
        # print("starting y position and starting x position: ", self.startingYPosition, ", ", self.startingXPosition)
        if (startOrEndID == 1) and (yPosition == self.startingYPosition and xPosition == self.startingXPosition):
            
            return True
        
        if (startOrEndID == 2) and (yPosition == self.endingYPosition and xPosition == self.endingXPosition):
            return True

        if (startOrEndID == 3) and ((yPosition == self.startingYPosition and xPosition == self.startingXPosition) or \
            (yPosition == self.endingYPosition and xPosition == self.endingXPosition)):
            return True
        
        # Base case, return false
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
            # Resets the end point value (currently set to goalColorID ex. 1.1) back to original color ID like 1
            currentSolutionArray[self.endingYPosition][self.endingXPosition] = self.colorID
            # Stores the current solution array to the colors arrayOfPathSolutions array
            self.arrayOfPathSolutions.append(currentSolutionArray)

            # Update and shows current solution as long as its a solution (up to 58 for depth of 8)
            if self.solutionsFoundForPath <= 25:
                self.updatePyGameScreen(True, False, False)

            # Returns true
            return True
        # Otherwise, if current block is not adjacent to end block then 
        else :
            # Return false
            return False

    # Function that runs the recursive colorPathCheck function for each individual color
    def puzzleSolvedCheck(self):
        # Runs color path checkers
        self.colorPathCheck(self.startingXPosition, self.startingYPosition, self.arrayOfPathSolutions[self.solutionsFoundForPath - 1], 0, 0)

    # Recursive function that simply checks if a color path is solved            
    def colorPathCheck(self, currentXPosition, currentYPosition, allSolutionCountGrid, lastMoveID, count):
        # Increment count, reassures that recursive function is not indefinite
        count += 1
        # Base case, if the function is still running and current grid position equals ending grid point, then puzzle is solved 
        if (currentXPosition == self.endingXPosition and currentYPosition == self.endingYPosition):
            # If our current grid position reaches our ending grid point, then path is successful and we set colorPathFound to true
            self.colorPathFound = True
        # Break clause of recursive function, prevents going forever
        elif (count < self.pathLengthLimit + 1):
            # Check each adjascent block, if any is of the same color then call function again after changing current grid position, lastMoveID assures the movement is not opposite to last move (becomes stuck)
            if (currentXPosition + 1 < size and allSolutionCountGrid[currentYPosition][currentXPosition + 1] != 0 and lastMoveID != 2):
                self.colorPathCheck(currentXPosition + 1, currentYPosition, allSolutionCountGrid, 1, count)
            elif (currentXPosition - 1 >= 0 and allSolutionCountGrid[currentYPosition][currentXPosition - 1] != 0 and lastMoveID != 1):
                self.colorPathCheck(currentXPosition - 1, currentYPosition, allSolutionCountGrid, 2, count)
            elif (currentYPosition + 1 < size and allSolutionCountGrid[currentYPosition + 1][currentXPosition] != 0 and lastMoveID != 4):
                self.colorPathCheck(currentXPosition, currentYPosition + 1, allSolutionCountGrid, 3, count)
            elif (currentYPosition - 1 >= 0 and allSolutionCountGrid[currentYPosition - 1][currentXPosition] != 0 and lastMoveID != 3):
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

    # Function that repeadily updates the board data
    def updatePyGameScreen(self, updatingIteration, updatingOtherGrid, gameArray): 
        # In range of the entire game array
        for row in range(size):
            for column in range(size):
                # Originally set to black, and if array are certain values, then change color
                color = WHITE

                # Gets current solution found
                #print("length is currently: ", self.color1.solutionsFoundForPath)

                if updatingOtherGrid:
                    currentGrid = gameArray
                else:
                    currentGrid = self.arrayOfPathSolutions[self.solutionsFoundForPath - 1]

                if self.checkStartOrEndPoint(row, column, 3):
                    color = BLUE
                elif currentGrid[row][column] != 0:
                    color = LIGHT_BLUE
                elif self.checkedInvalidBlocks[row][column] < 0:
                    color = LIGHT_RED

                """
                for checkedInvalidBlocksIndex in range (0, len(self.checkedInvalidBlocks), 2):
                    currentInvalidYPosition = self.checkedInvalidBlocks[checkedInvalidBlocksIndex]
                    currentInvalidXPosition = self.checkedInvalidBlocks[checkedInvalidBlocksIndex + 1]

                    if row == currentInvalidYPosition and column ==  currentInvalidXPosition:
                        invalidColor = LIGHT_RED
                        pygame.draw.rect(screen, invalidColor, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                """

                # Draws colored rectangles in respective spots with the color determined above
                pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

                # Displays the number of the block
                blockText = font.render(str(currentGrid[row][column]), True, WHITE)
                screen.blit(blockText, [(MARGIN + WIDTH) * column + (MARGIN * 3), (MARGIN + HEIGHT) * row + (MARGIN * 3), WIDTH, HEIGHT])

                # Coordinates for each block
                coordinateTextString = "(" + str(row) + ", " + str(column) + ")"
                coordinateText = font.render(coordinateTextString, True, BLACK)
                screen.blit(coordinateText, [(MARGIN + WIDTH) * (column + 1) - (MARGIN * 7), (MARGIN + HEIGHT) * (row + 1) - (MARGIN * 3), WIDTH, HEIGHT])

        # If we are updating with each iteration
        if updatingIteration:
            # Runs puzzle checker
            self.puzzleSolvedCheck()

            # Redraws display block
            pygame.draw.rect(screen, BLACK, [0, windowSize, windowSize, TEXT_DISPLAY_HEIGHT])

            # Creates and displays text of the current iteration
            iterationText = font.render("Solution: " + str(self.solutionsFoundForPath), True, WHITE)
            screen.blit(iterationText, [720, windowSize])

            # Creates and displays all five color path's statuses
            color1StatusText = font.render("Blue: " + str(self.colorPathFound), True, self.getStatusColor())
            screen.blit(color1StatusText, [5, windowSize + (18 * (self.colorID - 1))]) 

            # Prints current solution to console
            print("This is the current solution #", str(self.solutionsFoundForPath))
            super().printAnyArray(currentGrid)             

        # Updates pygame display at a maximum rate of 8 frames per second
        pygame.display.flip()
        clock.tick(2)

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

    

    # Updates the screen
    # pygame.display.flip()
    # clock.tick(60)

# Calls updatePyGameScreen() function once
newGame.color1.updatePyGameScreen(False, False, False)

# Terminates once quit button is hit
pygame.quit()

""""""""""""""""""""""""""""""""