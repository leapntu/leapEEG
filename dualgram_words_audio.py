from psychopy import visual, core, parallel, event, gui, sound
import pyglet, os, random, copy
from pyo import *

###ENVIRONMENT AND LOADING###
mode = 'load'
win = visual.Window()

loadMessage = visual.TextStim(win, text="Loading Stimuli\n\nPlease Wait")
loadMessage.draw()

win.flip()

###CONSTANTS AND PARAMETERS###

introMessage = "DUAL GRAMMAR TASK - INSTRUCTIONS TO PARTICIPANTS AND ORDER OF PRESENTATION OF PARTS OF EXPERIMENT\nHello! Welcome to our cognitive brain training game! Test your attention abilities and the way you can improve them! If you complete the following tasks successfully, you may improve your cognitive abilities!\nThe game has 6 rounds, lasting approximately 12 minutes overall. Your task is to pay close attention to the sequences of words. It is important to pay attention to the words as you will be tested on what you have heard later on! We believe that though this task is demanding, it will pay off.\nYou will be given a break at the end of each round. Please rest for as long as you need to during the breaks given, or continue to the next round if you are able to power through!\nPlease ensure that you are in a quiet room and have earphones to listen to the words before starting the task.\nPress <b>SPACEBAR</b> when you are ready."

restMessage = "You can now take a break for as long as you need to before continuing.\nPlease press <b>SPACEBAR</b> when you are ready to continue."

halfwayMessage = "WELL DONE! You are halfway done!\n"+restMessage

preTestMessage = "Well done!\nThe  sequences that you have just heard were generated according to a set of rules that determined the order of words within each sequence.\nYou will now hear a new set of  sequences. Half of these sequences will conform to the same set of rules as before, and the rest will not. Your task is to judge which of the sequences follow the same rules as before and which do not.\nIf the  sequence follows the same roles as before, press <b>Y</b>.\nIf the  sequence does not follow the same rules as before,\npress <b>N</b>.\nIf you are unsure, please respond with your gut feeling.\nPress <b>SPACEBAR</b> when you are ready to begin."

testMessage = "Did the  sequence follow the same rules as before?\n<b>Y (YES)</b>                                     <b>N (NO)</b>"

goodbyeMessage = "You have now come to the end of our experiment.\nFor more information on our study, please refer to our debrief notes.\nThank you for your time and participation!"

intro = visual.TextStim(win, text=introMessage)
rest = visual.TextStim(win, text=restMessage)
halfway = visual.TextStim(win, text=halfwayMessage)
preTest = visual.TextStim(win, text=preTestMessage)
test = visual.TextStim(win, text=testMessage)
goodbye = visual.TextStim(win, text=goodbyeMessage)

gramASymbols = 'M R V T X'.split()
gramBSymbols = 'P Q W Y Z'.split()

expDir = '/home/leapadmin/Desktop/leapEEG/'
stimuliDir = expDir + 'stimuli/'
gramADir = stimuliDir + 'gram_a/'
gramBDir = stimuliDir + 'gram_b/'

gramAFiles = os.listdir(gramADir)
gramBFiles = os.listdir(gramBDir)

blockFile = 'stimuli/metadata/order.txt'

gramAStims = [ sound.Sound(gramADir+filename) for filename in gramAFiles ]
gramBStims = [ sound.Sound(gramBDir+filename) for filename in gramBFiles ]

fixation = visual.ImageStim(win, stimuliDir + 'fix.svg.png')

port = parallel.ParallelPort('/dev/parport0')
core.wait(2)
port.setData(0)

data = []

###FUNCTION DEFINITIONS###
def parseBlocks(blockFile):
#Data Types
    blockTemplate = { 'id': 0 , 'bites': [] }
    biteTemplate = { 'grammar': '' , 'symbols': [] }
    parseData = { 'blocks': [], 'line': '', 'reader': open(blockFile) }

#Data Type Functions
    def init(template):
        return lambda : copy.deepcopy(template)

    newBlock = init(blockTemplate)
    newBite = init(biteTemplate)

#Processing Functions
    def startsWith(str):
        return lambda l : l.startswith(str)

    isBlock = startsWith('b:')
    isGram = startsWith('Gram')
    isUn = startsWith('Un')

    def isBite(str):
        if isGram(str) or isUn(str):
            return True
        return False

    def nextline():
        parseData['line'] = parseData['reader'].readline()
        
    def getline():
        return parseData['line']

    def addBlock(block):
        parseData['blocks'].append(block)

    def readBite(block):
        bite = newBite()
        bite['grammar'] = getline().split()[0]
        bite['symbols'] = getline().split()[1:]
        return bite

    def readBlock():
        block = newBlock()
        block['id'] = getline().split(':')[1].strip()
        nextline()
        lineNum = 1 #counter for bite number in block (ignored for non-test bites)
        while isBite(getline()):
            block['bites'].append(readBite(block))
            if block['id'] == 'test': #code test bites in sequence in file
              block['bites'][-1]['code'] = lineNum
              lineNum += 1
            elif block['id'] != 'test': #ignore non-test bites and code uniformly
              block['bites'][-1]['code'] = 21
            nextline()
        return block

#Algorithm
    nextline()
    while getline() != '':
        if isBlock(getline()):
            addBlock(readBlock())
        nextline()
    parseData['reader'].close()
    return parseData['blocks']

#Create map between symbols in block and playable stimuli
def setSymbols():
    lookupDict = {}
    random.shuffle(gramASymbols)
    random.shuffle(gramBSymbols)
    for symbol, stimuli in zip(gramASymbols, gramAStims):
        lookupDict[symbol] = stimuli
    for symbol, stimuli in zip(gramBSymbols, gramBStims):
        lookupDict[symbol] = stimuli
    return lookupDict

#Experiment control functions
def playBite(bite):
    for symbol in bite['symbols']:
        stim = lookup[symbol]
        duration = stim.getDuration()
        code = bite['code']
        port.setData(code)
        stim.play()
        core.wait(duration)
        port.setData(0)

def playTrainingBlock(block):
    for bite in block['bites']:
        playBite(bite)
    

def playTestBlock(testBlock):
    global data
    random.shuffle(testBlock['bites'])
    for bite in testBlock['bites']:
        fixation.draw()
        win.flip()
        playBite(bite)
        test.draw()
        win.flip()
        answer = event.waitKeys(keyList=['y','n'])[0]
        data.append(answer)

def playBlocks(blocks):
    global mode
    for block in blocks:
      fixation.draw()
      win.flip()
    if block['id'] != 'test':
        playTrainingBlock(block)
        if block['id'] == 3:
          halfway.draw()
        elif block['id'] != 3:
          rest.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
    elif block['id'] == 'test':
        preTest.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        playTestBlock(block)
        goodbye.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        win.close()

###MAIN ROUTINE###
#Get experiment blocks from file, create symbol map, and play all blocks of experiment
blocks = parseBlocks(blockFile)
lookup = setSymbols()
intro.draw()
win.flip()
event.waitKeys(keyList=['space'])
playBlocks(blocks)
