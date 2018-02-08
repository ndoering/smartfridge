<?php
// Loading login data for the SQL DataBase Management System
require_once './dbconfig.php';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    
    // 3 Queries. 1 & 2 only for the latest dataset of seperate tables (for the current information)
    // TODO: Unify queies.
    
    // LF - Retrieve latest entry from fridgelog table
    $sql_last_fridgelog = 'SELECT fid, capturetime, full_image FROM fridgelog WHERE fid=(SELECT MAX(fid) FROM fridgelog)';
    $q_lf = $pdo->query($sql_last_fridgelog);
    $q_lf->setFetchMode(PDO::FETCH_ASSOC);
    while ($row = $q_lf->fetch()):
    $lf_fid = $row['fid'];
    $lf_capturetime = $row['capturetime'];
    $lf_full_image = $row['full_image'];
    endwhile;
    
    // LA - Retrieve latest entry from all_fruits
    $sql_last_all_fruits = 'SELECT fid, afid, class, confidence, note
                    FROM all_fruits
                    WHERE afid = (SELECT MAX(afid) FROM all_fruits)
                    AND note ="B"';
    $q_la = $pdo->query($sql_last_all_fruits);
    $q_la->setFetchMode(PDO::FETCH_ASSOC);
    while ($row = $q_la->fetch()):
    $la_fid = $row['fid'];
    $la_afid = $row['afid'];
    $la_class = $row['class'];
    $la_confidence = $row['confidence'];
    endwhile;
    
    // AJ - Retrieve all entries from both tables joined
    $sql_all_join = 'SELECT f.fid, a.afid, capturetime, class, confidence, full_image
                    FROM fridgelog f INNER JOIN all_fruits a
					ON f.fid = a.fid
                    WHERE a.note="B"
                    ORDER BY f.fid DESC';
    $q_aj = $pdo->query($sql_all_join);
    $q_aj->setFetchMode(PDO::FETCH_ASSOC);
    $resultset = array();
    while ($row = $q_aj->fetch()):
    $join_resultset[] = $row;
    endwhile;
    
} catch (PDOException $e) {
    die("Could not connect to the database $dbname :" . $e->getMessage());
}
?>
