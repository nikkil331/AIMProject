import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SyncBlockTest12 {
	int x = 0;
	
	public void read(){
		int y = x;
	}
	
	public void write(){
		x++;
	}
	
	public void neither(){
		int y = 5;
	}
	
	private static class Test implements Runnable{
		public void run(){
			SyncBlockTest12 sbt1 = new SyncBlockTest12();
			SyncBlockTest12 sbt2 = new SyncBlockTest12();
			SyncBlockTest12 sbt3 = new SyncBlockTest12();
			
			synchronized(sbt1){
				sbt1.read();
				synchronized(sbt2){
					sbt2.write();
					synchronized(sbt3){
						sbt3.neither();
					}
				}
			}
		}
	}
	public static void main(String[] args){
		ExecutorService executor = Executors.newFixedThreadPool(10);
		for(int i = 0; i < 10; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
