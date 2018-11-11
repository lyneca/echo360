# Echo360 Downloader

Echo360 is a video hosting site.
It actively makes viewing videos much harder than it should be,
by using ~dark rituals~ Flash and other deprecated technologies.

This script allows you to download the videos for offline use.

**NOTE**: Under the MIT license, I do not endorse nor take liability for the downloading of copyrighted content.
This is intended as a proof of concept; use this software at your own risk.

## Requirements

### Python Requirements

You need Python 3 to run this script.
`requirements.txt` contains the Python packages that are needed.

You can run 
```bash
pip3 install -r requirements.txt
```
to install them automatically.  

### FFmpeg

This program will not work without [FFmpeg](https://ffmpeg.org) installed
and available on your path. If you're not sure how to do this on Windows,
there are instructions available [here](http://adaptivesamples.com/how-to-install-ffmpeg-on-windows).

On OSX, `brew install ffmpeg` will work fine, and on Linux, use your package manager of choice.

## Usage

The hardest part is getting the _playlist URL_. So far, the easiest way I've
found is as follows:

1.  On Chrome/Firefox, go to the page you want to download
2.  Devtool > Network
3.  Click play, you should see GET requests
4.  The request URLs will be start with `delivery.streaming.<server>/echo/<4 digits>/<a number>/<long UUID>/` that's what you want

If you have any issues, feel free to [submit an issue on Github](https://github.com/lyneca/echo360/issues/new).

If you find another way to get the delivery URL that is easier than this one, _*PLEASE MAKE AN ISSUE!*_ I'd love to know!
