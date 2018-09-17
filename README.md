# SafetyNet
---
## About
SafetyNet is a drone network framework for coordinating search and rescue teams after natural disasters.  It uses OpenCV in tandem with the Watson Visual Recognition API to find survivors.  Then, it uses the Google Maps API to mark their location for rescuers.  Built for HackMIT 2018.

## Installation
SafetyNet is currently in its protoype stage.  Thus, this is for demonstration purposes only.  It requires OpenCV, Node.js, a Watson API key, and a Google Maps API key.  You will need to put your Watson API key inside the file `drone/api.key` (you must create this file).  Additionally, a MAMP server is needed for image streaming (if desired).

First, clone the repository using `git clone https://github.com/mihirbala/SafetyNet.git`

Then, from the repository, run `node server/server.js`

Finally, run `python drone/cascade.py -i TEST_VIDEO_HERE -g GEOTAG_FILE_HERE`

By default, the server runs on port 3000.
