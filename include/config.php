<?php
//------------------------------------------------------
// MySQL
//------------------------------------------------------
$dbuser = "root";
$dbpass = "passw0rd";
$database = "measurements";
/*
CREATE TABLE `data` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `location` VARCHAR(255),
  `timestamp` INT(11),
  `temp` FLOAT(11),
  `hum` FLOAT(11),
  `vcc` FLOAT(11),
  PRIMARY KEY (`id`),
  KEY `location` (`location`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
*/
//------------------------------------------------------
// Selectable Chart Ranges.
// Format:  $Chart['<period>'] = '<chart title>';
// Example: $Chart['12h'] = 'of the last 12 hours';
// Valid Units: s=second,mi=Minute,h=hour,d=day,w=week,m=month,y=year
//------------------------------------------------------
$Chart['30mi'] = 'of the last 30 minutes';
$Chart['1h'] = 'of the last 1 hour';
$Chart['2h'] = 'of the last 2 hours';
$Chart['3h'] = 'of the last 3 hours';
$Chart['6h'] = 'of the last 6 hours';
$Chart['12h'] = 'of the last 12 hours';
$Chart['24h'] = 'of the last 24 hours';
$Chart['2d'] = 'of the last 2 days';
$Chart['3d'] = 'of the last 3 days';
$Chart['1w'] = 'of the last week';
$Chart['2w'] = 'of the last 2 weeks';
$Chart['1m'] = 'of the last month';
$Chart['3m'] = 'of the last 3 months';
$Chart['6m'] = 'of the last 6 months';
$Chart['1y'] = 'of the last year';
//------------------------------------------------------
?>