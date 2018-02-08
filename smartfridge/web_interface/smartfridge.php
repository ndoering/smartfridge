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

<!-- =============================== DB Connection & Queries ============================== -->
<?php
// Loading database queries.
require_once './db_access.php';
// Maximum No of Pictures within the fridge image content slider.
$MAX_PICTURES = 10;
?>
<!-- TODOs: 
x Inputmöglichkeit für das Einkaufsdatum.
x Filter
x Prediction over time. -->
<!-- =============================== Page content ============================== -->
<body>

	<!-- Horizontal Menu -->
	<ul class="menu" align="center">
		<li class="current"><a href="smartfridge.php"><span class="icon" data-icon="R">Home</span></a></li>
		<li><a href="statistics.php"><span class="icon" data-icon="R">Statistics</span></a></li>
		<li><a href="db_logs.php"><span class="icon" data-icon="R">Log</span></a></li>
		<?php echo '<li><span class="icon" data-icon="R">Time: '.date('h:i:s');'</span></li>'; ?>
	</ul>

	<div class="grid">

		<div class="col_12" align="center">
			<h3>Welcome to Smart Fridge</h3>
			
			<div id="current_status" align="center">
			<!-- Displaying the current fruit's edibility information permanently. -->
			<h6>Current Edibility Status</h6>
			<?php
			// TODO: Check, wheter a seperate function makes sense.
			if ($la_class == 1)
			{
			    echo
			    '<div class="notice error">
    			    <i class="icon-ok icon-large">
                        Content is bad.
                    </i>
                </div>';
			}
			else if ($la_class == 2)
			{
			    echo
			    '<div class="notice error">
    			    <i class="icon-ok icon-large">
                        Content is neutral-bad.
                    </i>
                </div>';
			}
			else if ($la_class == 3)
			{
			    echo
			    '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Content is neutral.
                    </i>
                </div>';
			}
			else if ($la_class == 4)
			{
			    echo
			    '<div class="notice success">
    			    <i class="icon-ok icon-large">
                        Content is fresh-neutral.
                    </i>
                </div>';
			} 
			else if ($la_class == 5)
			{
			    echo 
			    '<div class="notice success">
    			    <i class="icon-ok icon-large">
                        Content is fresh.
                    </i>
                </div>';
			}
			    // For the permanent notice box under the slider, we use only the latest query data.
			    // TODO: Could be done by using the 3rd query.
    			echo
    			'<div class="notice warning">
    			    <i class="icon-ok icon-large">';
                        echo "Entire Content: Class: $la_class, Confidence: $la_confidence, Time: $lf_capturetime";
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
                            <img src="data:image/jpeg;base64,'.base64_encode( $result['full_image']).'" width="450" height="250"/>';
                            
                            //For each result row's information the edibility class is checked and the appropriate boxes and contents are displayed.
                            if ($result['class'] == 1)
                            {
                                echo
                                '<div class="notice error">
            			    <i class="icon-ok icon-large">
                                Content is bad.
                            </i>
                            </div>';
                            } else if ($result['class'] == 2)
                            {
                                echo
                                '<div class="notice error">
            			    <i class="icon-ok icon-large">
                                Content is neutral-bad.
                            </i>
                        </div>';
                            }
                            else if ($result['class'] == 3)
                            {
                                echo
                                '<div class="notice warning">
            			    <i class="icon-ok icon-large">
                                Content is neutral.
                            </i>
                        </div>';
                            }
                            else if ($result['class'] == 4)
                            {
                                echo
                                '<div class="notice success">
            			    <i class="icon-ok icon-large">
                                Content is fresh-neutral.
                            </i>
                        </div>';
                            }
                            else if ($result['class'] == 5)
                            {
                                echo
                                '<div class="notice success">
            			    <i class="icon-ok icon-large">
                                Content is fresh.
                            </i>
                            </div>';
                            }
                            // Under each edibility box, further information are displayed, not seperatedly formated.
                            echo
                            '<div class="notice warning">
    			             <i class="icon-ok icon-large">';
                            echo 'Entire Content:';
                            echo '<br/>Class: ';echo  $result['class'];
                            echo '<br/>Confidence: ';echo  $result['confidence'];
                            echo '<br/>Capturetime: ';echo  $result['capturetime'];
                            echo '</i>
                            </div>';
                            
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
	// Via old fashioned php function a button calls the system's terminal execution.
	// Using pkill a user signal is envoked on the server side, that triggers our smartfridge process to capture a picture and evaluate it immediately.
	// TODO: Solve via javascript to reduce ugly reload artefacts.
	if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['takephoto']))
	{
	    $cmdoutput = exec('pkill -USR1 -f smartfridge.py');
	    // Wait 5 sec to receive answer and reload freshest data to page.
	    sleep(5);
	    echo
	    '<div class="notice warning">
    			    <i class="icon-ok icon-large">
                        Photo taken. </p>';
	    echo "Shell Output [pkill]: $cmdoutput";
	    echo '</i></div>';
	}?>

</body>
</html>