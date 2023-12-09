The `extensibella` directory contains the actual web content.  The
`buildTools` directory contains scripts for creating the full web
content.

To build the website, run
```
./buildTools/build_web
```
This will build all the examples and put the website with generated
tarballs and no build scripts in a directory named `full_web`.
Options for this script:
```
-s              Skip rebuilding the HTML files for the examples (uses the existing ones)
-n <dir name>   Put the output into a directory named <dir name> instead
```
Note this does not include the tarballs for Extensibella and Sterling
by default, as it does not know where they are.
