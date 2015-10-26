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
Configure /usr/local/sbin/1wire.py and set MySQL Stuff.
```
sudo nano /usr/local/sbin/1wire.py
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
