<?php

// functions
//------------------------------------------------------
// http://www.w3schools.com/php/php_ref_mysqli.asp
function query($query_string) {
	global $conid, $showqueries;
	if (!isset($conid) OR !$conid) { $conid = mysql_con(); }
	if (!isset($showqueries)) { $showqueries = 0; }
	if ($showqueries) { echo "Query: $query_string <br/>\n"; }
	$query_id = mysqli_query($conid, $query_string);
	if (!$query_id) { echo "Invalid SQL: $query_string <br/>\n"; }
	return $query_id;
}
function mysql_con() {
	global $dbuser, $dbpass, $dbhost, $database;
	$conid = mysqli_connect($dbhost, $dbuser, $dbpass, $database);
	if (mysqli_connect_errno()) { die('Error connecting to MySQL: ' . mysqli_connect_error()); }
	return $conid;
}
//------------------------------------------------------

function getPeriodUnit($period) {
    // remove all numbers from period string
    $unit = preg_replace('/\d+/', '', $period);
    switch ($unit) {
        case 's': return 'SECOND';
        case 'mi': return 'MINUTE';
        case 'h': return 'HOUR';
        case 'd': return 'DAY';
        case 'w': return 'WEEK';
        case 'm': return 'MONTH';
        case 'y': return 'YEAR';
    }
}

?>