<?php

//sudo cp -R /config/workspace/web/oci/redirect.php /var/www/html/

	$uri = $_SERVER['REQUEST_URI'];
	$uri= str_replace("/redirect.php?uri=","",$uri);

    echo $uri;

    $fp = fopen($uri, 'r');
	
	// header('Access-Control-Allow-Origin: *'); 
	// header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
	// header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token, Authorization');
	// header("Content-Length: " . filesize($uri));
	
	// header_remove("server"); 
    // header_remove("content-type");
	
	fpassthru($fp);