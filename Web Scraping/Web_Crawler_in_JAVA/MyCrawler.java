import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.Semaphore;
import java.util.regex.Pattern;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class MyCrawler extends WebCrawler {
    static int objcounter = 0;

    private final static Pattern FILTERS = Pattern.compile(
            ".*(\\.(json|rss|css|min.css|js|mid|php|xml|flv|avchd|swf|qt|asf|divx|ico|svg" +
                    "|wav|avi|mov|mpeg|mpg|ram|m4v|wma|wmv|mid|txt" + "|mp2|mp3|mp4|rm|smil|wmv|swf|wma|zip|rar|gz|exe).*)");
    static FileWriter fetchFile = null;
    static FileWriter visitFile = null;
    static FileWriter urlsFile = null;

    static int totalOutgoingUrls = 0;
    static int uniqueUrls = 0;
    static int uniqueUrlsInside = 0;
    static int uniqueUrlsOutside = 0;
    static int totalSites = 0;
    static int totalSuccess = 0;
    static int totalAborted = 0;
    static int totalFail = 0;
    static Semaphore visitSemaphore = new Semaphore(1);
    static Semaphore fetchSemaphore = new Semaphore(1);
    static Semaphore statsSemaphore = new Semaphore(1);



    static Set<String> urlset = new HashSet<>();
    static Map<Integer, Integer> statusCodesCountMap = new HashMap<Integer, Integer>();
    static Set<String> contentTypes = new HashSet<>();
    static Map<String,Integer> contentTypesMap = new HashMap<String, Integer>();

    static int level1 = 0, level2 = 0, level3 = 0, level4 = 0, level5 = 0;
    String prefix = "https://www.reuters.com/", prefix2 = "http://www.reuters.com/";

    public MyCrawler() throws IOException {
        objcounter++;
        fetchFile = new FileWriter("fetch_reuters.csv");
        fetchFile.append("URL");
        fetchFile.append(",");
        fetchFile.append("status code");
        fetchFile.append("\n");

        visitFile = new FileWriter("visit_reuters.csv");
        visitFile.append("URL");
        visitFile.append(",");
        visitFile.append("size");
        visitFile.append(",");
        visitFile.append("Outgoing Links");
        visitFile.append(",");
        visitFile.append("Content-Type");
        visitFile.append("\n");

        urlsFile = new FileWriter("urls_reuters.csv");
        urlsFile.append("URL");
        urlsFile.append(",");
        urlsFile.append("within/not within website");
        urlsFile.append("\n");
    }

    public void uniqueURLstats(WebURL url) {
        if (urlset.contains(url.getURL()) == false) {
            urlset.add(url.getURL());
            uniqueUrls++;
            if (url.getURL().startsWith(prefix))
                uniqueUrlsInside++;
            else
                uniqueUrlsOutside++;
        }
    }

    /**
     * This method receives two parameters. The first parameter is the page
     * in which we have discovered this new url and the second parameter is
     * the new url. You should implement this function to specify whether
     * the given url should be crawled or not (based on your crawling logic).
     * In this example, we are instructing the crawler to ignore urls that
     * have css, js, git, ... extensions and to only accept urls that start
     * with "http://www.viterbi.usc.edu/". In this case, we didn't need the
     * referringPage parameter to make the decision.
     */

    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        try {
            uniqueURLstats(url);

            urlsFile.append(url.getURL().replace(',', '-'));
            urlsFile.append(",");

            if (url.getURL().startsWith(prefix)||url.getURL().startsWith(prefix2))
                urlsFile.append("OK");
            else
                urlsFile.append("N_OK");
            urlsFile.append("\n");

            String href = url.getURL().toLowerCase();
            return !FILTERS.matcher(href).matches() && (href.startsWith(prefix) || url.getURL().startsWith(prefix2));
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public void captureFileSize(long size) {
        int KB = 1024;
        if (size < KB)
            level1++;
        else if (size > KB && size < (KB * 10))
            level2++;
        else if (size > (KB * 10) && size < (KB * 100))
            level3++;
        else if (size > (KB * 100) && size < (KB * 1000))
            level4++;
        else
            level5++;
    }

    /**
     * This function is called when a page is fetched and ready
     * to be processed by your program.
     */
    @Override
    public void visit(Page page) {
        try {
            String url = page.getWebURL().getURL();

            System.out.println("URL: " + url);

            int outgoinglinks = 0;
            visitSemaphore.acquire();
            visitFile.append(url.replace(',', '-'));
            visitFile.append(",");
            visitFile.append("" + page.getContentData().length);
            visitFile.append(",");
            visitSemaphore.release();

            if (page.getParseData() instanceof HtmlParseData) {
                HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
                Set<WebURL> links = htmlParseData.getOutgoingUrls();
                visitSemaphore.acquire();
                outgoinglinks += links.size();
                visitSemaphore.release();
            }
            visitSemaphore.acquire();
            visitFile.append("" + outgoinglinks);
            visitFile.append(",");

            visitFile.append(page.getContentType());
            visitFile.append("\n");

            captureFileSize(page.getContentData().length);
            totalOutgoingUrls += outgoinglinks;
            if (!contentTypes.contains(page.getContentType())) {
                contentTypes.add(page.getContentType());
                contentTypesMap.put(page.getContentType(), 1);
            }
            else {
                contentTypesMap.put(page.getContentType(), contentTypesMap.get(page.getContentType()) + 1);
            }
            visitSemaphore.release();


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void statusCodeStatistics(int statusCode) {
        try {
            statsSemaphore.acquire();
            totalSites += 1;

            if (statusCode >= 200 && statusCode < 300) {
                totalSuccess += 1;
            } else if (statusCode >= 300 && statusCode < 400) {
                totalAborted += 1;
            } else {
                totalFail += 1;
            }

            if (statusCodesCountMap.containsKey(statusCode))
                statusCodesCountMap.put(statusCode, statusCodesCountMap.get(statusCode) + 1);
            else
                statusCodesCountMap.put(statusCode, 1);
            statsSemaphore.release();
        }
         catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {

        statusCodeStatistics(statusCode);
        try {
            fetchSemaphore.acquire();
            fetchFile.append(webUrl.getURL().replace(',', '-'));
            fetchFile.append(",");
            fetchFile.append("" + statusCode);
            fetchFile.append("\n");
            fetchSemaphore.release();

        } catch (Exception e) {
            e.printStackTrace();
        }
        super.handlePageStatusCode(webUrl, statusCode, statusDescription);
    }

    public void printstatictics() {
        System.out.println();
        System.out.println();
        System.out.println("Name: Sairam Kamal Raj");
        System.out.println("News site crawled: www.reuters.com/");
        System.out.println();
        System.out.println("Fetch Statistics");
        System.out.println("=====================");
        System.out.println("#fetches attempted: " + totalSites);
        System.out.println("#fetches succeeded: " + totalSuccess);
        System.out.println("#fetches aborted/failed: " + (totalAborted +totalFail));
        System.out.println();
        System.out.println("Outgoing URLs");
        System.out.println("===================");
        System.out.println("Total URLs extracted: " + totalOutgoingUrls);
        System.out.println("#unique URLs extracted: " + uniqueUrls);
        System.out.println("#unique URLs within News Site: " + uniqueUrlsInside);
        System.out.println("#unique URLs outside News Site: " + uniqueUrlsOutside);

        System.out.println("Status Codes");
        System.out.println("==================");
        for (Integer key : statusCodesCountMap.keySet()) {
            System.out.println(key + " " + statusCodesCountMap.get(key));
        }

        System.out.println("File Sizes:");
        System.out.println("==============");
        System.out.println("< 1KB: " + level1);
        System.out.println("1KB-10KB: " + level2);
        System.out.println("10KB-100KB: " + level3);
        System.out.println("100KB - 1MB: " + level4);
        System.out.println(">=1MB: " + level5);

        System.out.println("Content Types: ");
        System.out.println("=================");
        /*for (String key : contentTypes) {
            System.out.println(key);
        } */
        for (String key : contentTypesMap.keySet()) {
            System.out.println(key + " : " + contentTypesMap.get(key));
        }
    }

    @Override
    public void onBeforeExit() {
        try {
            fetchFile.close();
            visitFile.close();
            urlsFile.close();
            if (objcounter == 7) {
                printstatictics();
                objcounter = -1;
            }

        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
