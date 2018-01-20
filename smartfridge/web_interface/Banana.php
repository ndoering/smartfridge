<?php
require_once 'dbconfig.php';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    
    // Fridgelog Sandard Select
    $sql_std = 'SELECT fid,
                    capturetime,
                    manual_labeled
               FROM fridgelog';
    $qs = $pdo->query($sql_std);
    $qs->setFetchMode(PDO::FETCH_ASSOC);
       
    // Selecting latest entry from joined tables.
    $sql_last_entry = 'SELECT af.afid, fl.fid, class, confidence, prediction, MAX(capturetime) 
                    FROM fridgelog fl, all_fruits af 
                    WHERE af.fid = fl.fid';
    $q_le = $pdo->query($sql_last_entry);
    $q_le->setFetchMode(PDO::FETCH_ASSOC);
    
     while ($row = $q_le->fetch()):
        $class = $row['class'];
        $prediction = $row['prediction'];
        $confidence = $row['confidence'];
        $capturetime = $row['MAX(capturetime)'];
     endwhile;


} catch (PDOException $e) {
    die("Could not connect to the database $dbname :" . $e->getMessage());
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Smart Fridge - Banana</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="css/kickstart.css" media="all" />
</head>
<body>

	<!-- Menu Horizontal -->
	<ul class="menu">
		<li class="current"><a href="Banana.php"><span class="icon"	data-icon="R"></span>Banana</a></li>
		<li><a href="Tomato.php"><span class="icon" data-icon="R"></span>Tomato</a></li>
		<li><a href="db_logs.php"><span class="icon" data-icon="R"></span>Log</a></li>
	</ul>

	<div class="grid">

		<div class="col_12" align="center">
			<h3>Smart Fridge</h3>

			<div class="col_6" style="border: 1px solid red;" align="center">
				<p>
					<img class="align-center"
						src="https://img.purch.com/h/1000/aHR0cDovL3d3dy5saXZlc2NpZW5jZS5jb20vaW1hZ2VzL2kvMDAwLzA2NS8xNDkvb3JpZ2luYWwvYmFuYW5hcy5qcGc="
						width="550" height="350" />
			</div>
			
			<!-- Displaying the fruit's edibility class. -->
			<div class="col_6">
			<?php
			if ($class == 1)
			{
			    echo
			    '<div class="notice error">
    			    <i class="icon-ok icon-large">
                        Banana is bad.
                    </i>
                </div>';
			}
			else if ($class == 2)
			{
			    echo
			    '<div class="notice error">
    			    <i class="icon-ok icon-large">
                        Banana is neutral-bad.
                    </i>
                </div>';
			}
			else if ($class == 3)
			{
			    echo
			    '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Banana is neutral.
                    </i>
                </div>';
			}
			else if ($class == 4)
			{
			    echo
			    '<div class="notice success">
    			    <i class="icon-ok icon-large">
                        Banana is fresh-neutral.
                    </i>
                </div>';
			} 
			else if ($class == 5)
			{
			    echo 
			    '<div class="notice success">
    			    <i class="icon-ok icon-large">
                        Banana is fresh.
                    </i>
                </div>';
			}
			echo
			'<div class="notice warning">
			    <i class="icon-ok icon-large">';
                    echo "Class: $class, Prediction: $prediction, Confidence: $confidence, Time: $capturetime";
                echo '</i>
            </div>';
			?>
			</div>
		</div>

	</div>

	<div id="btn-example" align="center">
		<button class="large">Take foto</button>
		<button class="large">Reset</button>
	</div>


</body>
</html>