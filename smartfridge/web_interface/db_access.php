<?php
// This class centrally provides all database queries and helper functions.

// =============================== Database Connection & Queries ==================================
// Loading login data for the SQL DataBase Management System
require_once './dbconfig.php';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    
    // 3 Queries. 1 & 2 only for the latest dataset of seperate tables (for the current information)
    // TODO: Unify queries.
    
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
    $sql_last_all_fruits = 'SELECT fid, afid, class, confidence
                    FROM all_fruits
                    WHERE afid = (SELECT MAX(afid) FROM all_fruits)';
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

// =============================== Helper Functions ==================================

// Edibility-Helper function. It converts numbers to edibility terms.
function displayEdibility($arg) {
    if ($arg == 1) {
        $edibility = 'Fresh';
    }
    else if ($arg == 2) {
        $edibility = 'Fresh-neutral';
    }
    else if ($arg == 3) {
        $edibility = 'Neutral';
    }
    else if ($arg == 4) {
        $edibility = 'Neutral-bad';
    }
    else if ($arg == 5) {
        $edibility = 'bad';
    }
    return $edibility;
}

// Notice box style helper function. It changes color according to class
function displayNoticeWithStyle($arg) {
    if ($arg < 3) {
        echo '<div class="notice success">';
    } else if ($arg == 3) {
        echo '<div class="notice warning">';
    } else if ($arg > 3) {
        echo '<div class="notice error">';
    }
    echo '<i class="icon-ok icon-large">';
}

// Entire information box
function displayAllInfo($result, $txt) {
    if ($result['class'] < 3) {
        echo '<div class="notice success">';
    } else if ($result['class'] == 3) {
        echo '<div class="notice warning">';
    } else if ($result['class'] > 3) {
        echo '<div class="notice error">';
    }
    echo '<i class="icon-ok icon-large">';
    echo "$txt";
    echo '<br/>Edibility: ';echo  displayEdibility($result['class']);
    echo '<br/>Confidence: ';echo FLOOR($result['confidence']*100)."%";
    echo '<br/>Capturetime: ';echo  $result['capturetime'];
    echo '</i>';
}

// Notice box for displaying the ENTIRE edibility box according to edibility class.
function displayEdibilityBox($arg) {
    if ($arg == 5) {
        echo
        '<div class="notice error">
            			    <i class="icon-ok icon-large">
                                <strong>Content is bad.</strong>
                            </i>
                            </div>';
    } else if ($arg == 4) {
        echo
        '<div class="notice error">
            			    <i class="icon-ok icon-large">
                                <strong>Content is neutral-bad.</strong>
                            </i>
                        </div>';
    }
    else if ($arg == 3) {
        echo
        '<div class="notice warning">
            			    <i class="icon-ok icon-large">
                                <strong>Content is neutral.</strong>
                            </i>
                        </div>';
    }
    else if ($arg == 2) {
        echo
        '<div class="notice success">
            			    <i class="icon-ok icon-large">
                                <strong>Content is fresh-neutral.</strong>
                            </i>
                        </div>';
    }
    else if ($arg == 1) {
        echo
        '<div class="notice success">
            			    <i class="icon-ok icon-large">
                                <strong>Content is fresh.</strong>
                            </i>
                            </div>';
    }
}

?>
