#!/usr/bin/python3
# coding: utf-8
#
# Read 1-Wire sensors and write into database
# 06.10.2015 by meigrafd
#
# NOTE:
# Im using CyMySQL which is a fork of pymysql with C speedups. See http://stackoverflow.com/a/25724855
#
#------------------------------------------------------------------------

# Specify Settings for MySQL: Host, Port, Login and Password
mysqlHost = '127.0.0.1'
mysqlPort = '3306'
mysqlLogin = 'root'
mysqlPass = 'raspberry'
mysqlDatabase = "measurements"

sensor_dict={}
# 1wire Sensor Path and Place.
# Format: sensor_dict["<path>"] = "<Place>"
# E.g.: sensor_dict["/sys/bus/w1/devices/10-000801b5a7a6/w1_slave"] = "Bath"
sensor_dict["/sys/bus/w1/devices/10-000801b5a7a6/w1_slave"] = "Badezimmer"
sensor_dict["/sys/bus/w1/devices/10-000801b5959d/w1_slave"] = "Wohnzimmer"

#------------------------------------------------------------------------
import sys, time, os, re
try:
    import cymysql
except ImportError:
    print("ERROR: You must install cymysql Module: sudo apt-get install python3-pip && sudo pip-3.2 install cymysql")
    exit()
if not os.path.exists("/sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count"):
    print("ERROR: w1 Kernel Module not loaded?")
    print("With Kernel >= 3.18:")
    print(" echo dtoverlay=w1-gpio >> /boot/config.txt")
    print("or")
    print(" echo dtoverlay=w1-gpio-pullup >> /boot/config.txt")
    print("With older Kernels add:\n w1-gpio\n w1-therm\nto /etc/modules")
    exit()
if open("/sys/bus/w1/devices/w1_bus_master1/w1_master_slave_count").read(1000).startswith("0"):
    print("ERROR: No 1-wire Sensors connected?")
    exit()

# This handles console colors used for print's
#http://misc.flogisoft.com/bash/tip_colors_and_formatting
class c:
    ENDC='\33[0m'
    DEFAULT='\33[39m'; BOLD='\33[1m'; DIM='\33[2m'
    RESBOLD='\33[21m'; RESDIM='\33[22m'
    RED='\33[31m'; GREEN='\33[32m'; YELLOW='\33[33m'; CYAN='\33[36m'

def read_sensor(path):
    value=None
    try:
        f = open(path, 'r')
        line = f.readline()
        if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
            line = f.readline()
            m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
            if m:
                value = str(float(m.group(2)) / 1000.0)
        f.close()
    except (IOError) as e:
        print(time.strftime("%x %X"), c.BOLD+c.RED+"Error reading"+c.ENDC, path, ": ", e.strerror)
    return value

def get_data():
    for sensorPath in sensor_dict:
        sensorPlace = sensor_dict.get(sensorPath)
        data = read_sensor(sensorPath)
        if data:
            print('{} -> {}'.format(sensorPlace, data))
            addTemp(sensorPlace, data)
        else:
            print('{} -> None'.format(sensorPlace))

def addTemp(Place, Data):
    Timestamp = int(time.time())
    con = None
    try:
        con = cymysql.connect(host=mysqlHost, port=int(mysqlPort), user=mysqlLogin, passwd=mysqlPass)
        cur = con.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS %s;" % mysqlDatabase)
        cur.execute("USE %s;" % mysqlDatabase)
        con.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS data (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,location VARCHAR(255),timestamp INT(11),temp FLOAT(11),hum FLOAT(11),KEY location (location)) ENGINE=InnoDB DEFAULT CHARSET=utf8;")
        con.commit()
        cur.execute("INSERT INTO data (timestamp, location, temp) VALUES (%s,%s,%s);", (Timestamp, Place, Data))
        con.commit()
    except Exception as err:
        print(c.BOLD+c.RED+"MySQL Error: "+str(err)+c.ENDC)
    except (KeyboardInterrupt, SystemExit):
        exit()
    finally:
        if con:
            con.close()

if __name__ == '__main__':
    try:
        get_data()
    except (KeyboardInterrupt, SystemExit):
        print("\nSchliesse Programm..")
