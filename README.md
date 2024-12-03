Caitlin Sullivan (<ccsulliv@usc.edu>) | Isabella Samardzic (<samardzi@usc.edu>)

# EE 250 Final Project: RPi Digital Lock 

## Getting Started
**1. Install requirements.txt on your primary device or VM**

    pip install -r requirements.txt
    

**2. Prepare HTTPS**

- Create a new directory in `Main` called `keys`, and cd into it in a terminal. 
- When inside this directory, generate your RSA key pair using a self-signed certificate:

      openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.keys -out server.crt

- Skip all the special inputs by hitting the return key.
  

**3. On your Raspberry Pi:**

- SSH into your RPi. 
- Clone this repository there if you have not already.
- Ensure requirements are installed, including GrovePi. You can rerun `requirements.txt`, but that does not include the GrovePi suite, 
since it is very extensive.
- Connect the GrovePi to the RPi and attach the radial potentiometer to port `A0`.
- run  `rpi_pubsub.py` on the Rasperry Pi:

      python rpi_pubsub.py

**4. On your main OS or VM:**

- from `Main`, you will need **two additional terminal windows** open, for (1) the main host, and (2) server.py.
  Thus you will have **three windows in total**.
- start the MQTT client and the HTTPS server in separate terminals:

      python3 vm_pubsub.py
      python3 server.py

Once HTTPS is connected, Raw JSON data can be accessed on port 3000 at <https://localhost:3000/api>

Formatted live-update data is available at <https://localhost:3000/>


## Using the Application
The HTTPS server is just for displaying data. all user inputs will be managed through the main script, `vm_pubsub.py`. 
You should have this terminal open to type in.

- turn the potentiometer to change the current selected number 0-9.
- the current number will be printed in `rpi_pubsub.py` and visible on the HTTPS client (refresh rate: 2/sec).
- to lock in the current number, press the "a" key in `vm_pubsub.py`, or use the "enter" button on the frontend.
- to reset your progress and clear the input code, press the "d" key in `vm_pubsub.py` or use the "reset" button on the frontend.
- if you get the sequence correct (compared to the key specified in `vm_pubsub.py`), the lock will unlock. It will lock and reset if you get
  the sequence wrong. you can also reset anytime by locking in the number 0.

## Project Requirements

1. At least two physical nodes (such as laptop, rpi and cloud)...3 is preferred but you can get credit with just 2.
  - Laptop
  - RPi
  - HTTPS visualizer on localhost (does this count as another node if virtual?)
  
2. Data collection - Should be from at least 2 sensors. Sensors can be actual sensors (GrovePi) or a ‘virtual’ sensor could generate
   simulated data or use a public data API
  - GrovePI Potentiometer
  - Keyboard
  
3. Signal or data processing (in real time), some simple ML, or secure communications (encryption, etc.) - While our lecture focused on conversion
   to the frequency domain, it is likely easiest to do some filtering or "event detection" in the time domain. Some simple queries from the user
   interface may be answered through ML techniques. If your processing is simple, please add encryption and/or digital signatures to meet this requirement when transmitting information.
  - MQTT encrypted with TLS
  - HTTPS encrypted with RSA one-way
  - Threaded event detection on keyboard in `vm_pubsub`  

4. Node-to-node communication - Data must be transferred between the nodes (meaning you can’t do everything on one node like your laptop). You can use any cloud components, such as AWS IoT, EC2 etc.
  - RPi -- MQTT --> host OS
  - host OS -- HTTPS --> socket with html web client

5. Visualization and/or control.  Should be a simple web front end, use of Grafana for visualization, or other user interface.
  - using index.html with persistent GET to display JSON information from `vm_pubsub.py` 
