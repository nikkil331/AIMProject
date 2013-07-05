import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest16 {
	Integer[][] arr = new Integer[5][5];
	
	public SyncBlockTest16(){
		for(int i = 0; i < 5; i++){
			for(int j = 0; j < 5; j++){
				arr[i][j] = i + j;
			}
		}
	}
			
	public synchronized void read(){
		synchronized(arr[1]){
			int x = arr[1][2];
		}
	}
	
	public synchronized void write(){
		synchronized(arr[1]){
			arr[1] = new Integer[5];
			for(int i = 0; i < 5; i++){
				arr[1][i] = 1 + i;
			}
		}
	}
	public synchronized void neither(){ int y = 5;}
	
	private static class Test implements Runnable{
		SyncBlockTest16 sbt = new SyncBlockTest16();
		
		@Override
		public void run(){
			for(int i = 0; i < 10; i++){
				sbt.read();
				sbt.write();
				sbt.neither();
			}
		}
	}
	
	public static void main(String[] args){
		int numThreads = 25;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()) {}
	}
}
