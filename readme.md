# HoverPractice

This is a practice tool for doing the [Hover glitch][] in The Legend Of Zelda: A
Link To The Past.

[Download the Windows version here][download] (get the latest file that doesn't
have "source code" in the name). This tool also works on MacOS; see later in this readme for details.

[Hover glitch]: https://www.alttp-wiki.net/index.php/Hovering
[download]: https://www.alttp-wiki.net/index.php/Hovering

## How to use

In order to hover, you have to press your dash button for 30 or fewer frames,
then release that button for one single frame before pressing it again, and
then repeat this process until you're done hovering. Normally people do this by
scraping two fingernails back and forth across the button; the gap in between
the fingers is when the button gets released.

The tool draws two bars for each time you press the dash button. On top, it
shows you how long you held down the button. Below, it shows you how long you
had the button released. If both bars are green, that means you did a
successful hover input. The goal is to reliably have long stretches of all
green.

Each time you start the tool, it asks what your dash button is. You can use any
controller button or keyboard key.  If you use a controller, you can also press
down on a dpad or stick to see Link move.

![](https://i.imgur.com/FcgMSfp.gif)

## Local macOS

HoverPractice can run on macOS but no downloadable builds are available at the
moment. If you want to run this tool on macOS you will need to install
[Homebrew][] and run the following commands in your terminal:

```console
$ brew install git python sdl sdl_ttf sdl_image
$ git clone https://github.com/Hyphen-ated/HoverPractice
$ cd HoverPractice
$ pip3 install virtualenv
$ virtualenv ./env
$ source env/bin/activate
$ pip install --no-cache-dir -r requirements.txt
$ python src/hoverpractice.py
```

[Homebrew]: https://brew.sh/
