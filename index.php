<?php
//------------------------------------------------------
require_once('include/global.php');
//------------------------------------------------------
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="de">
<head>
<title>Sensor Infos</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="robots" content="DISALLOW">
<script src="js/jquery-1.11.3.min.js"></script>
<script src="js/functions.js"></script>
<style type=text/css>
 body { 
    font-size: 13pt;
    color: black;
    font-family: Verdana,arial,helvetica,serif;
    margin: 0px;
    background-color: #F5F5DC;
 }
 #header {
    width: 100%;
    min-height: 80px;
 }
 #menu {
    font-size: 11pt;
    color: #000;
    float: left;
    padding: 5px;
    background-color: #F5F5DC;
    margin: 0px 0px 0px 10px;
    line-height: 20px;
    min-width: 100px;
 }
 #content {
    min-height: 840px;
    margin-left: 140px;
    width: 80%;
 }
 #tempchart {
    margin-top: 0px;
 }
 #humchart {
    margin-top: 20px;
 }
 #footer {
    width: 100%;
    min-height: 0px;
    background-color: #F5F5DC;
    text-align: center;
 }
</style>
</head>
<body>
<div id='header'> </div>
<?php
//------------------------------------------------------

error_reporting(E_ALL);
ini_set('track_errors', 1);
ini_set('display_errors', 1);
ini_set('log_errors', 1);
ini_set('memory_limit', '64M');
ini_set('max_execution_time', '30');
@ob_implicit_flush(true);
@ob_end_flush();
$_SELF = $_SERVER['PHP_SELF'];
$DURATION_start = microtime(true);

//------------------------------------------------------
// Menue
//------------------------------------------------------

echo "<div id='menu'>\n";
foreach ($Chart AS $PERIOD => $DESCRIPTION) {
    echo "&#8226; <a href='?period=".$PERIOD."' title='".$DESCRIPTION."'>Last ".$PERIOD."</a><br/>\n";
}
echo "</div>\n";

//------------------------------------------------------
// Content / Charts
//------------------------------------------------------

echo "<div id='content'>\n";
echo "  <div id='tempchart'> </div>\n";
echo "  <div id='humchart'> </div>\n";

if (isset($_GET['period'])) {
    $Period = $_GET['period'];
?>
<script src='highcharts/js/highcharts.js'></script>
<script src='highcharts/js/themes/grid.js'></script>
<script src='highcharts/js/modules/exporting.js'></script>
<script src='highcharts/js/modules/no-data-to-display.js'></script>
<script type='text/javascript'>
$(function() {
    $(document).ready(function() {
        // Global Chart Options
        Highcharts.setOptions({
            global: {
              useUTC: false
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
              type: "datetime",
              labels: {
                style: {
                  "color":"#6D869F", "font-size":"10pt", "fontWeight":"bold"
                }
              }
            },
            legend: {
              enabled: true
            },
            credits: {
              enabled: false
            },
            colors: ["#4572A7", "#AA4643", "#89A54E", "#80699B", "#3D96AE", "#DB843D", "#92A8CD", "#A47D7C", "#B5CA92"]
        });

        // Chart: Temperatures
        $.getJSON("data.php?type=temp&period=<?php echo $Period; ?>", function(json) {
            var temp = new Highcharts.Chart({
                series: json,
                chart: {
                  type: "spline",
                  renderTo: "tempchart",
                  zoomType: 'x'
                },
                title: {
                  text: "Temperatures <?php echo $Chart[$Period]; ?>"
                },
                tooltip: {
                  crosshairs: true,
                  useHTML: true,
                  valueDecimals: 2,
                  valueSuffix: ' °C'
                },
                yAxis: {
                  title: {
                    text: "Temperatures (°C)" 
                  },      
                  labels: {
                    formatter: function() {
                      return this.value +"°C"
                    },
                    style: {
                      "color":"#6D869F", "font-size":"10pt", "fontWeight":"bold"
                    }
                  }
                },
                plotOptions: {
                  series: {
                    lineWidth: 2,
                    marker: {
                      radius: 2
                    }
                  }
                },
            });
        });

        // Chart: Humidity
        $.getJSON("data.php?type=hum&period=<?php echo $_GET['period']; ?>", function(json) {
            var hum = new Highcharts.Chart({
                series: json,
                chart: {
                  type: "spline",
                  renderTo: "humchart",
                  zoomType: 'x'
                },
                title: {
                  text: "Humidity <?php echo $Chart[$Period]; ?>"
                },
                tooltip: {
                  crosshairs: true,
                  useHTML: true,
                  valueDecimals: 2,
                  valueSuffix: ' %'
                },
                yAxis: {
                  title: {
                    text: "Humidity (%)" 
                  },      
                  labels: {
                    formatter: function() {
                      return this.value +"%"
                    },
                    style: {
                      "color":"#6D869F", "font-size":"10pt", "fontWeight":"bold"
                    }
                  }
                },
                plotOptions: {
                  series: {
                    lineWidth: 1,
                    marker: {
                      radius: 2
                    }
                  }
                },
            });
        });
    });
});
</script>
<?php
}
echo "</div>\n"; // END: content

//------------------------------------------------------
// Footer
//------------------------------------------------------
/*
echo "\n<div id='footer'>\n";
echo "<br/><br/><br/><br/>\n";
$DURATION_end = microtime(true);
$DURATION = $DURATION_end - $DURATION_start;
echo "<p><font size='0'>Page generated in ".round($DURATION, 3)." seconds</font></p>\n";
echo "</div>\n";
*/
?>
</body>
</html>
