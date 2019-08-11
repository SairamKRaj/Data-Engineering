<?php
ini_set('memory_limit','-1');
// make sure browsers see this page as utf-8 encoded HTML
include 'SpellCorrector.php';
include 'simple_html_dom.php';
header('Content-Type: text/html; charset=utf-8');
$div=false;
$correct = "";
$correct1="";
$output = "";
$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;
if ($query)
{
  $choice = isset($_REQUEST['sort'])? $_REQUEST['sort'] : "default";
  require_once('./solr-php-client-master/Apache/Solr/Service.php');
  $solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample3');
  if( ! $solr->ping()) { 
            echo 'Solr service is not available'; 
  } 
  else{
     
  }
  // if magic quotes is enabled then stripslashes will be needed
  if (get_magic_quotes_gpc() == 1)
  {
    $query = stripslashes($query);
  }
  try
  {
    if (isset($_GET['search']) && $_GET['search']=="lucene")
      $additionalParameters=array('sort' => '');
    else{
      $additionalParameters=array('sort' => 'pageRankFile desc');
    }
    $word = explode(" ",$query);
    $spell = $word[sizeof($word)-1];
    
     for($i=0;$i<sizeOf($word);$i++){
      ini_set('memory_limit',-1);
      ini_set('max_execution_time', 300);
     $che = SpellCorrector::correct($word[$i]);
     if($correct!="")
        $correct = $correct."+".trim($che);
      else{
        $correct = trim($che);
      }
        $correct1 = $correct1." ".trim($che);
    }
    $correct1 = str_replace("+"," ",$correct);
    $div=false;
    if(strtolower($query)==strtolower($correct1)){
       $results = $solr->search($query, 0, $limit, $additionalParameters);
    }
    else {
      $div =true;
      $results = $solr->search($query, 0, $limit, $additionalParameters);
      $link = "http://localhost/UI4.php?q=$correct&sort=$choice";
      $output = "Did you mean?: <a href='$link'>$correct1</a>";
    }
  }
  catch (Exception $e)
  {
    die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
  }
}
?>
<html>
  <head>
    <title>Sairam_Homework5 - Reuters Search</title>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
    <script src="http://code.jquery.com/jquery-1.10.2.js"></script>
    <script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <!--meta http-equiv="refresh" content="15;URL='http://localhost/UI4.php'"/-->
  </head>
  <body style= "background-color:orange; opacity=0.4;">
     <h1 align="center"><u> Enhanced Reuters Search </u></h1><br/>
    <form accept-charset="utf-8" method="get" id="searchform" align="center">
      Search: <input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>" list="searchresults" placeholder="Search the Solr or Type URL " autocomplete="off"/>
      <datalist id="searchresults"></datalist>
        <br><br>
        <input type="radio" name="sort" <?php if (isset($_GET['search']) && $_GET['search']=="lucene") echo 'checked="checked"';?>  value="lucene" /> Lucene(Default)
	<input type="radio" name="sort" <?php if (isset($_GET['search']) && $_GET['search']=="pagerank") echo 'checked="checked"';?> value="pagerank" /> PageRank <br><br>
      <input type="submit" value="Submit"/>
      
    </form>
    <script>
   $(function() {
     var URL_PREFIX = "http://localhost:8983/solr/myexample3/suggest?q=";
     var URL_SUFFIX = "&wt=json&indent=true";
     var count=0;
     var tags = [];
     $("#q").autocomplete({
       source : function(request, response) {
         var correct="",before="";
         var query = $("#q").val().toLowerCase();
         var character_count = query.length - (query.match(/ /g) || []).length;
         var space =  query.lastIndexOf(' ');
         if(query.length-1>space && space!=-1){
          correct=query.substr(space+1);
          before = query.substr(0,space);
        }
        else{
          correct=query.substr(0); 
        }
        var URL = URL_PREFIX + correct+ URL_SUFFIX;
        $.ajax({
         url : URL,
         success : function(data) {
          var js =data.suggest.suggest;
          var docs = JSON.stringify(js);
          var jsonData = JSON.parse(docs);
          var result =jsonData[correct].suggestions;
          var j=0;
          var stem =[];
          for(var i=0;i<5 && j<result.length;i++,j++){
            if(result[j].term==correct)
            {
              i--;
              continue;
            }
            for(var k=0;k<i && i>0;k++){
              if(tags[k].indexOf(result[j].term) >=0){
                i--;
                continue;
              }
            }
            if(result[j].term.indexOf('.')>=0 || result[j].term.indexOf('_')>=0)
            {
              i--;
              continue;
            }
            var s =(result[j].term);
            if(stem.length == 5)
              break;
            if(stem.indexOf(s) == -1)
            {
              stem.push(s);
              if(before==""){
                tags[i]=s;
              }
              else
              {
                tags[i] = before+" ";
                tags[i]+=s;
              }
            }
          }
          console.log(tags);
          response(tags);
        },
        dataType : 'jsonp',
        jsonp : 'json.wrf'
      });
      },
      minLength : 1
    })
   });
 </script>
<?php
if ($div){
  echo $output;
}
$csvArray =  array_map('str_getcsv', file('./URLtoHTML_reuters_news.csv'));
$count =0;
$pre="";

if ($results)
{
  $total = (int) $results->response->numFound;
  $start = min(1, $total);
  $end = min($limit, $total);
  $link;
?>
    <div>Results <?php echo $start; ?> - <?php echo $end;?> of <?php echo $total; ?>:</div>
    <ol>
<?php
  
  foreach ($results->response->docs as $doc)
  {
    
    $id = $doc->id;
    $link = $doc->value;
    $or_id = $id;
    $id = str_replace("/home/sairam/Downloads/Reuters_unzipped/reutersnews/reutersnews/","",$id);
    $descp = $doc->og_description;
    $title = $doc->title;
    if(is_array($title))
    {
    $title = implode(" ",$title);
    }
    foreach ($csvArray as $key ) {
      
      if ($id == $key[0]){
        $link = $key[1];
        break;
      }
    }
    
    $searchterm = $_GET["q"];//search content
    $ar = explode(" ", $searchterm);
    $html_to_text_files_dir = "./reutersnews/";
    $filename = $html_to_text_files_dir . $id;
    $html = file_get_contents($filename);
    $sentences = explode(".", $html);
    $words = explode(" ", $query);
    $snippet = "";
    $snippet1 = "";
    $text = "/";
    $start_delim="(?=.*?\b";
    $end_delim="\b)";
    foreach($words as $item){
      $text=$text.$start_delim.$item.$end_delim;
    }
    $text=$text."^.*$/i";
    foreach($sentences as $sentence){
      $sentence=strip_tags($sentence);
      if (preg_match($text, $sentence)>0){
        if (preg_match("(&gt|&lt|\/|{|}|[|]|\|\%|>|<|:)",$sentence)>0){
          continue;
        }
        else{
          $snippet = $snippet.$sentence;
          if(strlen($snippet)>160) 
            break;
        }
      }
     }
    $words = preg_split('/\s+/', $query);
    foreach($words as $item)
	$snippet = str_ireplace($item, "<strong>".$item."</strong>",$snippet);
    if($snippet == ""){
      $snippet="There are no sentences which has a match with the query terms in the entered order or in any order.";
    }

?>
      <li>
        <table style="border: 0px solid black; width=500px text-align: left">
          <tr>
            <qw><?php print "<a href = '{$link}' STYLE='text-decoration:none'><font size='4px'><b>".$title."</b></font></a>" ?></qw>
          </tr>
          <tr>
            <th><?php echo htmlspecialchars("link", ENT_NOQUOTES, 'utf-8'); ?></th>
            <td><?php echo "<a href = '{$link}' STYLE='text-decoration:none'><st>".$link."</st></a>" ?></td>
          </tr>
          <tr>
            <th><?php echo htmlspecialchars("id", ENT_NOQUOTES, 'utf-8'); ?></th>
            <td><?php echo htmlspecialchars($id, ENT_NOQUOTES, 'utf-8'); ?></td>
          </tr>
          <tr>
            <th><?php echo htmlspecialchars("description", ENT_NOQUOTES, 'utf-8'); ?></th>
            <td><?php echo htmlspecialchars($doc->og_description, ENT_NOQUOTES, 'utf-8'); ?></td>
          </tr>
          <tr>
            <th><?php echo htmlspecialchars("snippet", ENT_NOQUOTES, 'utf-8'); ?></th>
            <td><?php 
            if($snippet == "N/A"){
              echo htmlspecialchars($snippet, ENT_NOQUOTES, 'utf-8');
            }else{
              echo "...".$snippet."...";
            }
            ?></td>
          </tr>
          <tr>
            <th><br></th>
            <td><br></td>
          </tr>
        </table>
      </li>
<?php
  }
?>
    </ol>
<?php
}
?>
  </body>
</html>
