<?php
//------------------------------------------------------
require_once('include/global.php');
//------------------------------------------------------

if (isset($_GET['type'])) {

    if ($_GET['type'] == 'temp') {
        $Type = 'temp';
    } else {
        $Type = 'hum';
    }

    if (isset($_GET['period'])) {
        $Period = $_GET['period'];
        // remove all numbers from period string (eg. from 12h so only h is left)
        $PeriodUnit = preg_replace('/[0-9]+/', '', $Period);
        // remove the Unit from period string so only numbers are left
        $PeriodNum = str_replace($PeriodUnit, '', $Period);
    } else {
        $Period = '6h';
        $PeriodUnit = preg_replace('/[0-9]+/', '', $Period);
        $PeriodNum = str_replace($PeriodUnit, '', $Period);
    }
    
    $conid = mysql_con();
    $db_selected = mysqli_select_db($conid, $database);
    if (!$db_selected) { die('Cannot use Database '.$database.' : '.mysqli_error($conid)); }

    // Get each "location"
    $dataResult = array();
    $result = query("SELECT location FROM data GROUP BY location");
    while ($row = mysqli_fetch_array($result)) {
        $data = array();
        // Get Data from each "location"
        $result2 = query("SELECT location,timestamp,".$Type." FROM data 
                         WHERE location = '".$row['location']."' 
                         AND timestamp >= UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL ".$PeriodNum." ".getPeriodUnit($Period).")) 
                         AND timestamp <= UNIX_TIMESTAMP() 
                         ORDER BY timestamp ASC
                        ;");
        while ($row2 = mysqli_fetch_array($result2)) {
            if (!empty($row2[$Type])) {
                $data['data'][] = array((float)($row2['timestamp']*1000), (float)$row2[$Type]);
            }
        }
        if (isset($data['data'])) {
            $data['name'] = $row['location'];   
            array_push($dataResult, $data);
        }
    }
    mysqli_close($conid);

    print json_encode($dataResult);
}
?>