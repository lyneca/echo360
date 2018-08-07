import ffmpeg
import sys
import requests
import tempfile
import progressbar
import argparse

instructions = """Instructions:
  Step 1: Get the link
    - Get a plugin that lets you emulate a mobile device
      Chrome: Use the Chrome DevTools Device Mode
      Firefox: The Mobile View Switcher plugin works
    - Open the Echo360 link, and press F12. Find the link to the video playlist.
      It will end with '.m3u8'.
    - If you need more instructions, look at the readme:
      https://github.com/lyneca/echo360"""

parser = argparse.ArgumentParser(description=instructions)
parser.add_argument("-link", "-l", type=str)
parser.add_argument("-output", "-o", type=str)

args = parser.parse_args()

if not args.link:
    print(instructions)
    print("  Step 2: Enter the URL you copied here: ")
    url = input("> ")
else:
    url = args.link

if not args.output:
    print("  Step 3: What is the output file name?")
    name = input("> ")
else:
    name = args.output

vid_id = url.split('/')[-1].split('?')[0]

url = "http://delivery.streaming.sydney.edu.au:1935/echo/_definst_/1831/{{}}/{}/mp4:audio-vga-streamable.m4v/playlist.m3u8".format(vid_id)
base_url = ''

for i in range(13):
    temp_url = url.format(i)
    base_url = temp_url[:-13]

    print("Getting url to chunk list... (trying option #{})".format(i))
    try:
        chunk_file = list(requests.get(temp_url).iter_lines())[-1].decode()
    except IndexError:
        continue
    break
else:
    print("Couldn't figure out URL :(")
    sys.exit(0)

print("Getting chunk list...")
chunk_list = requests.get(base_url + chunk_file)

out_file_string = b""

bar = progressbar.ProgressBar()

chunk_list = [x for x in chunk_list.iter_lines() if not x.decode().startswith('#')]

print("Downloading chunks...")
for line in bar(chunk_list):
    line = line.decode()
    if not line.startswith('#'):
        chunk = requests.get(base_url + line).content
        out_file_string += chunk

tmp_file = tempfile.mktemp()
print("Writing to file...")
with open(tmp_file, 'xb') as out:
    out.write(out_file_string)

print("Converting to .mp4 with ffmpeg...")

ffmpeg.input(tmp_file).output(name, acodec='copy', vcodec='copy').run()

print("Done. Output to {}.".format(name))
