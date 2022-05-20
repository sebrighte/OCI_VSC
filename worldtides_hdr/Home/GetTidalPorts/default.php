<?php 

    //$apikey = "7fQGFhCmiQtQm8jQY+OfTTDLJzCO4ADkWysG4NFssCQ=";

    $countries = $_GET['countries']; 

    $url = 'https://ukho-tides-test.westeurope.cloudapp.azure.com/API/Tides/api/v1/Stations/EasytideStations';

    $query_array = array (
        'type' => 'FS_PortsOnly',
        'countries' => $countries
    );

    $query = http_build_query($query_array);
    $url = $url . '?' . $query;
    //echo $url;
    
    echo file_get_contents($url);

?>