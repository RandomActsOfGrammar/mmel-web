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


#Read the text, inserting spans to color the comments
def readFull(fContents):
    locStart = fContents.find("/*")
    if locStart < 0:
        return fContents
    else:
        initial = fContents[:locStart]
        comment, rest = readComment(fContents[locStart + 2:], 1)
        text = initial + '<span class="comment">/*' + comment
        text += '</span>'
        return text + readFull(rest)


#Mark the text, adding the start and end markers
def markFullFile(fContents, fname):
    text = '<pre class="code sterling" id="' + fname + '">\n'
    text += readFull(fContents)
    text += '</pre>\n'
    return text


#Read the file, process it, then write it out
def process(filenameIn, filenameOut, modeOut):
    fIn = open(filenameIn, "r")
    fContents = fIn.read()
    fIn.close()
    text = markFullFile(fContents, filenameIn)
    fOut = open(filenameOut, modeOut)
    fOut.write(text)
    fOut.close()


def main(args):
    fname = args[1]
    out = args[2]
    process(fname, out, "a")


if __name__ == "__main__":
    main(sys.argv)
