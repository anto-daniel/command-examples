<?php 
 $results = shell_exec ("./search \"" . $_POST["word"] . "\" 3") ; 
 
 print " 
 <html> 
 <head> 
 <title> About.com's Python Program Results.</title> 
 <link rel=\"stylesheet\" type=\"text/css\" href=\"./myway.css\" /> 
 </head> 
 <body> 
 
 <div class=\"search\"> 
 <form action=\"search.php\" method=\"post\"> 
 <h5>Search <br> 
 <input type=\"text\" name=\"word\" size=\"20\" onChange=\"submit(word)\"><br> 
 <!-- <input type=\"submit\" value=\"Submit\" /> </h5> --> 
 </form> 
 </div> 
 
 <h1 class=\"welcome\"> Welcome to Python with PHP and Javascript </h1> 
 
 <h6 class=\"maintext\"> "; 
 
 print $results; 
 print "</h6> </body> </html>"; 
 ?> 
