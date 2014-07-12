perfectgift
-----------

A wishlist site for organising gift giving between friends (apparently a social network).
Written for the 2014 NCSS (by the always amazing Group 4).

## Usage ##
The recommended usage is through `docker`. However, you can run the server using the `wishlist.py`
script:

```
python3 ./server.py [-h] [-p PORT] [-H HOST]
```

The above script expects the database to have been initialised (which can be done by running `db/initdb.py`).

## License ##

### Code ###
This excludes external scripts and the `epyc/` project.

```
perfectgift: a tornado webapp for creating wish lists between friends
Copyright (C) 2014, NCSS14 Group 4

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Artwork and other works ###
The artwork and other non-code parts of this project are also Copyright (C) 2014, NCSS14 Group 4
and are licensed under the Creative Commons Attribution-ShareAlike 4.0 International License.
For more information, visit [this site](http://creativecommons.org/licenses/by-sa/4.0).
