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
           
           
        }else if($password =='simcom') {
           $a=1;
           
           echo "<br />";
           echo "Selected module type simcom";
           
           
        }else{
           $a=0;
           echo "<br />";
           
           echo "Enter module name correctly";
          
        }     
        
        
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

