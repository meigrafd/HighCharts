Highcharts Sensors
****************************************************

Using Highcharts with MySQL to display Sensor Data


Installation:
--------

```
sudo mkdir /var/www/charts
cd /var/www/charts
sudo git clone https://github.com/meigrafd/HighCharts .
sudo mv 1wire.py /sbin/
sudo chown -R www-data:www-data /var/www/charts
sudo chmod 770 /sbin/1wire.py
```
Configure /sbin/1wire.py and set MySQL Stuff.
```
sudo nano /sbin/1wire.py
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
* * * * *     /sbin/1wire.py >/dev/null 2>&1
```
