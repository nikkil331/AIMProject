import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest17 {
	Inner in = new Inner();
	
	public synchronized void read(){
		synchronized(in){
			int y = in.x;
		}
	}
	
	public synchronized void write(){
		synchronized(in){
			in.x++;
		}
	}
	
	public class Inner{
		int x = 0;
	}
	
	private static class Test implements Runnable{

		@Override
		public void run() {
			SyncBlockTest17 sbt = new SyncBlockTest17();
			
			for(int i = 0; i < 10; i++){
				sbt.read();
				sbt.write();
			}
			
		}
		
	}
	
	public static void main(String[] args){
		int numThreads = 10;
		ExecutorService executors = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executors.execute(new Test());
		}
		executors.shutdown();
		while(!executors.isTerminated()){}
	}
}
