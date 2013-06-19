import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.RandomAccessFile;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Pattern;

/*
 * given a textfile and a character, creates a map whose keys
 * are the words in the file beginning with that character
 * and whose values are the number of times that word occurs in the file
 */
public class WordSearch {
	private volatile Map<String, Integer> words = new HashMap<String, Integer>();
	private final int numThreads = 2;
	private final char c;
	
	public WordSearch(String[] files, char c) throws IOException{
		this.c = c;
		
		/*RandomAccessFile rar = new RandomAccessFile(file, "r");
		Scanner scan = new Scanner(new File(file));
		scan.useDelimiter("[\\p{javaWhitespace}[:-@[!-/&&[^']]]]");
		long length = rar.length();
		for(int i = 0; i < numThreads; i++){
			FileWriter out = new FileWriter("out" + i+".txt");
			int bytes = 0;
			while(bytes < length / numThreads && scan.hasNext()){
				String token = scan.next();
				out.write(token.trim() + " ");
				bytes = bytes + token.getBytes().length;
			}
		}*/
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < files.length; i++){
			Searcher t = new Searcher(new Scanner(new File(files[i])));
			executor.execute(t);
		}
		
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
	
	private synchronized void addToList(String word){
		if(words.containsKey(word)){
			words.put(word, words.get(word) + 1);
			return;
		}
		words.put(word, 1);
		
	}
	
	private class Searcher implements Runnable{
		Scanner file;
		public Searcher(Scanner file){
			this.file = file;
			file.useDelimiter(Pattern.compile("\\b"));
		}
		
		@Override
		public void run() {
			while(file.hasNext()){
				String token = file.next();
				if(token.length() == 0) {return;}
				if(token.charAt(0) == c){
					addToList(token);
				}
			}
		}
		
	}
	
	public static void main(String[] args){
		try{
			String[] files = {"hamlet1.txt", "hamlet2.txt"};
			WordSearch search = new WordSearch(files, 'E');
			System.out.println(search.words.size());
			System.out.println(search.words.get("Elsinore"));
		}
		catch(IOException e){
			e.printStackTrace();
			System.exit(1);
		}
	}

}
