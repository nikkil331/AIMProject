package PartialOrdersTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class POTest6 {
	int a;
	int b;
	int c;
	private static class Test implements Runnable{
		POTest6 pot = new POTest6();
		@Override
		public void run(){
			synchronized(pot){
				pot.a = 0;
				pot.b = 1;
			}
			synchronized(pot){
				pot.b = 1;
				pot.c = 2;
			}
		}
	}
	public static void main(String[] args){
		int numThreads = 5;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		Test t = new Test();
		for(int i = 0; i < numThreads; i++){
			executor.execute(t);
		}
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
