#!/usr/bin/python3

import sys

#Read all comments from the start of fContents, currently at nesting
#   depth numComments
#Returns (text of the comment, rest of the file)
def readComment(fContents, numComments):
    if numComments == 0:
        return ("", fContents)
    locStart = fContents.find("/*")
    locEnd = fContents.find("*/")
    if locStart >= 0 and locStart < locEnd:
        c = fContents[:locStart + 2]
        a, b = readComment(fContents[locStart + 2:], numComments + 1)
        return (c + a, b)
    else:
        c = fContents[:locEnd + 2]
        a, b = readComment(fContents[locEnd + 2:], numComments -1)
        return (c + a, b)


#Read a single line comment
#Returns (text of the comment, rest of the file)
def readLineComment(fContents):
    lineEnd = fContents.find("\n")
    if lineEnd < 0: #end of file
        return (fContents, "")
    else:
        return (fContents[:lineEnd], fContents[lineEnd:])


#Turn the comment text, including delimiters, into a comment span
#Returns a string of the HTML comment
def makeComment(commentText):
    return '<span class="comment">' + commentText + '</span>'


#Read off space and comments before a command
#Returns (text of the space/comments, rest)
def readSpace(fContents):
    text = ""
    atCommand = False
    while fContents != "" and not atCommand:
        if fContents[0] == "%":
            commentText, fContents = readLineComment(fContents)
            text += makeComment(commentText)
        elif fContents[:2] == "/*":
            commentText, fContents = readComment(fContents[2:], 1)
            text += makeComment("/*" + commentText)
        elif fContents[0].isspace():
            text += fContents[0]
            fContents = fContents[1:]
        else: #actual text
            atCommand = True
    return (text, fContents)


#Return True if the string starts with a TopCommand thing
def isTopCommand(s):
    topCommandStart = ["Theorem", "Define", "CoDefine", "Query",
                       "Kind", "Type", "Close", "Import", "Split",
                       "Extensible", "Translation", "Ext_Ind",
                       "Prove"]
    for x in topCommandStart:
        if s.startswith(x):
            return True
    return False


#Read the next command, assuming we are starting with the command text
#Returns (text of the command, rest of the file, is TopCommand)
def readFullCommand(fContents):
    text = ""
    atEnd = False
    while fContents != "" and not atEnd:
        if fContents[0] == "%":
            commentText, fContents = readLineComment(fContents)
            text += makeComment(commentText)
        elif fContents[:2] == "/*":
            commentText, fContents = readComment(fContents[2:], 1)
            text += makeComment("/*" + commentText)
        elif fContents[0] == ".":
            text += "."
            fContents = fContents[1:]
            atEnd = True
        else: #regular text
            text += fContents[0]
            fContents = fContents[1:]
    return (text, fContents, isTopCommand(text))


#Read all commands that are part of a proof
#Ends when it finds a top command and leaves it there
#Returns (text of the proof, rest of the file, next cmd ID)
def readFullProof(fContents, cmdID, linkedFile):
    text = ""
    reachedEnd = False
    while not reachedEnd:
        initSpace, initRest = readSpace(fContents)
        cmd, rest, isTop = readFullCommand(initRest)
        if isTop or rest == "": #end on empty file as well
            reachedEnd = True
        else:
            text += initSpace
            text += '<a class="tactic" href="' + linkedFile
            text += '#' + str(cmdID) + '">' + cmd
            text += '</a>'
            cmdID += 1
            fContents = rest
    return (text, fContents, cmdID)


#Read the file, adding in all the links and whatnot
#Returns the text of the HTML
def readFullFile(fContents, cmdID, linkedFile):
    text = ""
    while fContents != "":
        initSpace, initRest = readSpace(fContents)
        cmd, cmdRest, _ = readFullCommand(initRest)
        #add command
        text += initSpace + '<a class="command" href="' + linkedFile
        text += '#' + str(cmdID) + '">' + cmd + '</a>'
        cmdID += 1
        #read proof
        if cmdRest[:1] == "\n":
            cmdRest = cmdRest[1:] #drop newline we replace
        prfText, prfRest, rID = readFullProof(cmdRest, cmdID, linkedFile)
        if cmdID < rID: #proof given
            text += "<span> </span>" #spacer before hide/show proof
            #proof toggle
            text += '<a class="fold-link" href="javascript:void" '
            text += 'onclick="proofToggle(' + str(cmdID) + ');" '
            text += 'id="toggleproof' + str(cmdID) + '">[Show Proof]</a>\n'
            #proof block
            text += '<div class="proof" id="proof' + str(cmdID)
            text += '" style="display: none;">\n' + prfText + '</div>'
        else:
            text += "\n" #if no proof, need to replace dropped one
        fContents = prfRest
        cmdID = rID
    return text


#Mark the text, adding the start and end markers
def markFullFile(fContents, linkedFile):
    text = '<pre class="code extensibella">\n'
    text += readFullFile(fContents, 1, linkedFile)
    text += '</pre>\n'
    return text


#Read the file, process it, then write it out
def process(filenameIn, filenameOut, modeOut):
    fIn = open(filenameIn, "r")
    fContents = fIn.read()
    fIn.close()
    text = markFullFile(fContents)
    fOut = open(filenameOut, modeOut)
    fOut.write(text)
    fOut.close()


def main(args):
    fname = args[1]
    out = args[2]
    process(fname, out, "a")


if __name__ == "__main__":
    main(sys.argv)
