<?php
include "config.php";
include "connect.php";

$match = $_POST["match"];
$sentences = $_POST["sentences"];

var_dump($sentences);

$stmt = $conn->prepare('SELECT `sentence_id` from source_material 
WHERE MATCH `sentence_data` AGAINST (?) LIMIT 1');
$stmt->bind_param('s', $match);
$stmt->execute();
$stmt->bind_result($sqlResult); 
while($stmt->fetch()){   
  $sentence_id=$sqlResult; 
} 

$stmt = $conn->prepare("UPDATE source_material
SET score= score+ ?
WHERE `sentence_id` = ?");
$stmt->bind_param("di", $INCREMENT, $sentence_id);
$stmt->execute();

foreach($sentences as $sentence) {
	$stmt = $conn->prepare("UPDATE source_material
	SET score = score - (? / ( ? + score))
	WHERE sentence_id = ?
	AND sentence_id != ?");
	$stmt->bind_param("ddii", $DROPOUT, $DROPOUT, $sentence, $sentence_id);
	$stmt->execute();
}

$stmt = $conn->prepare("UPDATE source_material
SET active = 0
WHERE score < ?");
$stmt->bind_param("d", $MIN_VAL);
$stmt->execute();

$stmt = $conn->prepare("UPDATE source_material
SET active = 1
WHERE score > ? AND active = 0");	
$stmt->bind_param("d", $MIN_VAL);
$stmt->execute();

$stmt = $conn->prepare("UPDATE source_material
SET active = 2
WHERE score > ?");
$stmt->bind_param("d", $MAX_VAL);
$stmt->execute();

echo $sentence_id;

$stmt->close();
$conn->close();
?>