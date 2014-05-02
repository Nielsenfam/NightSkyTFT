
# Hardware for NigthSkyTFT:

## Hardware Parts List

- Raspberry Pi Model A or B
- Adafruit 2.8 TFT https://www.adafruit.com/products/1601
- Wifi Dongle
- 5V 1A or greater Wall Wart with USB
- USB to USB micro cable
- Case for Raspberry Pi, see http://www.thingiverse.com/thing:233396
- Stand for Raspberry Pi see http://www.thingiverse.com/thing:254532

## Hardware needed for Setup only:

- HDMI Monitor or other suitable monitor compatible with the Pi
- USB Keyboard
- USB Mouse
- USB Hub unless keyboard/mouse only need one USB port

# How to setup a RaspberryPi to run the NightSkyTFT software:

## 1. format SD card 

Format the SD card with a FAT filesystem. Use SDFormatter or equivalent depending on platform.


## 2. Download NOOBs 

Download the NOOBs zip file from: [http://www.raspberrypi.org/downloads](http://www.raspberrypi.org/downloads)

## 3. Unzip and copy to SD card

Unzip the downloaded file and copy to the SD card.

## 4. Boot the card on the Raspberry Pi

Move the SD card to Raspberry Pi and boot, follow instructions to install raspberian

## 5. Configure the Operating System

Use the menus of the Raspi-config to select for language, keyboard, monitor, timezone, enable ssh login, and any other settings you desire. Do not select boot to desktop. 

## 6. login to the Raspberry Pi

Using the local keyboard and a monitor login and start X Windows GUI: 

---
startx
---

## 7. setup wifi

Setup a wifi connection using gui tool on desktop

## 8. Update raspberrian:

---

sudo apt-get update
sudo apt-get upgrade
---

## 9. Install vncserver (not strictly necessary, but convenient since will be running headless)

---
sudo apt-get install tightvncserver
---

## 10. Setup python development:

---
sudo apt-get install python-pip python-dev
---

## 11. get stuff for calculating ephem by getting pyephem and pytz packages:

---
sudo pip install pyephem pytz
---

## 12. get git so we can get NightSkyTFT code: 

---

sudo apt-get install git
---

## 13. get NightSkyTFT code from github:

---
git clone http://github.com/Nielsenfam/NightSkyTFT
---

## 14. Get weather underground login key

Goto http://www.wunderground.com/weather/api/ and signup for a key. The key will be used in the setup parameters in the next step.

## 15. Setup parameters for NightSkyTFT

---
cd NightSkyTFT
cp params.py-template params.py

nano params.py 
---

### 15a. Set locations.

You can setup up to three different locations, for each you will need to know the latitude, longitude and altitude set the parameters in the file for location 0, 1 and 2: 


---

lat[0] = 64.4186
lon[0] = -39.5153


alt[0] = 1000
---

### 15b. Set the weather underground keys:

---
wug_key = "xxxx"
---

### 15c. Set the start screen:

??

### 15d. Turn on/off buttons:

??

### 15e. Setup the cleardarksky locations:

??

### 15f. Save parameters file



## 16. Get the code for driving the TFT screen from adafruit:


  1. ---
  2. cd ~
  3. wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-bin-adafruit.deb
  4. wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-dev-adafruit.deb
  5. wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-doc-adafruit.deb
  6. wget http://adafruit-download.s3.amazonaws.com/libraspberrypi0-adafruit.deb
  7. wget http://adafruit-download.s3.amazonaws.com/raspberrypi-bootloader-adafruit-112613.deb

sudo dpkg -i -B *.deb
---


## 17. If you want the boot sequence to show up on the TFT display, edit config.txt to rotate display 180 degrees

---
sudo vi /boot/config.txt
---



add line at end:


---
display_rotate=2
---


then edit the codlin.txt file:


---

sudo vi /boot/cmdline.txt
---


after rootwait enter:


---
fbcon=map:10 fbcon=font:VGA8x8
---


## 18. Setup TFT modules:


---
sudo modprobe spi-bcm2708
sudo modprobe fbtft_device name=adafruitts rotate=90
export FRAMEBUFFER=/dev/fb1 
sudo mv /usr/share/X11/xorg.conf.d/99-fbturbo.conf ~
startx
---


the starts is just a test, quit if X windows desktop starts on TFT display


## 19. Now make modules permanent on boot:


---
sudo vi /etc/modules

---


add these two lines:

---
spi-bcm2708
fbtft_device
---

## 20. Create modprobe.d file:

---
sudo vi /etc/modprobe.d/adafruit.conf
---


add line:

---
 options fbtft_device name=adafruitts rotate=270 frequency=32000000
---


then reboot to see if it works:


---
sudo reboot
---

## 21. Make nightskyboot run on startup

---
cd ~/NightSkyTFT
sudo chmod +x nightskyboot
sudo cp nightskyboot /etc/init.d/
sudo update-rc.d nightskyboot defaults
---
