<?php
$path = $_SERVER['PATH_INFO'];
if ( strpos($path,'/') !== 0 ) {
    die('Bad format');
}
$path = substr($path,1);
$pieces = explode(':',$path);
if ( count($pieces) != 2 ) die('Bad format:');
/*
echo("<pre>\n");
var_dump($pieces);
var_dump($_SERVER);
echo("</pre>");
*/

$fname = 'html/'.$pieces[0].'/'.$pieces[1];
if ( ! file_exists($fname) ) {
    header("HTTP/1.0 404 Not Found");
    return;
}

header('Content-Type: text/html');
echo file_get_contents($fname);

