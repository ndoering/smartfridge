<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="Smartfridge" content="width=device-width, initial-scale=1.0"/>
    <meta name="description" content="A University project for food edibility analysis and recommendation." />
    <meta name="copyright" content="Goethe University, Frankfurt am Main." />
    
    <link rel="stylesheet" type="text/css" href="css/kickstart.css" media="all" />    <!-- KICKSTART --> 
	<link rel="stylesheet" type="text/css" href="style.css" media="all" />            <!-- CUSTOM STYLES -->
    
    <title>Smart Fridge Database Log</title>
</head>
<!-- ===================================== END HEADER ===================================== -->
<?php
// Loading database queries.
require_once './db_access.php';
?>
<!-- =============================== DB Connection & Queries ============================== -->

<!-- =============================== Page content ============================== -->
<body>

	<!-- Horizontal Menu -->
	<ul class="menu" align="center">
		<li><a href="smartfridge.php"><span class="icon" data-icon="R">Home</span></a></li>
		<li><a href="statistics.php"><span class="icon" data-icon="R">Statistics</span></a></li>
		<li class="current"><a href="db_logs.php"><span class="icon" data-icon="R">Log</span></a></li>
		<?php echo '<li><span class="icon" data-icon="R">Time: '.date('h:i:s');'</span></li>'; ?>
	</ul>
	
	<div class="grid">

		<div class="col_12" align="center">

    <table class="striped">
        <thead>
			<tr>
				<th>a.fid</th>
				<th>a.afid</th>
				<th>capturetime</th>
				<th>class</th>
				<th>confidence</th>
			</tr>
	    </thead>
            <tbody>
            <?php
            $cnt = 0;
            foreach ($join_resultset as $result){
        
                $cnt++;
                echo "<tr>";
                        echo'<td>';echo htmlspecialchars($result['fid']);echo "</td>";
                        echo'<td>';echo htmlspecialchars($result['afid']);echo "</td>";
                        echo'<td>';echo htmlspecialchars($result['capturetime']);echo "</td>";
                        echo'<td>';echo htmlspecialchars($result['class']);echo "</td>";
                        echo'<td>';echo htmlspecialchars($result['confidence']);echo "</td>";
                echo "</tr>";} 
            ?>
        </tbody>
    </table>
    
    </div>
    </div>

</body>
</html>