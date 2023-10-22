#!/usr/bin/python3

import sys
import subprocess

import sterling_to_html as sth

#Write out text starting the HTML for the basic file
def writeInitialText(outF, titleInfo):
    text = "<html>\n"
    #start head
    text += "<head>\n"
    #title
    text += '<title>Sterling:  ' + titleInfo + '</title>\n'
    #style sheet
    text += '<link href="../style.css" rel="stylesheet" type="text/css">\n'
    #script
    text += '<script src="../actions.js"></script>\n'
    #favicon
    text += '<link rel="icon" href="images/favicon.png" type="image/x-icon">\n'
    #end head
    text += "</head>\n"
    #start body
    text += "<body class=\"sterling\">\n"
    #logo
    text += '<div id="header-logo">\n'
    text += '<a href="index.html">\n'
    text += '<img class="header-logo" src="images/Sterling.png" '
    text += 'alt="Sterling logo">\n'
    text += '</a>\n'
    text += '</div>\n'
    outF.write(text)


#Write out text ending the HTML for the basic file
def writeEndText(outF):
    outF.write("</body>\n" + "</html>\n")


#Write out the specification files
def writeFiles(outF, sosFilenames):
    for fname in sosFilenames:
        shortName = fname.split("/")[-1]
        #heading for file
        outF.write("<h3>File:  " + shortName + "</h3>\n")
        #text of the body
        f = open(fname, "r")
        text = f.read()
        f.close()
        htmlText = sth.markFullFile(text, shortName)
        outF.write(htmlText)


#Write the full HTML file
def writeHTMLFile(outFilename, titleInfo, sosFilenames):
    outF = open(outFilename, "w")
    writeInitialText(outF, titleInfo)
    outF.write('<h1>' + titleInfo + '</h1>')
    writeFiles(outF, sosFilenames)
    writeEndText(outF)
    outF.close()


def main(args):
    if len(args) < 4 or args[1].split(".")[-1] != "html":
        print("Usage:  " + args[0] + " <out filename> <title info> <.sos files>")
        return
    outFilename = args[1]
    titleInfo = args[2]
    sosFiles = args[3:]
    writeHTMLFile(outFilename, titleInfo, sosFiles)


if __name__ == "__main__":
    main(sys.argv)
