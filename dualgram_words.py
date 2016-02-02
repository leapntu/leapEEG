from psychopy import visual, core, event, gui, sound   #, parallel
import pyglet, os, random, copy

#Environment setup and loading message
win = visual.Window()

loadMessage = visual.TextStim(win, text="Loading Stimuli\n\nPlease Wait")
loadMessage.draw()

win.flip()

#parallel.setPortAddress(0x378)
#parallel.setData(0)

#Constants and Parameters
gramASymbols = 'M R V T X'.split()
gramBSymbols = 'P Q W Y Z'.split()

gramAFiles = os.listdir('stimuli/gram_a')
gramBFiles = os.listdir('stimuli/gram_b')

blockFile = 'stimuli/metadata/order.txt'

gramAStims = [ sound.Sound(name=filename) for filename in gramAFiles ]
gramBStims = [ sound.Sound(name=filename) for filename in gramBFiles ]

codes = {
    'gramA': 0,
    'gramB': 2,
    'UngramA': 1,
    'UngramB': 3 }

def parseBlocks(blockFile):
    blockTemplate = { 'id': 0 , 'bites': [] }
    biteTemplate = { 'grammar': '' , 'symbols': [] }
    parseData = { 'blocks': [], 'line': '', 'reader': open(blockFile) }

    def init(template):
        return lambda : copy.deepcopy(template)

    newBlock = init(blockTemplate)
    newBite = init(biteTemplate)

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
        while isBite(getline()):
            block['bites'].append(readBite(block))
            nextline()
        return block

    nextline()
    while getline() != '':
        if isBlock(getline()):
            addBlock(readBlock())
        nextline()
    parseData['reader'].close()
    return parseData['blocks']

def setSymbols():
    dict = {}
    random.shuffle(gramASymbols)
    random.shuffle(gramBSymbols)
    for symbol, stimuli in zip(gramASymbols, gramAStims):
        dict[symbol] = stimuli
    for symbol, stimuli in zip(gramBSymbols, gramBStims):
        dict[symbol] = stimuli
    return dict

blocks = parseBlocks(blockFile)
lookup = setSymbols()

def playBite(bite):
    for symbol in bite['symbols']:
        stim = lookup[symbol]
        duration = stim.getDuration()
        stim.play()
        core.wait(duration)

def playTrainingBlock(block):
    for bite in block['bites']:
        playBite(bite)

def playTestBlock(testBlock):
    for bite in testBlock:
        playBite(bite)
        #parallel.setData(codes[ bite['grammar'] ])

def playBlocks(blocks):
    for block in blocks:
        if block['id'] != 'test':
            playTrainingBlock(block)
        elif block['id'] == 'test':
            playTestBlock(block)

playBlocks(blocks)

win.close()