<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="Smartfridge" content="width=device-width, initial-scale=1.0" />
<meta name="description"
	content="A University project for food edibility analysis and recommendation." />
<meta name="copyright" content="Goethe University, Frankfurt am Main." />

<!-- JS / CSS local library for UI Layout.-->
<link rel="stylesheet" type="text/css" href="css/kickstart.css"
	media="all" />
<!-- KICKSTART -->
<link rel="stylesheet" type="text/css" href="style.css" media="all" />
<!-- CUSTOM STYLES -->

<!-- JS / CSS local library for Chart visualization.-->
<link rel="stylesheet" href="dist/chartist.css">
<script src="dist/chartist.min.js" type="text/javascript"></script>

<title>Smart Fridge Statistics</title>
</head>
<!-- ===================================== END HEADER ===================================== -->
<?php
// Loading database queries.
require_once './db_access.php';
$MAXPOINTS = 10;
?>
<!-- =============================== Page content ============================== -->
<body>

	<!-- Horizontal Menu -->
	<ul class="menu" align="center">
		<li><a href="smartfridge.php"><span class="icon" data-icon="R">Home</span></a></li>
		<li class="current"><a href="statistics.php"><span class="icon"
				data-icon="R">Statistics</span></a></li>
		<li><a href="db_logs.php"><span class="icon" data-icon="R">Log</span></a></li>
		<?php echo '<li><span class="icon" data-icon="R">Time: '.date('h:i:sa');'</span></li>'; ?>
	</ul>

	<div class="grid">

		<div class="col_12" align="center">

			<!-- Charts -->
			<div class="ct-chart ct-perfect-fourth">
				<script type="text/javascript">

					// Initializing JS-Arrays
    				var class_ar = [];
    				var time_ar = [];
					
    			    // Loading content from joined table query results via php loop.
                    <?php 
                    $i = 0;
    				foreach (array_reverse($join_resultset) as $result){
    				    // Copy content from SQL results into JS-Arrays. 
    				    if ($i < $MAXPOINTS) {
    				        echo "time_ar[$i] = '$result[capturetime]';"; // js within php
    				        echo "class_ar[$i] = parseInt($result[class]);"; // js within php
    				    }
    				    $i++;
                    }
    				?>
    				//console.log(class_ar);
    				//console.log(time_ar);
    				
    				// Creating Chartist Object, using arrays as paramteters
                	new Chartist.Line('.ct-chart', {
                		  labels: 
                    	  //['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                		  time_ar,
                		  series: [
                    		class_ar,
                		  ]
                		}, {
                		  fullWidth: true,
                		  chartPadding: {
                		    right: 40
                		  }
                		});
            	</script>
			</div>
			
		</div>
	</div>

</body>
</html>