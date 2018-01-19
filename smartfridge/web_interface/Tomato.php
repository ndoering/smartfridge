<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="css/kickstart.css" media="all" />
    <title>Smart Fridge - Title</title>
</head>

<body>

	<ul class="menu">
		<li><a href="Banana.php"><span class="icon" data-icon="R"></span>Banana</a></li>
		<li class="current"><a href="Tomato.php"><span class="icon"
				data-icon="R"></span>Tomato</a></li>
		<li><a href="db_logs.php"><span class="icon" data-icon="R"></span>Log</a></li>
	</ul>


	<div class="grid">

		<div class="col_12" align="center">
			<h3>Smart Fridge</h3>

			<div class="col_6" style="border: 1px solid red;">
				<p>
					<img class="align-center"
						src="http://djfm.ca/wp-content/uploads/2016/08/Tomato.jpg"
						width="550" height="350" alt="" />
				</p>
			</div>
			<div class="col_6">
				<div class="notice error">
					<i class="icon-remove-sign icon-large"></i> Tomato is very bad <a
						href="#close" class="icon-remove"></a>
				</div>

				<div class="notice warning">
					<i class="icon-warning-sign icon-large"></i> Tomato is not good <a
						href="#close" class="icon-remove"></a>
				</div>

				<div class="notice success">
					<i class="icon-ok icon-large"></i> Tomato is good <a href="#close"
						class="icon-remove"></a>
				</div>
			</div>
		</div>

		<div id="btn-example" align="center">

			<button class="large">Take foto</button>
			<button class="large">Reset</button>
		</div>

	</div>
</body>
</html>