package StaticSyncBlockTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class StaticSBT10 {
	static int numThreads = 10;
	Integer x = 0; 
	
	public static class Test implements Runnable{
		StaticSBT10 sbt = new StaticSBT10();
		@Override
		public void run(){
			synchronized(sbt){
				synchronized(sbt.x){
					sbt.x = 5;
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
