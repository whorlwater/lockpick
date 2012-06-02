from random import shuffle, randint
from re import search
import sys
import os
import simplejson


HIGHSCORES_FILENAME = ".lockpick_highscores.json"


def makeLock():
    lock = []
    i = 0
    while i < 5:
        pin = randint(1,5)
        pin = str(pin)
        lock.insert(i,pin)
        i += 1
    shuffle(lock)
    return lock


def saveHighscore( name, tries ):

    if os.path.exists( HIGHSCORES_FILENAME ):
        data = simplejson.load( open( HIGHSCORES_FILENAME ) )
    
    else:
        data = {}

    if name not in data:
        data[ name ] = {}

    data[ name ][ "min"   ] = min( tries, data[ name ].get( "min", tries ) )
    data[ name ][ "max"   ] = max( tries, data[ name ].get( "max", tries ) )
    data[ name ][ "sum"   ] = data[ name ].get( "sum",   0 ) + tries
    data[ name ][ "count" ] = data[ name ].get( "count", 0 ) + 1

    fh = open( HIGHSCORES_FILENAME, "w" )
    simplejson.dump( data, fh )
    fh.close()

def returnHighscore( name ):

    if os.path.exists( HIGHSCORES_FILENAME ):
        data = simplejson.load( open( HIGHSCORES_FILENAME ) )
        
        min   = data[ name ][ "min"   ]
        max   = data[ name ][ "max"   ]
        sum   = data[ name ][ "sum"   ]
        count = data[ name ][ "count" ]

        average = sum / count

        print "You have completed %s games with %s guesses! On average, you can beat a game in %s guesses. Your best score is %s guesses in one game." % (count,sum,average,min)


    else:
        print "No high scores are available."

def main( argv ):
    # Enter name.
    validName = False
    print "Hello. Please enter your name."
    while not validName:
        checkName = raw_input()
        if not search("^[A-Za-z0-9]{1,19}$",checkName):
            print "Sorry, you can only use names 20 characters or less, using only letters and numbers."
            print "Please enter your name."
        else:
            while True:
                print "Is " + checkName + " correct? y/n?"
                verify = raw_input()
                if verify == "y":
                    name = checkName
                    validName = True
                    print "Welcome, %s!" % (name,)
                    break
                elif verify == "n":
                    print "That's O.K. Please re-enter your name."
                    break
                else:
                    print "Invalid response."

    # Play game.
    print "Lockpick is a game of logic. The lock has five pins that vary in length from 1-5. A lock may have any combination of pin lengths."
    print "If you guess a pin length in the correct location, you will hear a CLICK, and you will also receive feedback of how many total guessed lengths (including the ones which CLICKED) are correct, but not necessarily in the proper location."
    print "Type any combination of five numbers of 1-5 to begin. Good luck!"
    
    playGame = 1
    lock = makeLock()
    numberofPins = len(lock)
    tries = 0

    while playGame == 1:
        print "Pick the lock!"
        guessStr = raw_input()
        guess = list(guessStr)
        if len(guess) != numberofPins or search("[^0-5]",guessStr):
            print "Invalid guess. Try again."
        else:
            correctLocType = 0
            for x, y in zip(lock,guess):
                if x == y:
                    correctLocType += 1
            if correctLocType == numberofPins:
                tries += 1
                print "[CLICK]\nGood job, %s! Took you %s attempts to pick this lock." % ( name, tries )
                saveHighscore( name, tries )
                returnHighscore( name )
                checkPlay = 0
                while checkPlay == 0:
                    print "Play again? y/n?"
                    replay = raw_input()
                    if replay == "y":
                        checkPlay = 1
                        lock = makeLock()
                        numberofPins = len(lock)
                        tries = 0
                    elif replay == "n":
                        checkPlay = 1
                        playGame = 0
                        print "Goodbye!"
                    else:
                        print "Invalid response."
            else:
                tries += 1
                correctType = 0
                i = 1
                lockInt = map(int,lock)
                guessInt = map(int,guess)
                while i <= 5:
                    lockCount = lockInt.count(i)
                    if lockCount > 0:
                        guessCount = guessInt.count(i)
                        if guessCount >= lockCount:
                            correctType += lockCount
                        elif guessCount < lockCount:
                            correctType += guessCount
                    i += 1
                correctLocType = str(correctLocType)
                correctType = str(correctType)
                if correctType == correctLocType:
                    if correctLocType == '0':
                        print "You don't hear any pins snap in the right location. None of the guessed lengths match any of the five pins, and the lock won't turn. Keep trying!"
                    else:
                        print "You hear %s pins snap in the right location. All guessed lengths were in the right locations, but the lock won't turn. Keep trying!" % (correctLocType,)
                else:
                    print "You hear %s pins snap in the right location. Of all total guesses, %s were the correct length, but the lock won't turn. Keep trying!" % (correctLocType,correctType)


if __name__ == "__main__":
     main( sys.argv )



