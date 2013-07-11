package StaticSyncBlockTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;


public class StaticSBT12 {
	static int numThreads = 10;
	int x = 0; 
	
	public synchronized void read(int times){
		if(times == 0) return;
		int y = x;
		read(times - 1);
	}
	
	public static class Test implements Runnable{
		StaticSBT12 sbt = new StaticSBT12();
		@Override
		public void run(){
			sbt.read(10);
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
