
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest7 {
	private static int numThreads = 3;
	private Integer x = 0;
	
	public synchronized void read(){
		int y = x;
	}
	
	private class SBT7Test implements Runnable{

		@Override
		public void run() {
			read();
		}
		
	}
	
	public static void main(String[] args){
		SyncBlockTest7 sbt = new SyncBlockTest7();
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(sbt.new SBT7Test());
		}
		
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
