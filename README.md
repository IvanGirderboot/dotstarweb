# dotstarweb

DotStar Web is a simple API server with built-in web client to control DotStar RGB LED strips.
It is designed to be lightweight and deployable to any device with locally connected dotstar strips, e.g. a Raspberry Pi)

## Installation

Installation is simple using a virtual python3 environment:

1. Clone the repo: `git clone https://github.com/IvanGirderboot/dotstarweb.git`
2. In the source directly, create a Python virtual environment: `python3 -m venv venv`
3. Activate the virtual python environment: `source venv/bin/activate`
4. Install the necessary python modules: `python3 -m pip install -r requirements.txt`
5. Start the API server: `uvicorn api:app`
