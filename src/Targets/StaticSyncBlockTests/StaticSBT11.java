package StaticSyncBlockTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class StaticSBT11 {
	static int numThreads = 10;
	int x = 0;
	
	public synchronized void read(){
		int y = x;
	}
	
	public static class Test implements Runnable{
		StaticSBT11 sbt1 = new StaticSBT11();
		StaticSBT11 sbt2 = new StaticSBT11();
		
		@Override
		public void run(){
			sbt1.read();
			sbt2.read();
		}
	}
	
	public static void main(String[] args){
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated());
	}
}
