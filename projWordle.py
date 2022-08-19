# Claudia Deverdits
# Due May 2, 2022
# Programming Project Implementation - Wordle

# This implementation of Wordle is similar to the original in that a user guesses a 5 letter word and gets a clue,
# but everything is text-based. Players will be given the option to continue playing with new words for as long as
# they want to. The user has 6 guesses to guess a 5 letter word and gets clues to help them along the way. If a clue
# is "G", that letter is in the correct spot, if it is "Y" then it is in the incorrect spot, if it is "X",
# the letter is not in the word at all. The game ends once the player choses not to continue.

import random


def openFile():
    # This function will open the file and make sure the file name entered is valid.
    validFile = False
    while validFile == False:
        fileName = input("Please enter a file name: ")
        try:
            file = open(fileName, 'r')
            validFile = True
        except IOError:
            print("Invalid file name try again ...")
    return file


def getData():
    # This function will read the data from the file and return a list of all the words.
    wordFile = openFile()
    dictionary = []
    for line in wordFile:
        line = line.strip()
        dictionary.append(line)
    wordFile.close()

    return dictionary


def chooseWord(dictionary):
    # This function will choose a word from the dictionary to be the solution and remove
    # it from the list after to make sure it cannot be chosen again.
    solution = 0
    index = random.randint(0, len(dictionary) - 1)
    solution = dictionary[index]
    return solution, index


def getGuess(dictionary):
    # This function gets a guess from the user, and makes sure its a valid word.
    validWord = False
    while validWord == False:
        guess = input("Make a guess: ").upper()
        try:
            dictionary.index(guess)
            validWord = True
        except:
            print("Word not in dictionary - try again...")
    return guess


def computeClue(guess, solution):
    # This function will compute the clue by comparing the guess and the solution
    guess = list(guess)
    solution = list(solution)

    # list to hold clue
    clue = [0, 0, 0, 0, 0]

    if guess == solution:
        clue = ["G", "G", "G", "G", "G"]
    else:
        # If guess is not correct, go through the next loops

        # first check if there are any double letters and mark them as yellow
        for i in range(len(solution)):
            if guess.count(guess[i]) > 1:
                clue[i] = "Y"

        # if the letters match, mark them as green and remove the letter from the solution
        for i in range(len(solution)):
            if guess[i] == solution[i]:
                clue[i] = "G"
                solution[i] = "_"

        # if letter is in the solution and not already green, mark as yellow
        for i in range(len(solution)):
            if guess[i] in solution and clue[i] != "G":
                clue[i] = "Y"
            # otherwise, mark as not in the word
            elif clue[i] != "G":
                clue[i] = "X"
    clue = "".join(clue)
    return clue


def printGuess(guess, clue):
    # This function prints the guess and clue after it is computed
    print(guess)
    print(clue)


def handleEnd(clue, solution, numGuesses):
    # This function will compute the score for the game, based on the final clue and the number of guesses
    if clue == "GGGGG":
        score = numGuesses
        print(" ")
        print("Congratulations, your wordle score for this game is ", numGuesses)
    else:
        score = 10
        print("Sorry, you did not guess the word: ", solution)
    return score


def printResults(overallScore):
    # This function prints all of the results at the end of the game
    print("Your overall score is ", overallScore)


def handleChoice():
    # This function handles the Y/N choice that the user makes at the end of the game
    validChoice = False
    choices = ["Y","N"]
    while validChoice == False:
        choice = input("Would you like to play again (Y or N)?").upper()
        try:
            choices.index(choice)
            validChoice = True
        except:
            print("Invalid choice, please try again...")
    if choice == "N":
        print(" ")
        print("Thanks for playing!")

    return choice


def main(seedIn):
    random.seed(seedIn)
    dictionary = getData()
    overallScore = 0
    choice = "Y"
    # while choice is yes, run the functions that need to be repeated for the game
    while choice != "N":
        solution, index = chooseWord(dictionary)
        guesses = 0
        clue = 0
        # while guesses remain and the word is not guessed, run the functions that need to be repeated every turn
        while guesses != 6 and clue != "GGGGG":
            guess = getGuess(dictionary)
            clue = computeClue(guess, solution)
            printGuess(guess, clue)
            guesses += 1
        dictionary[index] = "_____"

        score = handleEnd(clue, solution, guesses)
        overallScore += score
        printResults(overallScore)
        print(" ")
        choice = handleChoice()