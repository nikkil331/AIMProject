import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest11 {
	long x = 0;
	private static class Test implements Runnable{
		public void run(){
			SyncBlockTest11 sbt = new SyncBlockTest11();
			synchronized(sbt){
				sbt = new SyncBlockTest11();
			}
		}
	}
	public static void main(String[] args){
		int numThreads = 2;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i ++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
		
	}

}
