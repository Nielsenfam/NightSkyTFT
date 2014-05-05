# NightSkyTFT Readme


# NigthSkyTFT Hardware

## Hardware Parts List

- Raspberry Pi Model A or B
- Adafruit 2.8 TFT https://www.adafruit.com/products/1601
- Wifi Dongle
- 5V 1A or greater Wall Wart with USB
- USB to USB micro cable
- Case for Raspberry Pi, see http://www.thingiverse.com/thing:233396
- Stand for Raspberry Pi see http://www.thingiverse.com/thing:254532

## Hardware needed for Setup only

- HDMI Monitor or other suitable monitor compatible with the Pi
- USB Keyboard
- USB Mouse
- USB Hub unless keyboard/mouse only need one USB port

# Software Setup

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

```
startx
```

## 7. setup wifi

Setup a wifi connection using gui tool on desktop

## 8. Update raspberrian


```
sudo apt-get update
sudo apt-get upgrade
```

## 9. Install vncserver 

This is not strictly necessary, but convenient since will be running headless.

```
sudo apt-get install tightvncserver
```

## 10. Setup python development

```
sudo apt-get install python-pip python-dev
```

## 11. get stuff for calculating ephem

Get stuff for calculating ephem by getting pyephem and pytz packages:

```
sudo pip install pyephem pytz
```

## 12. get git so we can get NightSkyTFT code 


```
sudo apt-get install git
```

## 13. Get the python code

get NightSkyTFT code from github

```
git clone http://github.com/Nielsenfam/NightSkyTFT
```

## 14. Get weather underground login key

Goto http://www.wunderground.com/weather/api/ and signup for a key. The key will be used in the setup parameters in the next step.

## 15. Setup parameters for NightSkyTFT

The NightSkyTFT settings are all stored in a file called params.py, these need to be modified as follows:

```
cd NightSkyTFT
cp params.py-template params.py
```

```
nano params.py 
```

### 15a. Set locations

You can setup up to three different locations, for each you will need to know the latitude, longitude, altitude and timezone. 

Set the parameters in the file for location 0, 1 and 2. For example, to setup the first location edit the following: 

```
lat[0] = 64.4186
lon[0] = -39.5153
alt[0] = 1000
tz[0] = 'US/Central'

```

### 15b. Setup the cleardarksky locations

The cleardarksky.com website provides simple text formated data as well as the graphic pages. The text file web page can be found from the graphical page. And has a format like:

http://cleardarksky.com/txtc/FlagstaffAZcsp.txt

The parameter should be set like this for each location:

```
clear_dark_sky_url[0]=http://cleardarksky.com/txtc/FlagstaffAZcsp.txt
```

### 15c. Set the weather pages

For each location, setup the weather underground location page like this:

```
wug_location[0] = "/q/ST/City.json"
```

### 15d. Set the weather underground key

Set the weather underground API key in the file by editing the value of wug_key like this:

```
wug_key = "xxxx"
```

### 15e. Test under X Windows

Set PiTFT to False and save the param.py file.

```
PiTFT = False
```

If you are running from a remote terminal or from the console, start your desktop environment with a startx and then start a terminal window cd to the NightSkyTFT directory and run the NightSkyTFTMain.py program, like this: 

```
cd NightSkyTFT
python ./NightSkyTFT.py
```

You should see an X window open showing the splash screen and then the main menu. Using the keyboard numbers for the menu choices, select weather, objects, sky conditions to see that they all work. Error messages will show up in the terminal window. 

Then toggle through the different locations, and confirm the weather, objects and sky conditions again to verify they all work.

If everythign is correct, edit the params.py file again and set PiTFT to True if running on Raspberry Pi with PiTFT that has 4 buttons on GPIO. Set to False if you do not have the buttons. 

```
PiTFT = True
```

## 16. Get TFT code

Get the code for driving the TFT screen from adafruit by doing the following:


```
cd ~
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-bin-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-dev-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi-doc-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/libraspberrypi0-adafruit.deb
wget http://adafruit-download.s3.amazonaws.com/raspberrypi-bootloader-adafruit-112613.deb

sudo dpkg -i -B *.deb
```


## 17. Setup console on the TFT display

This is also optional, but if you want the boot sequence to show up on the TFT display do this. 

First if you need to rotate the display, edit config.txt to rotate display 180 degrees

```
sudo vi /boot/config.txt
```

```
display_rotate=2
```

then edit the cmdlin.txt file:

```
sudo vi /boot/cmdline.txt
```


after rootwait add the following:


```
fbcon=map:10 fbcon=font:VGA8x8
```


## 18. Setup TFT modules


```
sudo modprobe spi-bcm2708
sudo modprobe fbtft_device name=adafruitts rotate=90
export FRAMEBUFFER=/dev/fb1 
sudo mv /usr/share/X11/xorg.conf.d/99-fbturbo.conf ~
startx
```


the startx is just a test, if it works, just quit if X windows desktop after it tarts on the TFT display


## 19. Make modules permanent

Now make modules permanent on boot by doing the following:


```
sudo vi /etc/modules
```


add these two lines:


```
spi-bcm2708
fbtft_device
```

## 20. Create modprobe.d file

```
sudo vi /etc/modprobe.d/adafruit.conf
```


add line:

```
 options fbtft_device name=adafruitts rotate=270 frequency=32000000
```


then reboot to see if it works:


```
sudo reboot
```

## 21. Starting up on boot

To mmke nightskyboot run on startup do the following:

```
cd ~/NightSkyTFT
sudo chmod +x nightskyboot
sudo cp nightskyboot /etc/init.d/
sudo update-rc.d nightskyboot defaults
```
