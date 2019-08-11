package parsing;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.html.HtmlParser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;


public class  HtmlParse{

	static long startTime = System.nanoTime();
	static int count=0;
		
	public static void defWriteToFile(ArrayList<String> wordList) throws IOException
		{
			
			BufferedWriter bw = new BufferedWriter(new FileWriter("/Users/sairam20/Downloads/Reuters/Reuters/reutersnews/big.txt"));
			for(String x: wordList)
			{   
				bw.write(x);
				bw.newLine();
			}
		    bw.flush();
		}
	
	
	public static void parseFiles(String directoryPath)throws FileNotFoundException, IOException, SAXException, TikaException
		{
	        File dir = new File(directoryPath);
	        File[] files = dir.listFiles();
	        int i =0;
	        ArrayList<String> fullList = new ArrayList<String>();
	        for(File x: files)
	        {
	        	fullList.addAll(parseFile(x));
	        	
	        }
	        defWriteToFile(fullList);
		}
	
	
	public static ArrayList<String> parseFile(File myFile) throws FileNotFoundException, IOException, SAXException, TikaException
		{
		      BodyContentHandler handler = new BodyContentHandler(-1);
		      Metadata metadata = new Metadata();
		      FileInputStream inputstream = new FileInputStream(myFile);
		      ParseContext pcontext = new ParseContext();
		      
		      //Html parser 
		      HtmlParser htmlparser = new HtmlParser();
		      htmlparser.parse(inputstream, handler, metadata,pcontext);
		      String myString = handler.toString();
		      ArrayList bigList1 = new ArrayList(Arrays.asList(myString.split("\\W+")));
		      String[] metadataNames = metadata.names();
		      ArrayList<String> bigList2 = new ArrayList<String>();
		      for(String name : metadataNames) {
		    	  String element=name+":"+metadata.get(name);
		    	  bigList2.add(element);
		      }
		      bigList1.addAll(bigList2);
		      System.out.println(bigList1);
		      count=count+1;
		      System.out.println(count);
		      return bigList1;
		}
	
	
	public static void main(String args[]) throws FileNotFoundException, IOException, SAXException, TikaException 
			{
				try {	
				String directoryPath= "/Users/sairam20/Downloads/Reuters/Reuters/reutersnews/reutersnews/";
				parseFiles(directoryPath);
				}
				catch(Exception e) {
					e.printStackTrace();
				}
				long endTime   = System.nanoTime();
				long totalTime = endTime - startTime;
				System.out.println(totalTime);
			}	
}
