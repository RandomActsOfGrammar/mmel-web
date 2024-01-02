#!/usr/bin/python3

import sys
import os
import subprocess

import main_to_html_extensibella as mthe


def buildStdLibBody(outF, stdLibDir):
    try:
        #go to the stdLib directory
        os.chdir(stdLibDir)
        #build the HTML file
        runres = subprocess.run(["./build_docs", "--html"])
        if runres.returncode != 0:
            return 1
        #put all of it after the first two lines (<html> and <body>)
        #   into outF
        stdLibF = open("stdLibDoc.html", "r")
        stdLibF.readline() #<html>
        stdLibF.readline() #<body>
        rest = stdLibF.read()
        outF.write(rest)
        return 0
    except Exception:
        return 1


def fullBuild(stdLibDir, outputFilename):
    outputFile = open(outputFilename, "w")
    mthe.writeInitialText(outputFile, 0, "Standard Library")
    retVal = buildStdLibBody(outputFile, stdLibDir)
    outputFile.close()
    return retVal


def main(args):
    if len(args) < 3:
        print("Usage:  " + args[0] + " <stdLib dir> <output filename>")
    stdLibDir = args[1]
    outputFilename = args[2]
    return fullBuild(stdLibDir, outputFilename)


if __name__ == "__main__":
    sys.exit(main(sys.argv)) #return the error code
