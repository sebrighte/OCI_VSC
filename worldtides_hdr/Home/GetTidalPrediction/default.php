<?php 

    $stationId = $_GET['stationId']; 

    $apikey = "7fQGFhCmiQtQm8jQY+OfTTDLJzCO4ADkWysG4NFssCQ=";

    $predURL = "https://ukho-tides-test.westeurope.cloudapp.azure.com/API/Tides/api/v1/Stations/EasytidePrediction?api_key=$apikey&portId=$stationId";

    //$predURL = 'https://easytide.admiralty.co.uk/Home/GetPredictionData?stationId=' .$stationId;

    echo file_get_contents($predURL);
    
?>