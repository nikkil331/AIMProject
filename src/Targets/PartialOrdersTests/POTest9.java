package PartialOrdersTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class POTest9 {
	int a;
	int b;
	private static class Test implements Runnable{
		POTest9 pot = new POTest9();
		@Override
		public void run(){
			synchronized(pot){
			pot.a = 0;
			pot.b = 1;
			}
		}
	}
	
	public static void main(String[] args){
		int numThreads=5;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		for(int i = 0; i < numThreads; i++){
			executor.execute(new Test());
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
