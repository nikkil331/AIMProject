import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SyncBlockTest25 {
	Integer arr[] = {1,2,3,4};
	
	public void readArr(){
		synchronized(arr){
			Integer copy[] = arr;
		}
	}
	
	public void writeArr(){
		synchronized(arr){
			arr = new Integer[2];
		}
	}
	
	public synchronized void doNothing(){
		int y = 4;
	}
	
	private static class Test implements Runnable{
		SyncBlockTest25 sbt = new SyncBlockTest25();
		@Override
		public void run(){
			sbt.readArr();
			sbt.writeArr();
			sbt.doNothing();
		}
	}
	public static void main(String[] args){
		int numThreads = 10;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
