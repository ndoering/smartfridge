<?php
require_once './dbconfig.php';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    
    // Selecting latest entry from joined tables. To Fix latest Image
    $sql_last_entry = 'SELECT fid, capturetime, full_image FROM fridgelog WHERE fid=(SELECT MAX(fid) FROM FRIDGELOG)';
    
    $q_le = $pdo->query($sql_last_entry);
    $q_le->setFetchMode(PDO::FETCH_ASSOC);
    
    while ($row = $q_le->fetch()):
    $class = 1;//$row['class'];
    $note = 1;//$row['note'];
    $confidence = 1;//$row['confidence'];
    $capturetime = $row['capturetime'];
    $full_image = $row['full_image'];
    endwhile;
    
} catch (PDOException $e) {
    die("Could not connect to the database $dbname :" . $e->getMessage());
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Smart Fridge Home Screen</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="css/kickstart.css" media="all" />
</head>
<body>

	<!-- Menu Horizontal -->
	<ul class="menu">
		<li class="current"><a href="smartfridge.php"><span class="icon" data-icon="R"></span>Home</a></li>
		<li><a href="db_logs.php"><span class="icon" data-icon="R"></span>Log</a></li>
	</ul>

	<div class="grid">

		<div class="col_12" align="center">
			<h3>Smart Fridge</h3>
			
			<div class="col_6" style="border: 1px solid red;" align="center">
			<!-- Displaying the fruit's latest picture. -->
			<?php
			echo '<img src="data:image/jpeg;base64,'.base64_encode( $full_image).'" width="550" height="350"/>';
            ?>
			</div>
			
			<div class="col_6">
			<!-- Displaying the fruit's edibility information. -->
			<?php
			if ($class == 1)
			{
			    echo
			    '<div class="notice error">
    			    <i class="icon-ok icon-large">
                        Content is bad.
                    </i>
                </div>';
			}
			else if ($class == 2)
			{
			    echo
			    '<div class="notice error">
    			    <i class="icon-ok icon-large">
                        Content is neutral-bad.
                    </i>
                </div>';
			}
			else if ($class == 3)
			{
			    echo
			    '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Content is neutral.
                    </i>
                </div>';
			}
			else if ($class == 4)
			{
			    echo
			    '<div class="notice success">
    			    <i class="icon-ok icon-large">
                        Content is fresh-neutral.
                    </i>
                </div>';
			} 
			else if ($class == 5)
			{
			    echo 
			    '<div class="notice success">
    			    <i class="icon-ok icon-large">
                        Content is fresh.
                    </i>
                </div>';
			}
    			echo
    			'<div class="notice warning">
    			    <i class="icon-ok icon-large">';
                        echo "Entire Content: Class: $class, Confidence: $confidence, Time: $capturetime";
                    echo '</i>
                </div>';
            // Die Notiz je nach Note anzeigen lassen.
//                 echo
//                 '<div class="notice warning">
//     			    <i class="icon-ok icon-large">';
//                     echo "Banana Content: Class: $bclass, Confidence: $bconfidence, Time: $bcapturetime";
//                     echo '</i>
//                 </div>';?>
<!-- 			</div> -->
			
			<div id="btn-example" align="center">
                <form action="smartfridge.php" method="post">
                    <input type="submit" name="takephoto" value="Take Photo." />
                    <input type="submit" name="reset" value="Reset." />
                </form>
    		</div>
			
		</div>

	</div>

	<?php
	if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['takephoto']))
	{
	    // Todo:
	    // Execute the Command line for taking photo.
	    // Nils could implement a "take snapshot executable."
	    $cmdoutput = exec('pkill -USR1 -f smartfridge.py');
	    //$cmdoutput = exec('pkill -USR1');
	    echo
	    '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Photo taken. </p>';
	    echo "Shell Output [pkill]: $cmdoutput";
	    echo
	    '</i>
              </div>';
	}
	else if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['reset']))
	{
	    // Todo:
	    // What should be done on this reset request?
	    echo '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Reset successfull.
                    </i>
              </div>';
    }?>

</body>
</html>