<?php

function show_directory() {
    header('Content-Type: text/html');
    echo("<h1>Welcome to the Wiki Archive</h1>\n");
    echo("<ul>\n");
    foreach (glob("html/*/Main") as $filename) {
        $pieces = explode('/',$filename);
        if ( count($pieces) != 3 ) continue;
        echo('<li><a href="/wiki/index.php/'.$pieces[1].':'.$pieces[2].'">');
        echo($pieces[1].':'.$pieces[2]."</a></li>\n");
    }
}

if ( !isset($_SERVER['PATH_INFO']) ) {
    show_directory();
    return;
}

$path = $_SERVER['PATH_INFO'];
if ( strpos($path,'/') !== 0 ) {
    show_directory();
    return;
}
$path = substr($path,1);
$pieces = explode(':',$path);
if ( count($pieces) != 2 ) {
    show_directory();
    return;
}
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

