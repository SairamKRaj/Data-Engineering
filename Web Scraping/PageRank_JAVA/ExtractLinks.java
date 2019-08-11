package pagerank;

import java.io.*;
import java.util.*;
import org.jsoup.*;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


public class ExtractLinks {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String name = "/Users/sairam20/Downloads/Reuters/Reuters/URLtoHTML_reuters_news.csv";
		String line = "";
        String cvsSplitBy = ",";
        HashMap<String, String> fileUrlMap = new HashMap<>();
        HashMap<String, String> urlFileMap = new HashMap<>();
        System.out.println("1");
        try {
        	BufferedReader br = new BufferedReader(new FileReader(name));
        	PrintWriter writer = new PrintWriter("edgeList.txt", "UTF-8");
        	System.out.println("2");
        	while ((line = br.readLine()) != null) {

                String[] country = line.split(cvsSplitBy);
               // System.out.println(country[0]+"----"+country[1]+"----"+country.length);
                fileUrlMap.put(country[0],country[1]);
                
                urlFileMap.put(country[1],country[0]);
                
            }
        	System.out.println(fileUrlMap.size());
        	String dirPath="/Users/sairam20/Downloads/Reuters/Reuters/reutersnews/reutersnews";
        	File dir = new File(dirPath);
        	
        	Set<String> edges = new HashSet<>();
        	int count=0;
        	for(File file : dir.listFiles()) {
			System.out.println("Count" + (++count));
        		Document doc = Jsoup.parse(file, "UTF-8", fileUrlMap.get(file.getName()));
        		Elements links = doc.select("a[href]");
        		
        		for(Element link : links) {
        			String url = link.attr("abs:href").trim();
        			if(urlFileMap.containsKey(url)) {
        				//System.out.println(file.getName()+"-------"+urlFileMap.get(url));
        				edges.add("/Users/sairam20/Downloads/Reuters/Reuters/reutersnews/reutersnews"+file.getName() + " " + "/Users/sairam20/Downloads/Reuters/Reuters/reutersnews/reutersnews"+urlFileMap.get(url));
        			}
        		}
        		       		
        	}
        	
        	for(String s : edges) {
        		writer.println(s);
        	}
        	
        	writer.flush();
        	writer.close();
        	System.out.println("Done");
        }
        catch(Exception e) {
        	e.printStackTrace();
        }
	}

}
