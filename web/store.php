<?php
global $a;
if (isset($_GET["SSID"]) && isset($_GET["module"]))
{
	
        $ssid=$_GET["SSID"];
        $password=$_GET["module"];
	if($password =='cavili') {
           $a=1;
           echo "<br />";
           echo "Selected module type cavili";
           $command = escapeshellcmd('python3 /var/www/html/test.py '.$ssid);
           $output = exec($command);
           echo $output;
           
        }else if($password =='simcom') {
           $a=1;
           
           echo "<br />";
           echo "Selected module type simcom";
           //$command = escapeshellcmd('python3 /var/www/html/test.py '.$ssid);
           //$output = exec($command);
           //echo $output;
           
        }else{
           $a=0;
           echo "<br />";
           //echo "<br />";
           echo "Enter module name correctly";
           //echo "<br />";
           //echo "Failed to update APN";
           //echo '<a href="Gsm.html"><br /><br />Return to Previous Page</a>';
        }     
        //$command = escapeshellcmd('python3 /var/www/html/test.py '.$ssid);
        //$output = exec($command);
        //echo $output;
        
	if($return !=0 || $a !=1) {
        //if($return !=0) {
           echo "<br />";
           echo "<br />";
           echo "Failed to update APN";
           echo '<a href="Gsm.html"><br /><br />Return to Previous Page</a>';
        }else{
           echo "<br />";
           echo "<br />";
           echo "Sucessfully updated APN";
           echo '<a href="Gsm.html"><br /><br />Return to Modem Setup Page</a>';
        }
        
} ?>

