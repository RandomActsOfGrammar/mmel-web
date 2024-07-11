The `web` directory contains the actual web content.  The
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
-s               Skip rebuilding the HTML files for the examples (uses the existing ones)
-n <dir name>    Put the output into a directory named <dir name> instead
-ex <dir name>   Get the Extensibella distribution tarball by going to <dir name> and creating it
-st <dir name>   Get the Sterling distribution tarball by going to <dir name> and creating it
```
If the Extensibella and/or Sterling directories are given, it tries to
go to them and build the distribution tarballs and copy them into the
website.  If they are not given, it tries to find the directories as
siblings of this repository, that is, it expects the directory
structure to be
```
<parent dir>
  |- extensibella
  |- sterling
  |- mmel-web
```
Messages are printed at the end if the tarballs are not built and
added to the web directory.

To move the website to the hosting directory, run
```
./buildTools/place_web
```
By default this will copy from `full_web`; run it as
```
./buildTools/place_web <dir>
```
to use a different directory if you built into a different directory.
This will set the permissions correctly for you, but you need to be in
the correct group first.


----------------------------------------------------------------------


The `MMEL.drawio` document contains the drawings of the logos for the
pages here.  I believe this requires using [draw.io]() to view and to
extract the logos as images for use.  The logos used in the website
are also in the appropriate `images/` directories within the `web/`
directory.
