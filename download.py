print("Instructions:")
print(" Step 1: Get the link")
print("   - Get a plugin that lets you emulate a mobile device") 
print("     Chrome: Use the Chrome DevTools Device Mode") 
print("     Firefox: The Mobile View Switcher plugin works")
print("   - Open the Echo360 link, and press F12. Find the link to the video playlist.")
print("     It will end with '.m3u8'.")
print(" Step 2: Enter the URL you copied here: ")
url = input("> ")
print()

base_url = url[:-13]

print("Getting url to chunk list...")
chunk_file = list(requests.get(url).read_lines())[-1].decode()

print("Getting chunk list...")
chunk_list = requests.get(base_url + chunk_file)

out_file_string = ""

bar = progressbar.ProgressBar()

print("Downloading chunks...")
for line in bar(chunk_file.read_lines()):
    line = line.decode()
    if not line.startswith('#'):
        chunk = requests.get(base_url + line).content()
        out_file_string += chunk

print("Writing to file...")
with open('out.ts', 'x') as out:
    out.write(out_file_string)
