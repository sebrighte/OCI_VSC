<?php 

$api_key = "Ocp-Apim-Subscription-Key: 9d7d513a7e9849f8bc3ad9f05fe0b033";

$bbox = $_GET['bbox'];
$service = $_GET['service'];
$request = $_GET['request'];
$styles = $_GET['styles'];
$version = $_GET['version'];
$format = $_GET['format'];
$layers = $_GET['layers'];
$width = $_GET['width'];
$height = $_GET['height'];
$srs = $_GET['srs'];
$transparent = $_GET['transparent'];
$Display_params = $_GET['Display_params'];

$url = $_GET['uri'];

$url = str_replace("?","",$url);

$query_array = array (
    'SERVICE' => $service,
    'REQUEST' => $request,
    'VERSION' => $version,
    'STYLES' => $styles,
    'FORMAT' => $format,
    'LAYERS' => $layers,
    'HEIGHT' => $height,
    'WIDTH' => $width,
    'TRANSPARENT' => $transparent,
    'SRS' => $srs,
    //'BGCOLOR' => 'B4A970',
    'DISPLAY_PARAMS' => $Display_params,
    'BBOX' => $bbox
);

$query = http_build_query($query_array);
$url = $url . '?' . $query;

$opts = array (
    'http' => array (
        'header'=> $api_key
    )
);

$image = file_get_contents($url, false, stream_context_create($opts));

header('Content-type: image/png;');
header("Content-Length: " . strlen($image));

echo $image;

