<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="Smartfridge" content="width=device-width, initial-scale=1.0"/>
    <meta name="description" content="A University project for food edibility analysis and recommendation." />
    <meta name="copyright" content="Goethe University, Frankfurt am Main." />
    
    <link rel="stylesheet" type="text/css" href="css/kickstart.css" media="all" />    <!-- KICKSTART --> 
	<link rel="stylesheet" type="text/css" href="style.css" media="all" />            <!-- CUSTOM STYLES -->
	<script type="text/javascript" src="js/kickstart.js"></script>                    <!-- WORKING? KICKSTART -->
   
    <!-- TODO: Setup Locally bxSllider CSS and JQuery CSS. -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/bxslider/4.2.12/jquery.bxslider.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/bxslider/4.2.12/jquery.bxslider.min.js"></script>
    
    <script>
      $(document).ready(function(){
        $('.slider').bxSlider();
      });
    </script>
    
    <title>Smart Fridge Home Screen</title>
</head>
<!-- ===================================== END HEADER ===================================== -->

<!-- =============================== DB Connection & Helper ============================== -->
<?php
// Including database queries and helper functions.
require_once './db_access.php';
// Maximum No of Pictures within the fridge image content slider.
$MAX_PICTURES = 20;
?>

<!-- =============================== Page content ============================== -->
<body>

	<!-- Horizontal Menu -->
	<ul class="menu" align="center">
		<li class="current"><a href="smartfridge.php"><span class="icon" data-icon="R">Home</span></a></li>
		<li><a href="statistics.php"><span class="icon" data-icon="R">Statistics</span></a></li>
		<li><a href="db_logs.php"><span class="icon" data-icon="R">Log</span></a></li>
		<?php echo '<li><span class="icon" data-icon="R">Time: '.date('h:i:sa');'</span></li>'; ?>
	</ul>

	<div class="grid">

		<div class="col_12" align="center">
			<h3>Welcome to Smart Fridge</h3>
			
			<div id="current_status" align="center">
			<!-- Displaying the current fruit's edibility information permanently. -->
			<h4>Current Status</h4>
			<?php
			    //displayEdibilityBox($la_class);
			    // For the permanent notice box under the slider, we use only the latest query data.
			    displayNoticeWithStyle($la_class);
    			echo "Edibility: ".displayEdibility($la_class)."";
    			echo "<br/>Confidence: ".FLOOR($la_confidence*100)."%";
    			echo "<br/>Timestamp: $lf_capturetime";
                echo '</i>
                </div>';
				?>
        		
        	<!-- Slider containing latest pictures (Defined in the initial php section): 
			It's javascript behavior is assigned via its div class that points to the stylesheet.
			Php creates a list out of the the 3rd queries result (joined tables) and displays images and information belonging to each result's row.-->	
			<div id="slider" class="slider">
			    <?php
			    $cnt = 0;
			    if ($cnt < $MAX_PICTURES) {
    			foreach ($join_resultset as $result){
    			    $cnt++;
                    echo '<div>
                            <img src="data:image/jpeg;base64,'.base64_encode( $result['full_image']).'" width=100% height=100%/>
                            <h6>Please swipe left or right for older data.</h6>';
                            //For each result row's information the edibility class is checked and the appropriate boxes and contents are displayed.
                            displayEdibilityBox($result['class']);
                            // Under each edibility box, further information are displayed, not seperatedly formated.
                            displayAllInfo($result, "Logged Food Status:");
                            echo '</div>';
                            
                       echo '</div>';
    			  }
			    }?>
            </div>
            
            <div id="take_picture" align="center">
                <form action="smartfridge.php" method="post">
                    <input type="submit" name="takephoto" value="Get Update." />
                </form>
    		</div>
			
		</div>
		</div>
	</div>

	<?php
	// Via exec-php function a button calls the system's terminal execution.
	// Using pkill a user signal is envoked on the server side, that triggers our smartfridge process to capture a picture and evaluate it immediately.
	// TODO: Solve via javascript to reduce ugly reload artefacts.
	if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['takephoto']))
	{
	    $cmdoutput = exec('pkill -USR1 -f smartfridge.py');
	    // Wait 14 sec to receive answer and reload freshest data to page.
	    sleep(14);
	    echo
	    '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Photo taken. </p>';
	    echo "Shell Output [pkill]: $cmdoutput";
	    echo '</i></div>';
	}?>

</body>
</html>