
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest8 {
	private static int numThreads = 3;
	private int x = 0;
	private int y = 0;
	
	public synchronized void write(){
		x = 5;
		y = 6;
	}
	
	private class Test implements Runnable{

		@Override
		public void run() {
			write();
		}
		
	}
	
	public static void main(String[] args){
		SyncBlockTest8 sbt = new SyncBlockTest8();
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(sbt.new Test());
		}
		
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}