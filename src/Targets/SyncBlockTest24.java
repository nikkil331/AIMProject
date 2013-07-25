import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest24 {
	private Integer x = 2;
	public void readX(){
		synchronized(x){
			int y = x;
		}
	}
	public void writeX(){
		synchronized(x){
			x++;
		}
	}
	public synchronized void doNothing(){ 
		int x = 5;
	}
	
	private static class Test implements Runnable{
		SyncBlockTest24 sbt = new SyncBlockTest24();
		@Override
		public void run(){
			sbt.readX();
			sbt.writeX();
			sbt.doNothing();
		}
	}
	
	public static void main(String[] args){
		int numThreads = 20;
		ExecutorService executors = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executors.execute(new Test());
		}
		executors.shutdown();
		while(!executors.isTerminated()){}
	}
}
