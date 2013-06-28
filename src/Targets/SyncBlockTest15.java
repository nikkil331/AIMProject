import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SyncBlockTest15 {
	private Integer[] arr = {1,2,3,4,5,6,7,8,9,10};
	
	public synchronized void read(){
		synchronized(arr){
			int x = arr[5];
		}
	}
	
	public synchronized void write(){
		int index = (int)Thread.currentThread().getId() % 10; 
		synchronized(arr){
			arr[index] = arr[index] + 1;
		}
	}
	private static class Test implements Runnable{
		SyncBlockTest15 sbt = new SyncBlockTest15();
		@Override
		public void run(){
			sbt.read();
			sbt.write();
		}
	}
	public static void main(String[] args){
		int numThreads = 50;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
