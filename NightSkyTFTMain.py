import pygame
from pygame.locals import *
from sys import exit
import os
import time
from time import strftime

#
# modules used to calculate object positions
#
import ephem
import pytz
import datetime

import urllib2
import json
import StringIO

#
# paramaters for location and options 
#
import params

## if running on RPi with a PiTFT
##   search for all PiTFT comments and do as instructed


## PiTFT: (uncomment) 
##import RPi.GPIO as GPIO

#
# function to calculate if night sky object is visible in a given hour
#
def calc_status( rise_tm, set_tm, clocktm ):

    #
    # function to calculate the clock light status based upon rise and set time for a given hour
    #
    # 6 possible cases, truth table:
    #    
    #  First Second Last   Display
    # 1  RT    ST     CL      OFF     
    # 2  ST    RT     CL      ON
    # 3  RT    CL     ST      ON
    # 4  ST    CL     RT      OFF
    # 5  CL    ST     RT      ON
    # 6  CL    RT     ST      OFF
    #
    # key:
    #   RT = rise date/time
    #   ST = set date/time
    #   CL = clock date/time being evaluated

    # 1. case where rise time is before set time
    #     and the set time is before the clock time
    #
    if ( rise_tm < set_tm and
         set_tm < clocktm ):
        clock_status = "off"
        #print "case 1:", clock_status

    # 2. case where set time is before the rise time
    #     and rise time is before the clock time
    if ( set_tm < rise_tm and
         rise_tm < clocktm ):
        clock_status = "on"
        #print "case 2:", clock_status

    # 3. case where rise time is before the clock time
    #     and clock time is before the set time
    if ( rise_tm < clocktm and
         clocktm < set_tm ):
        clock_status = "on"
        #print "case 3:", clock_status

    # 4. case where set time is before clock time
    #     and the clock time is before the rise time
    #
    if ( set_tm < clocktm and
         clocktm < rise_tm ):
        clock_status = "off"
        #print "case 4:", clock_status

    # 5. case where clock time is before the set time
    #     and set time is before the rise time
    if ( clocktm < set_tm and
         set_tm < rise_tm ):
        clock_status = "on"
        #print "case 5:", clock_status

    # 6. case where clock time is before the rise time
    #     and rise time is before the set time
    if ( clocktm < rise_tm and
         rise_tm < set_tm ):
        clock_status = "off"
        #print "case 6:", clock_status

    return clock_status

#
# function to display hour columns
#
def dispHourCols():

        hourx = 0
        houry = 38
        
        hour_label = font.render("Hour:", True, (255,255,255))
        screen.blit(hour_label, (hourx, houry))
    
        hourx = 60
        xinc = 20
        for col in (5,6,7,8,9,10,11,12,1,2,3,4,5):
            hour_col = font.render( str(col), True, (255,255,255))
            screen.blit(hour_col, (hourx, houry))
            hourx = hourx + xinc
#
# function to display title
#
def dispTitle(title_text):

    title_font_size = 32
    title_font = pygame.font.SysFont(None, title_font_size)

    line_surface = title_font.render(title_text, True, (0,0,255))
    linerect = line_surface.get_rect()
    x = background.get_rect().centerx - linerect.width /2
    screen.blit(line_surface, (x,0))
    
#
# Display Main Menu and Description
#
def dispMain():

    title_txt = "Main Menu"
    dispTitle(title_txt)
#
# Display astronomy object details
#
def dispDetails():

    title_txt = "Details"
    dispTitle(title_txt)

    # explain that it is not implemented
    details_font = pygame.font.SysFont(None, 32)
    details_surface = details_font.render("Not Implemented", \
                                        True, (255,0,0))
    details_rect = details_surface.get_rect()
    x = background.get_rect().centerx - details_rect.width/2
    y = background.get_rect().centery
    screen.blit(details_surface, (x,y) )

#
# Display Sky conditions for tonight
#   based upon clear dark sky chart 
#
def dispSky():
                                                               
    cloud_d = {}
    transp_d = {}
    seeing_d = {}
    wind_d = {}
    humidity_d = {}
    temp_d = {}
                    

    title_txt = "Sky"
    dispTitle(title_txt)

    dispHourCols()

    # Get the html page from www.cleardarksky.com
    url  = params.clear_dark_sky_url

    # Get the data in text version

    try: req = urllib2.Request(url)
    except:
        print "failed to request url: ", url
        fail_font = pygame.font.SysFont(None, 32)
        fail_surface = fail_font.render("No Sky Data Available", \
                                        True, (255,0,0))
        fail_rect = fail_surface.get_rect()
        x = background.get_rect().centerx - fail_rect.width/2
        y = background.get_rect().centery
        screen.blit(fail_surface, (x,y) )

        return
        
    try: response = urllib2.urlopen(req)
    except:
        print "failed to open url: ", url
        fail_font = pygame.font.SysFont(None, 32)
        fail_surface = fail_font.render("No Sky Data Available", \
                                        True, (255,0,0))
        fail_rect = fail_surface.get_rect()
        x = background.get_rect().centerx - fail_rect.width/2
        y = background.get_rect().centery
        screen.blit(fail_surface, (x,y) )

        return
        
    data = response.read()
    data = data.split("blocks = (\n")
    data_table = data[1].splitlines()

    # current date
    now = datetime.date.today()

    # tomorrows date
    tomorrow = now + datetime.timedelta(days=1)

    # loop over rows
    for line in data_table:
        if ( line[0:1] != "#" ):
            cols = line.split(",")

            datestring1 = cols[0].split("\"")[1]
            datestruct = time.strptime(datestring1,'%Y-%m-%d %H:%M:%S')

            # if today and 5PM or later
            if (datestruct.tm_year == now.year and 
                datestruct.tm_mon == now.month and
                datestruct.tm_mday == now.day ):

                if ( datestruct.tm_hour > (16) ):   
                    # print "todays hour, cloud, transp, seeing, wind, hum, temp : ", \
                    #      datestruct.tm_hour, cols[1], cols[2], cols[3], \
                    #      cols[4], cols[5], cols[6]
                    cloud_d[datestruct.tm_hour] = cols[1]
                    transp_d[datestruct.tm_hour] = cols[2]
                    seeing_d[datestruct.tm_hour] = cols[3]
                    wind_d[datestruct.tm_hour] = cols[4]
                    humidity_d[datestruct.tm_hour] = cols[5]
                    temp_d[datestruct.tm_hour] = cols[6]

            # if tomorrow and before 5AM
            if (datestruct.tm_year == tomorrow.year and 
              datestruct.tm_mon == tomorrow.month and
              datestruct.tm_mday == tomorrow.day ): 

                if ( datestruct.tm_hour < 6):   
                    # print "tomorrows hour, cloud, transp, seeing: ", \
                    #    datestruct.tm_hour, cols[1], cols[2], cols[3]
                    cloud_d[datestruct.tm_hour] = cols[1]
                    transp_d[datestruct.tm_hour] = cols[2]
                    seeing_d[datestruct.tm_hour] = cols[3]
                    wind_d[datestruct.tm_hour] = cols[4]
                    humidity_d[datestruct.tm_hour] = cols[5]
                    temp_d[datestruct.tm_hour] = cols[6]

            # if we got to 5AM tomorrow we are done
            if (datestruct.tm_year == tomorrow.year and 
              datestruct.tm_mon == tomorrow.month and
              datestruct.tm_mday == tomorrow.day ): 
              if ( datestruct.tm_hour == 6):   
                  break

    y = 38 + 3*16 - 8
    xinc = 20
    yinc = 16
    for row in ( "clouds","transp","seeing","wind","humid","temp" ):
        x = 0
        row_label = font.render( row, True, (255,255,255))
        screen.blit(row_label, (x,y-8))
        x = 65 - 6
        for hr in (17,18,19,20,21,22,23,0,1,2,3,4,5):

            shade = (0,0,0)
            if row == "clouds":
                if hr in cloud_d:
                    shade = params.cloud_shades[ int(cloud_d[hr])]
            elif row == "transp":
                if hr in transp_d:
                    shade = params.transp_shades[ int(transp_d[hr])]
            elif row == "seeing":
                if hr in seeing_d:
                    shade = params.seeing_shades[ int(seeing_d[hr])]
            elif row == "wind":
                if hr in wind_d:
                    shade = params.wind_shades[ int(wind_d[hr])]
            elif row == "humid":
                if hr in humidity_d:
                    shade = params.humidity_shades[ int(humidity_d[hr])]
            elif row == "temp":
                if hr in temp_d:
                    shade = params.temp_shades[ int(temp_d[hr])]
                
            # print "x, y, shade =", x, y, shade

            box = pygame.Rect(x,y-8,18,14)                
            pygame.draw.rect(screen, shade, box )

            x = x + xinc
        y = y + yinc 

#
# display current weather conditions
#
def dispWeather():

    title_txt = "Current Weather"
    dispTitle(title_txt)

    url = params.wug_url_base + params.wug_key + \
                        params.wug_conditions + params.wug_location
    try: f = urllib2.urlopen(url)
    except:
        print "failed to request url: ", url
        fail_font = pygame.font.SysFont(None, 32)
        fail_surface = fail_font.render("No Weather Data Available", \
                                        True, (255,0,0))
        fail_rect = fail_surface.get_rect()
        x = background.get_rect().centerx - fail_rect.width/2
        y = background.get_rect().centery
        screen.blit(fail_surface, (x,y) )
        return        

    json_string = f.read()
    parsed_json = json.loads(json_string)

    if 'current_observation' in parsed_json:
        observation = parsed_json['current_observation']
    else:
        print "no observation data at url: ", url
        fail_font = pygame.font.SysFont(None, 32)
        fail_surface = fail_font.render("No Weather Data Found", \
                                        True, (255,0,0))
        fail_rect = fail_surface.get_rect()
        x = background.get_rect().centerx - fail_rect.width/2
        y = background.get_rect().centery
        screen.blit(fail_surface, (x,y) )
        return        
        
    location = observation['display_location']['city']
    temp_f = observation['temp_f']
    wind_dir = observation['wind_dir']
    wind_mph = observation['wind_mph']
    dewpoint = observation['dewpoint_f']
    visibility = observation['visibility_mi']
    weather = observation['weather']
    icon_url = observation['icon_url']

    # print location, weather
    # print "temp and wind:", temp_f, wind_dir, wind_mph
    # print "dewpoint and visability", dewpoint, visibility
    # print "icon", icon_url

    bg_rect = background.get_rect()

    # display location under title in large font
    location_font_size = 32
    location_font = pygame.font.SysFont(None, location_font_size)

    loc_surface = location_font.render(location, True, (255,0,0))
    loc_rect = loc_surface.get_rect()
    x = bg_rect.centerx - loc_rect.width /2
    screen.blit(loc_surface, (x,32))

    data_font_size = 22
    data_font = pygame.font.SysFont(None, data_font_size)
    data_color = (255,255,255)

    # put icon in middle of screen
    stream = urllib2.urlopen(icon_url)
    buffer = StringIO.StringIO(stream.read())
    image_surface = pygame.image.load(buffer)
    image_rect = image_surface.get_rect()
    screen.blit(image_surface, (bg_rect.centerx \
                                        - image_rect.width/2, \
                                bg_rect.centery \
                                        - image_rect.height/2)) 

    # put weather description under icon
    weather_surface = data_font.render(weather, True, data_color)
    weather_rect = weather_surface.get_rect()
    x = bg_rect.centerx - weather_rect.width/2
    y = bg_rect.centery + image_rect.height/2 + 40
    screen.blit(weather_surface, (x,y) )

    # draw data on screen                                   
    data_row_dy = 25
    data_row_y = 70

    data_col1_center = background.get_rect().centerx \
                       - background.get_rect().width/4
    data_col3_center = background.get_rect().centerx \
                       + background.get_rect().width/4

    # temperature label
    temp_surface = data_font.render("Temp:", True, data_color)
    temp_rec = temp_surface.get_rect()
    x = data_col1_center - temp_rec.width/2
    y = data_row_y    
    screen.blit(temp_surface, (x,y))

    # dewpoint label
    dewpoint_surface = data_font.render("Dew Point:", True, data_color)
    dewpoint_rec = dewpoint_surface.get_rect()
    x = data_col3_center - dewpoint_rec.width/2
    screen.blit(dewpoint_surface, (x,y))

    # tempurature value
    temp_surface = data_font.render(str(temp_f) + " F",True, data_color)
    temp_rec = temp_surface.get_rect()
    x = data_col1_center - temp_rec.width/2
    y = y + data_row_dy
    screen.blit(temp_surface, (x,y))
    dewpoint_rec = dewpoint_surface.get_rect()

    # dewpoint value
    dewpoint_surface = data_font.render(str(dewpoint) + " F", True, data_color)
    dewpoint_rec = dewpoint_surface.get_rect()    
    x = data_col3_center - dewpoint_rec.width/2
    screen.blit(dewpoint_surface, (x,y))

    # wind label
    wind_surface = data_font.render("Wind:", True, data_color)
    wind_rec = wind_surface.get_rect()
    x = data_col1_center - wind_rec.width/2
    y = y + data_row_dy + 10
    screen.blit(wind_surface, (x,y))

    # visibility label
    visib_surface = data_font.render("Visibility:", True, data_color)
    visib_rec = visib_surface.get_rect()
    x = data_col3_center - visib_rec.width/2
    screen.blit(visib_surface, (x,y))

    # wind value line 1
    wind_surface = data_font.render( wind_dir + " at ", True, data_color)
    wind_rec = wind_surface.get_rect()
    x = data_col1_center - wind_rec.width/2
    y = y + data_row_dy
    screen.blit(wind_surface, (x,y))

    # visibility value
    visib_surface = data_font.render(str(visibility) + " mi", True, data_color)
    visib_rec = visib_surface.get_rect()
    x = data_col3_center - visib_rec.width/2
    screen.blit(visib_surface, (x,y))

    # wind value line 2
    wind_surface = data_font.render(str(wind_mph) + " mph", True, data_color)
    wind_rec = wind_surface.get_rect()
    x = data_col1_center - wind_rec.width/2
    y = y + data_row_dy - 10
    screen.blit(wind_surface, (x,y))    

#
# not used, but intended to show hourly weather data
#
def dispWeatherHourly():

    title_txt = "Hourly Weather"
    dispTitle(title_txt)

    dispHourCols()

    yinc = 16
    houry = 38 + 2*yinc           
    xinc = 20
    for row in (range(0,8)):
        hourx = 60
        for col in (5,6,7,8,9,10,11,12,1,2,3,4,5):
            hour_col = font.render( str(row), True, (255,255,255))
            screen.blit(hour_col, (hourx, houry))
            hourx = hourx + xinc
        houry = houry + yinc

#    
# display night sky objects that are visible tonight
#
def dispObjs():

    title_txt = "Objects"
    dispTitle(title_txt)

    dispHourCols()

    # local inforamtion parameterized
    lat = params.lat
    lon = params.lon
    alt = params.alt
    tz = params.tz

    # time of clock start and end in military time
    clock_start_hr = 17
    clock_end_hr = 5


    # dictonary for rise, set times
    set_tm_d = {}
    rise_tm_d = {}

    # use time of 4PM today for all calculations so that it always gets next rise and set times for this evening

    mytz = pytz.timezone(tz)
    eptz = pytz.timezone('utc')

    now = datetime.date.today()
    afternoon = mytz.localize( datetime.datetime(now.year,now.month,now.day)+ datetime.timedelta(hours=16))
    eptafternoon = afternoon.astimezone(eptz)
    # print "eptafternoon", eptafternoon

    # define objects
    sun = ephem.Sun()
    moon = ephem.Moon()
    venus = ephem.Venus()
    mars = ephem.Mars()
    jupiter = ephem.Jupiter()
    saturn = ephem.Saturn()

    # setup current location
    here = ephem.Observer()
    here.lon = str(lon)
    here.lat = str(lat)
    here.elev = alt
    here.date = eptafternoon
    # print here

    # compute objects based upon current location
    sun.compute(here)
    moon.compute(here)
    venus.compute(here)
    mars.compute(here)
    jupiter.compute(here)
    saturn.compute(here)

    sun_r = ephem.localtime(here.next_rising(sun))
    sun_s = ephem.localtime(here.next_setting(sun))
    rise_tm_d[ "sun" ] = sun_r
    set_tm_d[ "sun" ] = sun_s

    moon_r = ephem.localtime(here.next_rising(moon))
    moon_s = ephem.localtime(here.next_setting(moon))
    rise_tm_d[ "moon" ] = moon_r
    set_tm_d[ "moon" ] = moon_s

    venus_r = ephem.localtime(here.next_rising(venus))
    venus_s = ephem.localtime(here.next_setting(venus))
    rise_tm_d[ "venus" ] = venus_r
    set_tm_d[ "venus" ] = venus_s

    mars_r = ephem.localtime(here.next_rising(mars))
    mars_s = ephem.localtime(here.next_setting(mars))
    rise_tm_d[ "mars" ] = mars_r
    set_tm_d[ "mars" ] = mars_s

    jupiter_r = ephem.localtime(here.next_rising(jupiter))
    jupiter_s = ephem.localtime(here.next_setting(jupiter))
    rise_tm_d[ "jupiter" ] = jupiter_r
    set_tm_d[ "jupiter" ] = jupiter_s

    saturn_r = ephem.localtime(here.next_rising(saturn))
    saturn_s = ephem.localtime(here.next_setting(saturn))
    rise_tm_d[ "saturn" ] = saturn_r
    set_tm_d[ "saturn" ] = saturn_s

    ## print "sun r,s:", sun_r, sun_s
    ## print "moon r,s:", moon_r, moon_s
    ## print "venus r,s:", venus_r, venus_s 
    ## print "mars r,s:", mars_r, mars_s
    ## print "jupiter_r,s:", jupiter_r, jupiter_s
    ## print "saturn_r,s:", saturn_r, saturn_s

    y = 38 + 3*16
    xinc = 20
    yinc = 16
    for objs in ( "sun","moon","venus","mars","jupiter","saturn" ):
        x = 0
        obj_label = font.render( objs, True, (255,255,255))
        screen.blit(obj_label, (x,y-8))
        x = 65
        for hr in (17,18,19,20,21,22,23,0,1,2,3,4,5):
            if (hr > 16 ):
                clck_tm = datetime.datetime(now.year,now.month,now.day) + \
                      datetime.timedelta(hours=hr)
            else:
                clck_tm = datetime.datetime(now.year,now.month,now.day) + \
                      datetime.timedelta(days=1,hours=hr)
            if ( calc_status( rise_tm_d[ objs ], set_tm_d[ objs ], \
                              clck_tm) == "on" ):
                 pygame.draw.circle(screen, (255,0,0), (x,y), 8 )
            else:
                pygame.draw.circle(screen, (50,50,50), (x,y), 8 )
            x = x + xinc
        y = y + yinc 
#
# function to display time on screen
#
def dispTime():

    now = time.localtime()
    currentTimeLine = strftime("%H:%M:%S", now)
    text = font.render(currentTimeLine, 0, (0,250,150))
    textpos = text.get_rect()
    textpos.topright = background.get_rect().topright
    screen.blit(background, textpos, textpos )
    screen.blit(text, textpos)

#
# function to display menu at bottom of screen
#
def dispMenu(options):
    textstr = ""
    if (options[0] != ""):
        textstr = textstr + " 1 =" + options[0]
    if (options[1] != ""):
        textstr = textstr + " 2 =" + options[1]
    if (options[2] != ""):
        textstr = textstr + " 3 =" + options[2]
    if (options[3] != ""):
        textstr = textstr + " 4 =" + options[3] 
    text = font.render( textstr, True, (255,255,0))
    textpos = text.get_rect()
    textpos.bottomleft = background.get_rect().bottomleft
    screen.blit( text, textpos)

#
# Main routine
# 
def main():

## PiTFT: (uncomment)
##    GPIO.setmode(GPIO.BCM)
##    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    global background, screen, font

    background_image_filename = 'constellation-320px.png'
    splash_image_filename = 'Yellow_Sky.png'


    ## Dictionary of pages and the pages that are called from buttons 1-4
    displaydict = { "Menu": ["Cycle","Details","Objs","Quit"],
                    "Objs": ["Menu","Objs","Sky","Weather"],
                    "Sky": ["Menu","Objs","Sky","Weather"],
                    "Weather": ["Menu","Objs","Sky","Weather"],
                    "Quit": ["Yes","No","",""],
                    "Cycle": ["Yes","No","",""],
                    "Details": ["Menu","Objs","Sky","Weather"],
                    "Yes":["","","",""],
                    "No":["","","",""]
                    }

    font_size = 22
    splash_font_size = 50
    size = width, height = 320, 240

    os.environ["SDL_FBDEV"] = "/dev/fb1"
    disp_no = os.getenv("DISPLAY")

    if disp_no:
        print "running under X display"
    else:
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

    pygame.font.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("NightSkyOrb: vers: PiTFT")
    font = pygame.font.SysFont(None, font_size);
    splash_font = pygame.font.SysFont(None, splash_font_size)

    background = pygame.image.load(splash_image_filename).convert()

    splash_surface = splash_font.render("Night Sky Orb", \
                                        True, (255,255,255))
    splash_rect = splash_surface.get_rect()
    x = background.get_rect().centerx - splash_rect.width/2
    y = background.get_rect().centery
    
    screen.blit(background,(0,0))
    screen.blit(splash_surface, (x,y) )

    pygame.display.update()
    time.sleep(3)

    background = pygame.image.load(background_image_filename).convert()

    lastpage = ""
    displaypage = "Menu"
    quit_confirm = False
    cycle_confirm = False
    cycle_flag = False
    cycle_min = -1


    #
    # Main Event Loop
    # 
    while True:

        ## Always display time in right corner
        dispTime()

        ## Always display menu at bottom corner
        try:
            dispMenu(displaydict[displaypage])
        except KeyError:
            print ( "no menu" )

        ## Get keyboard events        
        buttonpress = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                
                if event.key == K_q:
                    pygame.quit()
                    exit()
                elif event.key == K_1:
                    buttonpress = 1
                elif event.key == K_2:
                    buttonpress = 2
                elif event.key == K_3:
                    buttonpress = 3
                elif event.key == K_4:
                    buttonpress = 4

## PiTFT (uncomment) 
##        if not(GPIO.input(23)):
##	    buttonpress = 1
##	    time.sleep(0.5)
##        if not(GPIO.input(22)):
##            buttonpress = 2
##            time.sleep(0.5)
##        if not(GPIO.input(27)):
##            buttonpress = 3
##            time.sleep(0.5)
##        if not(GPIO.input(18)):
##            buttonpress = 4
##            time.sleep(0.5)

##        debug code to see button press events
##        text = font.render(str(buttonpress), 0, (0,250,150))
##        textpos = text.get_rect()
##        textpos.center = background.get_rect().center
##        screen.blit(text, textpos)


        ## Find new page based upon button pressed
        if (buttonpress != 0):
            try:
                choice = displaydict[displaypage]
                displaypage = choice[buttonpress-1]
            except KeyError:
                print ( "No page found, back to page1" )
                displaypage = "Menu"
              
            ## print ("choice = ", choice)
            ## print ("displaypage =", displaypage )

        if (displaypage != lastpage):

            ## Start with background
            screen.blit(background, (0, 0))

            ## display page depbug
            # text = font.render(displaypage, 0, (0,250,150))
            # textpos = text.get_rect()
            # textpos.center = background.get_rect().center
            # screen.blit(text, textpos)

            if (displaypage == "Menu"):
                print ("call Menu")
                dispMain()
                
            elif (displaypage == "Objs"):
                print ("call Objs")
                dispObjs()
                    
            elif (displaypage == "Sky"):
                print ("call Sky")
                dispSky()
                                    
            elif (displaypage == "Weather"):
                print ("call Weather")
                dispWeather()
                    
            elif (displaypage == "Quit"):
                print ("call Quit")
                quit_confirm = True
                
            elif (displaypage == "Cycle"):
                print ("call Cycle")
                cycle_confirm = True
                
            elif (displaypage == "Details"):
                print ("call Details")
                dispDetails()
                
            elif (displaypage =="Yes"):
                if (quit_confirm):
                    pygame.quit()
                    exit()
                if (cycle_confirm):
                    cycle_flag = True
                    displaypage = "Objs"
                    dispObjs()
                    
            elif (displaypage =="No"):
                if (quit_confirm):
                    quit_confirm = False
                    displaypage = "Menu"
                    dispMain()

                if (cycle_confirm):
                    cycle_flag = False
                    displaypage = "Menu"
                    dispMain()
        
        pygame.display.update()
        time.sleep(0.1)

        lastpage = displaypage

        ## cycle display every minute when seconds are 0 and new minute
        if (cycle_flag == True):
            if ( (time.localtime()[5] == 0) and
                 (cycle_min != time.localtime()[4]) ):
                cycle_min = time.localtime()[4]
                if (displaypage == "Objs"):
                    displaypage = "Sky"
                elif (displaypage == "Sky"):
                    displaypage = "Weather"
                elif (displaypage == "Weather"):
                    displaypage = "Objs"

if __name__ == '__main__':
    main()
    
