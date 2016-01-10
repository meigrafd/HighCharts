Highcharts Sensors
****************************************************

Using Highcharts with MySQL to display Sensor Data


Installation:
--------

```
sudo apt-get install git-core
sudo mkdir /var/www/charts
cd /var/www/charts
sudo git clone https://github.com/meigrafd/HighCharts .
sudo mv 1wire.py /usr/local/sbin/
sudo chmod 770 /usr/local/sbin/1wire.py
sudo chown -R www-data:www-data /var/www/charts
```
Edit config.php and configure at last the db lines:
```
sudo nano /var/www/charts/include/config.php
```
```
$dbuser = "root";
$dbpass = "passw0rd";
$database = "measurements";
```

Edit /usr/local/sbin/1wire.py and configure following lines:
```
sudo nano /usr/local/sbin/1wire.py
```
```
mysqlHost = '127.0.0.1'
mysqlPort = '3306'
mysqlLogin = 'root'
mysqlPass = 'raspberry'
mysqlDatabase = "measurements"

sensor_dict["/sys/bus/w1/devices/10-000801b5a7a6/w1_slave"] = "Badezimmer"
sensor_dict["/sys/bus/w1/devices/10-000801b5959d/w1_slave"] = "Wohnzimmer"
```

Dont forget to install needed Python Modules
```
sudo apt-get install python3-pip && sudo pip-3.2 install cymysql
```
Edit root Crontab
```
sudo crontab -e
```

and add following line:
```
* * * * *     /usr/local/sbin/1wire.py >/dev/null 2>&1
```
