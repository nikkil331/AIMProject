package StaticSyncBlockTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class StaticSBT9 {
	static int numThreads = 10;
	int x = 0; 
	
	public static class Test implements Runnable{
		StaticSBT9 sbt = new StaticSBT9();
		@Override
		public void run(){
			synchronized(sbt){
				synchronized(sbt){
					int y = sbt.x;
				}
			}
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
