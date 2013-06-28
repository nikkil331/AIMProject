import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest11 {
	long x = 0;
	private static class Test implements Runnable{
		public void run(){
			SyncBlockTest11 sbt = new SyncBlockTest11();
			synchronized(sbt){
				sbt.x++;
			}
		}
	}
	public static void main(String[] args){
		ExecutorService executor = Executors.newFixedThreadPool(100);
		for(int i = 0; i < 100; i ++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
		
	}

}
