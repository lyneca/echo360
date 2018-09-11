import ffmpy
import os
import requests
import tempfile
import multiprocessing as mp
from tqdm import tqdm
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

base_url = url[:-13]

print("Getting url to chunk list...")
chunk_file = list(requests.get(url).iter_lines())[-1].decode()

print("Getting chunk list...")
chunk_list = requests.get(base_url + chunk_file)

out_file_string = b""

chunk_list = [x for x in chunk_list.iter_lines() if not x.decode().startswith('#')]

tmp_file = tempfile.mktemp()
print("Downloading chunks...")
for i, line in enumerate(tqdm(chunk_list)):
    line = line.decode()
    if not line.startswith('#'):
        chunk = requests.get(base_url + line).content
        with open(tmp_file, 'ab') as out:
            out.write(chunk)

print("Converting to .mp4 with ffmpeg...")


ffmpeg.input(tmp_file).output(name, acodec='copy', vcodec='copy').run()

print("Done. Output to {}.".format(name))
