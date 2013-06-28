
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest7 {
	private static int numThreads = 3;
	private int x = 0;
	private int y = 0;
	
	public synchronized void read(){
		int y = x;
	}
	
	private class Test implements Runnable{

		@Override
		public void run() {
			read();
		}
		
	}
	
	public static void main(String[] args){
		SyncBlockTest7 sbt = new SyncBlockTest7();
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(sbt.new Test());
		}
		
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
