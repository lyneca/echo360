#!/usr/bin/env python
"""
Todo: add back module level doc
"""

import ffmpeg
import os
import requests as r
import tempfile
import argparse
import concurrent.futures as cf


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

url = 'http://delivery.streaming.sydney.edu.au:1935/echo/_definst_/{}/mp4:audio-vga-streamable.m4v/playlist.m3u8'
base_url = url[:-13]

print("Getting url to chunk list...")
chunk_file = list(r.get(url).iter_lines())[-1].decode()

print("Getting chunk list...")
chunk_list = r.get(base_url + chunk_file)

out_file_string = b""

chunk_list = [x for x in chunk_list.iter_lines() if not x.decode().startswith('#')]

tmp_file = tempfile.mktemp()

print("Downloading chunks...")
with cf.ThreadPoolExecutor(max_workers=20) as ex:
    promises = [
        ex.submit(r.get, base_url + line.decode)
        for line in chunk_list if not line.decode.startswith('#')
    ]
    for p in promises:
        with open(tmp_file, 'ab') as out:
            out.write(p.result().content)

print("Converting to .mp4 with ffmpeg...")
ffmpeg.input(tmp_file).output(name, acodec='copy', vcodec='copy').run()

print("Done. Output to {}.".format(name))
