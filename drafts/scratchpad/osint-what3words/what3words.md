#### A narration of how I found the flag

- Expecting that this is an OSINT, it is highly likely the picture contains relevant metadata that will help point to the flag
- Using the `exiftool` command at my Fedora Machine, it outputs an ironic comment:
	``` If you're looking here, then you've searched yourself into a wrong hole.```
-  I thought maybe this is a red-herring.  It is possible that it is misleading me from checking other parts of the metadata.
- Upon further inspection, nothing out-of-ordinary came out of the picture.
- However, I found the title of the image quite peculiar. It is made up of three (3) words with no articles in between, which points me exactly to what3words.com
- I searched the words (`treasure.hunt.trip`) through the website and found an empty location.
- I clicked on the navigate bar then to the Google maps and found the coordinates, which are the flag itself
- Converted them to DMS by searching them up again on Google Maps
- `PacketCapture{85.36, 81.05}`

- What I learned:
	- Any anomaly is something to take note of
	- Use online-available tools to improve efficiency
	- Learn to read file metadata (example, using exiftools via the terminal)