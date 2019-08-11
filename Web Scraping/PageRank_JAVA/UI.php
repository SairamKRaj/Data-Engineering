<?php
header('Content-Type: text/html; charset=utf-8');
$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;
if($query)
{
$choice = isset($_REQUEST['sort'])? $_REQUEST['sort'] : "Lucene";
  require_once('./solr-php-client-master/Apache/Solr/Service.php');
  $solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample3');

  if (get_magic_quotes_gpc() == 1)
  {
    $query = stripslashes($query);
  }
  try
  {
  if($choice == "Lucene")
     $parameters=array('sort' => '');
    else{
    $parameters=array('sort' => 'pageRankFile desc');
}
    $results = $solr->search($query, 0, $limit, $parameters);
  }
  catch (Exception $e)
  {
    die("<html><head><title>Reuters Search</title><body><pre>{$e->__toString()}</pre></body></html>");
  }
}
?>
<html>
  <head>
    <title>Sairam_Homework4 - Reuters Search</title>
  </head>
  <body>
    <form  accept-charset="utf-8" method="get" >
      <label for="q">Search:</label>
      <input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/>
      <input type="submit" value="Submit"/>
<br/>
    <input type="radio" name="sort" value="pagerank" <?php if(isset($_REQUEST['sort']) && $choice == "pagerank") { echo 'checked="checked"';} ?>>Page Rank
    <input type="radio" name="sort" value="Lucene" <?php if(isset($_REQUEST['sort']) && $choice == "Lucene") { echo 'checked="checked"';} ?>>Lucene(Default)
    </form>
      
<?php
$csv =  array_map('str_getcsv', file('./URLtoHTML_reuters_news.csv'));
if ($results)
{
  $total = (int) $results->response->numFound;
  $start = min(1, $total);
  $end = min($limit, $total);
  $stack = [];
echo "  <div>Results $start -  $end of $total results:</div> <ol>";
foreach ($results->response->docs as $doc)
  {  
    $id = $doc->id;
$url = $doc->og_url;
    $title = $doc->title;
   $desc = $doc->og_description;
   if($title=="" ||$title==null){
     $title = $doc->dc_title;
     if($title=="" ||$title==null)
       $title="N/A";
   }
	if($desc=="" ||$desc==null)
{
       $desc="N/A";
   }
   //url
   	if($url == "" || $url == null)
	{
	foreach($csv as $row)
		{
			$cmp = "/home/Downloads/Reuters_unzipped/reutersnews/reutersnews/" + $row[0];
			if($id == $cmp)
			{
				$url = $row[1];
				unset($row);
				break;
			}
		}
	}
#   unset($row1);
echo "<li>";
echo "Title : <a href = '$url'>$title</a></br>";
echo	"URL : <a href = '$url'>$url</a></br>";
	echo	"ID : $id</br>";
echo	"Description : $desc </br></br>";
echo "</li>";
  array_push($stack,$id);
}
  echo "</ol>";
  
}
?>

  </body>
</html>