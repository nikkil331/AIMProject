import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class SyncBlockTest13{
	String x = "string";
	public void read(){
		String s = x;
	}
	public void write(){
		x = "new string";
	}
	public void neither(){
		int y = 5;
	}
	private static class Test implements Runnable{
		@Override
		public void run() {
			SyncBlockTest13 sbt1 = new SyncBlockTest13();
			SyncBlockTest13 sbt2 = new SyncBlockTest13();
			SyncBlockTest13 sbt3 = new SyncBlockTest13();
			
			synchronized(sbt1.x){
				sbt1.read();
				synchronized(sbt2){
					sbt1.write();
					sbt2.neither();
					synchronized(sbt3){
						sbt2.read();
						sbt3.neither();
					}
				}
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
