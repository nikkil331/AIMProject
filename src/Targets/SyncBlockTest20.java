import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest20 {
	volatile Integer x = 0;
	
	public synchronized void read(){
		int y = x;
	}
	
	public synchronized void write(){
		x++;
	}
	public synchronized void neither(){
		int y = 2;
	}
	
	private static class Test implements Runnable{
		SyncBlockTest20 sbt = new SyncBlockTest20();
		
		@Override
		public void run() {
			sbt.write();
			sbt.neither();
			sbt.read();
		}
		
	}
	public static void main(String[] args){
		int numThreads = 10;
		ExecutorService executors = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i<numThreads; i++){
			executors.execute(new Test());
		}
			executors.shutdown();
			while(!executors.isTerminated()){}
	}
}
