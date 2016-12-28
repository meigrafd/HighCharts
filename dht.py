#!/usr/bin/python3
# coding: utf-8
#
# Read DHT Sensors and write into MySQL Database for HighCharts
# 28.12.2016  Copyright (C) by meigrafd (meiraspi@gmail.com) published under the MIT License
#
# NOTE:
# Im using CyMySQL which is a fork of pymysql with speedups. See http://stackoverflow.com/a/25724855
#
#------------------------------------------------------------------------
import sys
import time
import os
import re
#from decimal import Decimal, ROUND_HALF_UP
sensor_dict={}
#------------------------------------------------------------------------
#
#### CONFIG - START

# Specify Path to config.php File
phpConfigFile = '/var/www/html/charts/include/config.php'

# DHT Sensor Type, GPIO pin and Place.
# Format: sensor_dict["<Place>"] = "<Type>;<GPIO>"
# E.g.: sensor_dict["Bath"] = "22;4"
# Types: 11 = DHT11 , 22 = DHT22 , 23 = AM2302
sensor_dict["Badezimmer"] = "22;4"
sensor_dict["Terrasse"] = "22;17"

#### CONFIG - END
#
#------------------------------------------------------------------------
try:
    import cymysql
except ImportError:
    print("ERROR: You must install cymysql Module: sudo apt-get install python3-pip && sudo pip-3.2 install cymysql")
    exit()
try:
    import Adafruit_DHT
except ImportError:
    print("ERROR: You must install Adafruit_DHT Python3 Module!")
    exit()


# Try to read config.php to get mysql settings
# http://stackoverflow.com/questions/16881577/parse-php-file-variables-from-python-script
try:
    pattern = re.compile(r"""(^)\$([a-z]*)\s*=\s*(.*?);$""")
    php_config={}
    with open(phpConfigFile) as fileObject:
        for line in fileObject.readlines():
            for match in pattern.finditer(line):
                php_config[match.group(2)] = match.group(3).replace('"', '')
    if 'dbhost' in php_config:
        mysqlHost = php_config['dbhost']
    else:
        mysqlHost = "127.0.0.1"
    if 'dbport' in php_config:
        mysqlPort = php_config['dbport']
    else:
        mysqlPort = 3306
    mysqlLogin = php_config['dbuser']
    mysqlPass = php_config['dbpass']
    mysqlDatabase = php_config['database']
except Exception as error:
    print("Error reading config.php: %s" % str(error))


# This handles console colors used for print's
#http://misc.flogisoft.com/bash/tip_colors_and_formatting
class c:
    ENDC='\33[0m'
    DEFAULT='\33[39m'; BOLD='\33[1m'; DIM='\33[2m'
    RESBOLD='\33[21m'; RESDIM='\33[22m'
    RED='\33[31m'; GREEN='\33[32m'; YELLOW='\33[33m'; CYAN='\33[36m'


#https://github.com/liftoff/GateOne/blob/master/terminal/terminal.py#L358
def strtranslate(from_str):
    translations = (
        (u'\N{LATIN SMALL LETTER U WITH DIAERESIS}', u'ue'),
        (u'\N{LATIN SMALL LETTER O WITH DIAERESIS}', u'oe'),
        (u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'ae'),
        (u'\N{LATIN CAPITAL LETTER A WITH DIAERESIS}', u'Ae'),
        (u'\N{LATIN CAPITAL LETTER O WITH DIAERESIS}', u'Oe'),
        (u'\N{LATIN CAPITAL LETTER U WITH DIAERESIS}', u'Ue'),
        (u'\N{LATIN SMALL LETTER SHARP S}', u'ss'),
        # et cetera
    )
    out = from_str
    for from_str, to_str in translations:
        out = out.replace(from_str, to_str)
    return out


class DhtSensorController():
    def __init__(self, sensorType, gpioPin):
        self.sensorType = sensorType
        self.gpioPin = gpioPin
        
    def readData(self):
        if self.sensorType == 11:
            sensor = Adafruit_DHT.DHT11
        elif self.sensorType == 22:
            sensor = Adafruit_DHT.DHT22
        elif self.sensorType == 23:
            sensor = Adafruit_DHT.AM2302
        else:
            self.readSuccess = False
            raise Exception("Unknown sensor type. Use 11 for DHT11, 22 for DHT22 and 23 for AM2302")

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.gpioPin, retries=15, delay_seconds=2)
        if humidity is not None and temperature is not None:
            #temp = Decimal(temperature)
            #hum = Decimal(humidity)
            #self.temperature = Decimal(temp.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
            #self.humidity = Decimal(hum.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
            self.temperature = format(temperature, '.2f')
            self.humidity = format(humidity, '.2f')
            self.readSuccess = True
        else:
            self.readSuccess = False
            print('Failed to get reading. Try again!')


def get_data():
    for sensorPlace in sensor_dict:
        sensorPlace = strtranslate(sensorPlace)
        sensorType, sensorGPIO = sensor_dict.get(sensorPlace).split(';')
        DHT = DhtSensorController(int(sensorType), int(sensorGPIO))
        DHT.readData()
        if DHT.readSuccess:
            return (True, sensorPlace, DHT.temperature, DHT.humidity)
        else:
            return (False, sensorPlace)


def add_data(Place, Temp, Hum):
    con = None
    try:
        con = cymysql.connect(host=mysqlHost, port=int(mysqlPort), user=mysqlLogin, passwd=mysqlPass)
        cur = con.cursor()
        cur.execute("USE %s;" % mysqlDatabase)
        con.commit()
        cur.execute("INSERT INTO data (timestamp, location, temp, hum) VALUES (%s,%s,%s,%s);", (int(time.time()), Place, Temp, Hum))
        con.commit()
    except Exception as err:
        print(c.BOLD+c.RED+"MySQL Error: "+str(err)+c.ENDC)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
    finally:
        try: cur.close()
        except: pass
        try: con.close()
        except: pass


if __name__ == '__main__':
    try:
        con = cymysql.connect(host=mysqlHost, port=int(mysqlPort), user=mysqlLogin, passwd=mysqlPass)
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS %s;" % mysqlDatabase)
        cur.execute("USE %s;" % mysqlDatabase)
        con.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS data (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,location VARCHAR(255),timestamp INT(11),temp FLOAT(11),hum FLOAT(11),KEY location (location)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        con.commit()
        try: cur.close()
        except: pass
        try: con.close()
        except: pass
        
        data = get_data()
        if data[0]:
            print('{0} -> {1}C , {2}%'.format(data[1], data[2], data[3]))
            add_data(data[1], data[2], data[3])
        else:
            print('{} -> None'.format(data[1]))
        
    except (KeyboardInterrupt, SystemExit):
        print("\nSchliesse Programm..")


#EOF
