<?php
require_once 'dbconfig.php';
 
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
 
    $sql = 'SELECT fid,
                    capturetime,
                    manual_labeled
               FROM fridgelog';
 
    $q = $pdo->query($sql);
    $q->setFetchMode(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    die("Could not connect to the database $dbname :" . $e->getMessage());
}
?>

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
	<link rel="stylesheet" href="css/kickstart.css" media="all"/>
	<title>Smart Fridge - Logs</title>
</head>

<body>

<!-- Menu Horizontal -->
<ul class="menu">
	<li ><a href="Banana.php"><span class="icon" data-icon="R"></span>Banana</a></li>
	<li ><a href="Tomato.php"><span class="icon" data-icon="R"></span>Tomato</a></li>
	<li class="current" ><a href="db_logs.php"><span class="icon" data-icon="R"></span>Log</a></li>
</ul>


<div class="grid">

<!-- 	<table class="striped" cellspacing="0" cellpadding="0"> -->
	<table class="striped">
		<thead>
			<tr>
				<th>fid</th>
				<th>capturetime</th>
				<th>manuallabeled</th>
			</tr>
		</thead>
                <tbody>
                    <?php while ($row = $q->fetch()): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($row['fid']) ?></td>
                            <td><?php echo htmlspecialchars($row['capturetime']); ?></td>
                            <td><?php echo htmlspecialchars($row['manual_labeled']); ?></td>
                        </tr>
                    <?php endwhile; ?>
			<!-- <tr>
				<td>Item4</td>
				<td>Item5</td>
				<td>Item6</td>
			</tr>
            -->
		</tbody>
	</table>
	
</div>

<!-- TODO:
- Load Image and display image from DB
- Implementing the statements we had in Python. -->

</body>

</html>