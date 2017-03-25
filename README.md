# Auto latex generator for counters

## Usage:
1. Test if you have necessary packages:
   ```bash
   $ which pdflatex
   $ which convert
   ```
   If you don't have it, install it. The program convert is part of the imagemagick package, thus to install both packages i.e. on Debian you will have to run command `apt install imagemagick pdflatex` as `root`.


1. Create virtualenv and install python packages:
   ```bash
   $ virtualenv -p python3.5 counter-env3
   $ . counter-env3/bin/activate
   $ pip install -r requirements.txt
   ```

1. Run server:
   ```bash
   $ cd web
   $ python server.py &
   ```

1. Visit site: `0.0.0.0:5000` in your browser.
1. Enjoy :)
