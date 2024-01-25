<?php
if (isset($_GET["SSID"]))
{
	
        $ssid=$_GET["SSID"];
        $command = escapeshellcmd('python3 /var/www/html/test.py '.$ssid);
        $output = exec($command);
        echo $output;
        
	
        if($return !=0) {
           echo "<br />";
           echo "Failed to update APN";
           echo '<a href="Wlan.html"><br /><br />Return to Previous Page</a>';
        }else{
           echo "<br />";
           echo "<br />";
           echo "Sucessfully updated APN";
           echo '<a href="Wlan.html"><br /><br />Return to Modem Setup Page</a>';
        }
        
} ?>

