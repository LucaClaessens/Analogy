
<?php
include "config.php";
include "connect.php";

$sql ="SELECT sentence_id, sentence_data, score, RAND() * score AS weighted_score FROM source_material WHERE active = 1 ORDER by weighted_score DESC LIMIT 10";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
	$data = $result->fetch_all( MYSQLI_ASSOC );
	echo json_encode( $data );
	} else {
    	echo "0 results";
	}
$conn->close();

?>