#!/bin/python3

import os
import sys
import re

#check all the files
def check_all(root):
    messages = []
    for f in os.listdir(root):
        full = root + "/" + f
        if os.path.isdir(full):
            messages += check_all(full)
        elif f.endswith(".html"):
            openFile = open(full, 'r')
            fContents = openFile.read()
            openFile.close()
            messages += check_file(fContents, f, root)
    return messages

#regex for matching an href or src in a file
REF_RE = r'(([hH][rR][eE][fF])|([sS][rR][cC]))' + \
         r'[\ ]*=[\ ]*"([^"#]*)(#[^"]*)?"'

#check all links in a file for validity, returning a list of messages
#for missing files
def check_file(fContents, filename, dirname):
    output = []
    l = re.findall(REF_RE, fContents)
    for _, _, _, lookForName, tag in l:
        full = dirname + "/" + lookForName
        if  not (lookForName.startswith("https://") or \
                 lookForName.startswith("http://")) and \
            not lookForName == "javascript:void" and \
            not lookForName == "" and \
            not os.path.isfile(full):
            output += ["'" + lookForName + "' missing (linked in '" +
                       dirname + "/" + filename + "')"]
    return output


def main(args):
    if len(args) < 2:
        print("Must give directory to check")
    msgs = check_all(args[1])
    if len(msgs) > 0:
        print("Missing files linked in website files:")
        for m in msgs:
            print("   " + m)
        return 1
    else:
        print("No missing files; good to place")
        return 0

if __name__ == "__main__":
    main(sys.argv)
