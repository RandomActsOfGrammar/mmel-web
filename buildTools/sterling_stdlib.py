#!/usr/bin/python3

import sys
import os
import subprocess

import main_to_html_sterling as mths
import sterling_to_html as sth


def buildSosStdLibBody(outF, stdLibDir):
    #get the .sos files
    files = [f for f in os.listdir(stdLibDir) if f.endswith(".sos")]
    for f in files:
        #read file
        fIn = open(stdLibDir + "/" + f, "r")
        contents = fIn.read()
        fIn.close()
        #mark it up
        htmlContents = sth.markFullFile(contents, f)
        #write it out
        shortName = f.split("/")[-1]
        fileText = '<div class="section">\n'
        fileText += '<h3>File:  ' + shortName + '</h3>\n'
        fileText += htmlContents
        fileText += '</div>\n'
        outF.write(fileText)
    return 0


def buildXthmStdLibBody(outF, stdLibDir):
    #get the .xthm file
    filename = [f for f in os.listdir(stdLibDir) if f.endswith(".xthm")][0]
    #mark it up
    runRes = subprocess.run(["extensibella", "--thmDocHTML",
                             stdLibDir + "/" + filename])
    if runRes.returncode != 0:
        return 1
    thmDocFilename = ".".join(filename.split(".")[:-1]) + ".html"
    thmDocFile = open(thmDocFilename, "r")
    thmDocContents = thmDocFile.read()
    thmDocFile.close()
    os.remove(thmDocFilename) #no longer need it, so clean up after ourselves
    #write it out
    intro = """
<div class="section">
<h2>Extensibella Properties about the Standard Library</h2>
<p>
The Sterling standard library module also includes an Extensibella
reasoning module with properties about its relations.  These
properties are all proven to hold.
</p>
"""
    close = "</div>\n"
    outF.write(intro + thmDocContents + close)
    return 0


def fullBuild(stdLibDir, outputFilename):
    outputFile = open(outputFilename, "w")
    #heading
    mths.writeInitialText(outputFile, 0, "Standard Library")
    #title/intro
    intro = """
<div class="section">
<h1>Standard Library</h1>
<p>
All relations are part of the <tt>sterling:stdLib</tt> reasoning
module. Then, for example, the full name of the relation listed below
as <tt>lookup</tt> is <tt>sterling:stdLib:lookup</tt>.
</p>
</div>
"""
    outputFile.write(intro)
    #body
    retVal = buildSosStdLibBody(outputFile, stdLibDir)
    if retVal != 0:
        outputFile.close()
        return retVal
    retVal = buildXthmStdLibBody(outputFile, stdLibDir)
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
