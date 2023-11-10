#!/usr/bin/python3

import sys
import subprocess

import sterling_to_html as sth

#Write out text starting the HTML for the basic file
def writeInitialText(outF, depth, titleInfo):
    depthText = "../" * depth
    text = "<html>\n"
    #start head
    text += "<head>\n"
    #title
    text += '<title>Sterling:  ' + titleInfo + '</title>\n'
    #style sheet
    text += '<link href="' + depthText + '../style.css" rel="stylesheet" type="text/css">\n'
    #script
    text += '<script src="' + depthText + '../actions.js"></script>\n'
    #favicon
    text += '<link rel="icon" href="' + depthText + 'images/favicon.png" type="image/x-icon">\n'
    #end head
    text += "</head>\n"
    #start body
    text += "<body class=\"sterling\">\n"
    #logo
    text += '<div id="header-logo">\n'
    text += '<a href="' + depthText + 'index.html">\n'
    text += '<img class="header-logo" src="' + depthText + 'images/Sterling.png" '
    text += 'alt="Sterling logo">\n'
    text += '</a>\n'
    text += '</div>\n'
    outF.write(text)


#Write out text ending the HTML for the basic file
def writeEndText(outF):
    #link to navigate back to example home
    outF.write('<div class="section">\n')
    outF.write('<a class="navlink" href="../description.html">Back to example home</a>\n')
    outF.write('</div>\n')
    #close out file
    outF.write("</body>\n" + "</html>\n")


#Write out the specification files
def writeFiles(outF, sosFilenames):
    for fname in sosFilenames:
        shortName = fname.split("/")[-1]
        #heading for file
        outF.write("<h3>File:  " + shortName + "</h3>\n")
        #links
        foldLink = '<a class="fold-link" href="javascript:void" '
        foldLink += 'id="toggle' + shortName + '" '
        foldLink += 'onclick="toggleFile(\'' + shortName + '\')">'
        foldLink += '[Reduce File]</a>'
        foldLink += '<span> </span>'
        foldLink += '<a class="fold-link" href="' + fname + '">'
        foldLink += '[Raw File]</a>\n'
        outF.write(foldLink)
        #text of the body
        f = open(fname, "r")
        text = f.read()
        f.close()
        htmlText = sth.markFullFile(text, shortName)
        outF.write(htmlText)


#Write the full HTML file
def writeHTMLFile(depth, outFilename, titleInfo, sosFilenames):
    outF = open(outFilename, "w")
    writeInitialText(outF, depth, titleInfo)
    outF.write('<h1>' + titleInfo + '</h1>')
    outF.write('<div class="section">\n')
    writeFiles(outF, sosFilenames)
    outF.write('<div>\n')
    writeEndText(outF)
    outF.close()


def main(args):
    if len(args) < 5 or args[2].split(".")[-1] != "html":
        print("Usage:  " + args[0] + " <depth from root> <out filename> <title info> <.sos files>")
        return
    depth = int(args[1])
    outFilename = args[2]
    titleInfo = args[3]
    sosFiles = args[4:]
    writeHTMLFile(depth, outFilename, titleInfo, sosFiles)


if __name__ == "__main__":
    main(sys.argv)
