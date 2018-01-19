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
		<li class="current"><a href="Banana.php"><span class="icon"
				data-icon="R"></span>Banana</a></li>
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
			<div class="col_6">

				<div class="notice error">
					<i class="icon-remove-sign icon-large"></i>Banana is very bad <a
						href="#close" class="icon-remove"></a>
				</div>

				<div class="notice warning">
					<i class="icon-warning-sign icon-large"></i> Banana is not good <a
						href="#close" class="icon-remove"></a>
				</div>

				<div class="notice success">
					<i class="icon-ok icon-large"></i> Banana is good <a href="#close"
						class="icon-remove"></a>
				</div>
			</div>
		</div>

	</div>

	<div id="btn-example" align="center">

		<button class="large">Take foto</button>
		<button class="large">Reset</button>
	</div>


</body>
</html>