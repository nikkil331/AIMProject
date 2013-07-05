import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest34 {
	Object o = new Object();
	public void write(){
		o = new Object();
	}
	private static class Test implements Runnable{
		@Override
		public void run() {
			SyncBlockTest34 sbt1 = new SyncBlockTest34();
			
			synchronized(sbt1.o){
				sbt1.write();
			}
		}
	}
	public static void main(String[] args){
		int numThreads = 100;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
