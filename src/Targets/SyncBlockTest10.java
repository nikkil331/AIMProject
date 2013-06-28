import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SyncBlockTest10 {
	int x = 0;
	public synchronized void read(){
		int y = x;
	}
	public synchronized void write(){
		x = 2;
	}
	public synchronized void neither(){
		int y = 3;
	}
	private static class Test implements Runnable{
		
		@Override
		public void run() {
			SyncBlockTest10 sbt = new SyncBlockTest10();
			for(int i = 0; i < 5; i++){
				sbt.read();
			}
			for(int i = 0; i < 5; i++){
				sbt.write();
			}
			for(int i = 0; i < 5; i++){
				sbt.neither();
			}
		}
		
	}
	
	public static void main(String[] args){
		ExecutorService executor = Executors.newFixedThreadPool(2);
		executor.execute(new Test());
		executor.execute(new Test());
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
