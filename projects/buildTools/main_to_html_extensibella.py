#!/usr/bin/python3

import sys
import subprocess

import extensibella_to_html as eth
import sterling_to_html as sth

#Write out text starting the HTML for the basic file
def writeInitialText(outF, titleInfo):
    text = "<html>\n"
    #start head
    text += "<head>\n"
    #title
    text += '<title>Extensibella:  ' + titleInfo + '</title>\n'
    #style sheet
    text += '<link href="../style.css" rel="stylesheet" type="text/css">\n'
    #script
    text += '<script src="../actions.js"></script>\n'
    #favicon
    text += '<link rel="icon" href="images/favicon.png" type="image/x-icon">\n'
    #end head
    text += "</head>\n"
    #start body
    text += "<body class=\"extensibella\">\n"
    #logo
    text += '<div id="header-logo">\n'
    text += '<a href="index.html">\n'
    text += '<img class="header-logo" src="images/Extensibella.png" '
    text += 'alt="Extensibella logo">\n'
    text += '</a>\n'
    text += '</div>\n'
    outF.write(text)


#Write out text ending the HTML for the basic file
def writeEndText(outF):
    outF.write("</body>\n" + "</html>\n")


#Write out the language specification
def writeSpec(outF, sosFilenames):
    outF.write('<div class="section specification">\n')
    outF.write("<h2>Language Specification</h2>\n")
    for fname in sosFilenames:
        shortName = fname.split("/")[-1]
        #heading for file
        outF.write("<h3>File:  " + shortName + "</h3>\n")
        #collapse/expand
        foldLink = '<a class="fold-link" href="javascript:void" '
        foldLink += 'id="toggle' + shortName + '" '
        foldLink += 'onclick="toggleFile(\'' + shortName + '\')">'
        foldLink += '[Shrink File]</a>'
        outF.write(foldLink)
        #text of the body
        f = open(fname, "r")
        text = f.read()
        f.close()
        htmlText = sth.markFullFile(text, shortName)
        outF.write(htmlText)
    outF.write("</div>\n")


#Write out the proof part
def writeProof(outF, extensibellaFilename, detailsFile):
    outF.write('<div class="section reasoning">\n')
    outF.write('<h2>Reasoning</h2>\n')
    #intro
    links = '<a class="fold-link" href="javascript:void" '
    links += 'onclick="allProofShow();">[Show All Proofs]</a>'
    links += '<span> </span>'
    links += '<a class="fold-link" href="javascript:void" '
    links += 'onclick="allProofHide();">[Hide All Proofs]</a>\n'
    outF.write(links)
    text = "<p>Click on a command or tactic to see a detailed view "
    text += "of its use.</p>"
    outF.write(text)
    #.xthm contents
    f = open(extensibellaFilename, "r")
    text = f.read()
    f.close()
    htmlText = eth.markFullFile(text, detailsFile)
    outF.write(htmlText)
    outF.write("</div>\n")


#Write the full HTML file
def writeHTMLFile(outFilename, extensibellaFilename, sosFilenames,
                  titleInfo, detailsFile):
    outF = open(outFilename, "w")
    writeInitialText(outF, titleInfo)
    outF.write('<h1>' + titleInfo + '</h1>')
    writeSpec(outF, sosFilenames)
    writeProof(outF, extensibellaFilename, detailsFile)
    writeEndText(outF)
    outF.close()





#Write the details file
def writeDetailsFile(outFilename, extensibellaFilename, titleInfo):
    outF = open(outFilename, "w")
    writeInitialText(outF, titleInfo + " - Details")
    outF.write("<h2>Reasoning Details</h2>\n")
    outF.write('<div class="section">\n')
    outF.close()
    #run Extensibella for the main text
    subprocess.run(["extensibella", "--annotate", outFilename,
                    extensibellaFilename])
    #write the end
    outF = open(outFilename, "a")
    outF.write('</div>\n')
    writeEndText(outF)
    outF.close()





#Write both files
def fullProcess(outFilebase, extensibellaFilename, sosFilenames,
                titleInfo):
    detailsFile = outFilebase + "-details.html"
    writeHTMLFile(outFilebase + ".html", extensibellaFilename,
                  sosFilenames, titleInfo, detailsFile)
    writeDetailsFile(detailsFile, extensibellaFilename, titleInfo)





def main(args):
    if len(args) < 5:
        print("Usage:  " + args[0] + " <out filename base> " +
              "<title info> <.xthm file> <.sos files>")
        return
    fbase = args[1]
    titleInfo = args[2]
    extensibellaFile = args[3]
    sosFiles = args[4:]
    fullProcess(fbase, extensibellaFile, sosFiles, titleInfo)


if __name__ == "__main__":
    main(sys.argv)
