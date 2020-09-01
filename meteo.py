#!/usr/bin/python3
""" IMPORTS """
import requests
import sys
import json

""" BRIAN SINQUIN - METEO """

""" CONSTANTS """
# openweather API key
app_key="835295f911955ff31de25a0226a08f11" # Please register your own key

""" PRINTING METHODS """
# console colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# colored log function
def log(str, c : bcolors = bcolors.ENDC):
    print(c+str+bcolors.ENDC)

""" INPUT METHOD """
# colored input method with type exception handling
def ask(str, t : type):
    r = input(bcolors.HEADER+str+bcolors.ENDC)
    try:
        r=t(r)
    except ValueError:
        log("\t[!] Input error - Exiting ...", bcolors.FAIL + bcolors.BOLD)
        sys.exit(0)
    return r

""" Hacking stuff """

def go():
    log("~~<: Setting Up :>~~", bcolors.OKBLUE)

    # retrieving inputs
    city = ask("Please give us your city: ", str)
    c_code = ask("Please give us your country code (uk, fr, ca ...) [Optional]: ", str)

    log(f"\t Searching for meteo in {city}..")

    # creating API call url
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={app_key}&q={city}"
    if c_code != "":
        url=url+f',{c_code}'
    # API call
    r = requests.get(url)

    # parse json
    data=r.json()

    # check result status (error, not found, 200 OK)
    if r.status_code==404: 
        log("\t[!] City Not Found", bcolors.FAIL+bcolors.BOLD) 
        sys.exit(0)
    elif r.status_code==401:
        log("\t[!] Service error", bcolors.FAIL+bcolors.BOLD) 
        sys.exit(0)
    else: 
        log("\tParsing data ...", bcolors.OKGREEN+bcolors.BOLD)
        print("\n")

        # retrieving temperatures & kelvin to celcius conversion
        ta = format(data["main"]["temp"]-273.15, '.2f')
        tr = format(data["main"]["feels_like"]-273.15, '.2f')
        tmin = format(data["main"]["temp_min"]-273.15, '.2f')
        tmax = format(data["main"]["temp_max"]-273.15, '.2f')

        hum =  data["main"]["humidity"]
        desc = data["weather"][0]["description"]

        # printing weather results

        log(f"{str.upper(city)},{str.upper(c_code)} : Today's meteo\n", bcolors.BOLD+bcolors.WARNING)
        log("\t* Temperatures\n", bcolors.UNDERLINE+bcolors.OKBLUE)
        log(f"\t\t* Actual temperature : {ta}°C")

        # prints red if felt temp. is greater than actual one, blue if not
        if ta > tr:
            f=bcolors.OKBLUE
        else:
            f=bcolors.FAIL

        log(f"\t\t * Feeling temperature : {tr}°C", f)

        log(f"\t\t* Minimum temperature : {tmin}°C")
        log(f"\t\t* Maximum temperature : {tmax}°C")
        log("\t* Others \n", bcolors.UNDERLINE+bcolors.OKBLUE)
        log(f"\t\t* Humidity : {hum}%")
        log(f"\t\t* Description : {str.upper(desc)}")

if __name__ == "__main__" :
    go()
    # end of program -> exit
    sys.exit(0)
