<?php

function show_header() {
?>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

<style>
a[href^="http://"] {
    background: url(http://upload.wikimedia.org/wikipedia/commons/6/64/Icon_External_Link.png)     center right no-repeat;
    padding-right: 13px;
}
a[href^="https://"] {
    background: url(http://upload.wikimedia.org/wikipedia/commons/6/64/Icon_External_Link.png)     center right no-repeat;
    padding-right: 13px;
}
body {
    padding-left: 10px;
    padding-right: 10px;
}
</style>
</head>
<body>
<!-- This is an archive of a MediaWiki site - some links might be broken -->
<?php
}

function show_directory() {
    header('Content-Type: text/html');
    show_header();
    echo("<h1>Welcome to the Wiki Archive</h1>\n");
    echo("<ul>\n");
    foreach (glob("html/*/Main") as $filename) {
        $pieces = explode('/',$filename);
        if ( count($pieces) != 3 ) continue;
        echo('<li><a href="/wiki/index.php/'.$pieces[1].':'.$pieces[2].'">');
        echo($pieces[1].':'.$pieces[2]."</a></li>\n");
    }
?>
</ul>
<p>If you want your own copy of this material or want to have some of this material removed, please contact Charles R. Severance.</p>
<p><small>This is an archive of a MediaWiki site - some links might be broken.<br/>
<a href="#" onclick="$('#about').show();$('#about_link').hide();return false;"
    id="about_link">About the software</a>
<span style="display: none" id="about">This data was spidered using the 
<a href="https://github.com/csev/wikiextract" target="_blank">WikiExtract</a>
software developed by <a href="http://www.dr-chuck.com/" target="_blank">Charles R. Severance.</a>
</span></small></p>
<?php
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

show_header();
echo file_get_contents($fname);
echo("<hr/>\n");
if ( $pieces[1] != 'Main' ) {
?>
<a href="/wiki/index.php/<?= $pieces[0] ?>:Main">Back to <?= $pieces[0] ?></a>
<?php } ?>
<a href="/wiki/index.php">Back to all categories</a>
<p><small>This is an archive of a MediaWiki site - some links might be broken.<br/>
<a href="#" onclick="$('#about').show();$('#about_link').hide();return false;"
    id="about_link">About the software</a>
<span style="display: none" id="about">This data was spidered using the 
<a href="https://github.com/csev/wikiextract" target="_blank">WikiExtract</a>
software developed by <a href="http://www.dr-chuck.com/" target="_blank">Charles R. Severance.</a>
</span></small></p>

<script type="text/javascript">/*<![CDATA[*/

  // http://www.w3schools.com/jquery/jquery_get_started.asp
  $(document).ready(function(){
    
    // external links to new window
    $('a[href^="http://"]').not('a[href*=mydomainname]').attr('target','_blank');
    $('a[href^="https://"]').not('a[href*=mydomainname]').attr('target','_blank');
    
    // force PDF Files to open in new window
    $('a[href$=".pdf"]').attr('target', '_blank');

  });

 /*]]>*/</script>
</body>
