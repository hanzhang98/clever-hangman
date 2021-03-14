"""
Created on 4/12/2020

@author: Han Zhang
"""
import random

def handleUserInputDebugMode():
    '''
    Asks the user to input 'd' for debug mode or 'p' for play mode.
    Returns True for debug mode and False for play mode.
    '''
    mode = input("Which mode do you want: (d)ebug or (p)lay: ")
    if str(mode) == 'd':
        return True
    if str(mode) == 'p':
        return False


def handleUserInputWordLength():
    '''
    Asks the user to input the number of letters of a word to guess
    Returns the length of the word based on user input
    '''
    wordLength = input("How many letters in the word you'll guess: ")
    return int(wordLength)


def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the
    corresponding number of misses allowed for the game.
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    difficulty = input("(h)ard or (e)asy> ")
    if str(difficulty) == 'e':
        return 12
    if str(difficulty) == 'h':
        return 8


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    print(displayString)
    guess = input("letter >")
    while guess in lettersGuessed:
        print("you already guessed that")
        guess = input("letter >")
    if guess not in lettersGuessed:
        lettersGuessed.append(guess)
    return guess


def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    Letters that have not been guessed, number of misses left and the current Hangman word will be printed
    '''
    all = 'abcdefghijklmnopqrstuvwxyz'
    ret = ''
    for c in all:
        if c not in lettersGuessed:
            ret = ret + c
        else:
            ret = ret + ' '
    return "letters not yet guessed: " + ret + "\nmisses remaining = " + str(
        missesLeft) + "\n" + " ".join(hangmanWord)


def createTemplate(currTemplate, letterGuess, word):
    '''
    Checks if the letter guessed by user is in the secret word and returns an
    updated template
    '''
    current = [c for c in currTemplate]
    wordlst = [x for x in word]
    for i in range(len(wordlst)):
        if letterGuess == wordlst[i] and current[i] == '_':
            current[i] = letterGuess
    return ''.join(current)


def getNewWordList(currTemplate, letterGuess, wordList, debug):
    '''
    Asks the user to input 'd' for debug mode or 'p' for play mode.
    Returns True for debug mode and False for play mode.
    '''
    dict = {}
    for e in wordList:
        wordkey = createTemplate(currTemplate, letterGuess, e)
        if wordkey not in dict:
            dict[wordkey] = []
        dict[wordkey].append(e)
    if debug:
        for item in sorted(dict.keys()):
            print(item + ' : ' + str(len(dict[item])))
        print('# keys = ' + str(len(dict)))
    dictlst = sorted(dict.items(), key = lambda k: (len(k[1]), k[0].count(
        '_')), reverse = True)
    return dictlst[0]


def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    Based on the new hangmanWord from the getNewWordList function, check if the
    guessedLetter is in hangmanWord and returns the updated number of misses
    left as well as if user guessed the letter correctly
    '''
    if guessedLetter not in hangmanWord:
        index0 = missesLeft - 1
        index1 = False
    if guessedLetter in hangmanWord:
        index0 = missesLeft
        index1 = True
    return [index0, index1]



def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    First, file is opened to obtain and cleaned
    '''
    f = open(filename, encoding="utf-8")
    ret = []
    for line in f:
        clean = line.replace("\n", "")
        ret.append(clean)
    f.close()
    '''
    Random word is chosen, and empty lists of hangman word and letters
    guessed are build. Following which, the
    various functions are called
    '''

    mode = handleUserInputDebugMode()
    letters = handleUserInputWordLength()
    missesLeft = int(handleUserInputDifficulty())
    misses_allowed = missesLeft
    lettersGuessed = []
    hangmanWord = []
    #word list is based on the number of letters
    wordList = [e for e in ret if len(e) == letters]
    total_guesses = 0
    for i in range(letters):
        hangmanWord.append("_")
    '''
    Loop is used to process each guess until 0 misses left or word is guessed
    '''
    while "_" in hangmanWord and missesLeft > 0:
        secretWord = wordList[random.randint(0, len(wordList)-1)]
        # returns letters user has not guessed
        displayString = createDisplayString(lettersGuessed, missesLeft,
                                            hangmanWord)
        if mode:
            print("(word is " + secretWord + ")")
            print("# possible words: ", len(wordList))

        # prints the string and ask user to input string
        guessedLetter = handleUserInputLetterGuess(lettersGuessed,
                                                   displayString)
        # returns a new list
        newlist = getNewWordList(''.join(hangmanWord), guessedLetter, wordList,
                             mode)
        # newlist is a tuple of (template, list of words), thus hangmanWord is
        # updated as the template and wordList is updated accordingly
        hangmanWord = [x for x in newlist[0]]
        wordList = newlist[1]
        #process the guess and updates
        outcome = processUserGuessClever(guessedLetter, hangmanWord, missesLeft)
        total_guesses += 1
        if not outcome[1]:
            print("you missed: " + guessedLetter + " not in word")
        missesLeft = outcome[0]
    missed_guesses = misses_allowed - missesLeft
    if "_" not in hangmanWord:
        print("you guessed the word: " + secretWord)
        print("you made " + str(total_guesses) + " guesses with " + str(
            missed_guesses) + " misses")
        return True
    elif missesLeft <= 0:
        print("you're hung!! \nword was " + secretWord)
        print("you made " + str(total_guesses) + " guesses with " + str(
            misses_allowed) + " misses")
        return False

if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    win = 0
    count = 1
    if runGame('somewords.txt'):
        win += 1
    repeat = input("Do you want to play again? y or n> ")
    while repeat == 'y':
        count += 1
        if runGame('somewords.txt'):
            win += 1
        repeat = input("Do you want to play again? y or n> ")
    loss = count - win
    print('You won ' + str(win) +' game(s) and lost ' + str(loss))