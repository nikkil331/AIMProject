package PartialOrdersTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class POTest5 {
	int a;
	int b;
	int c;
	
	static POTest5 pot = new POTest5();
	
	private static class AtoB implements Runnable{
		@Override
		public void run(){
			synchronized(pot){
				pot.a = 0;
				pot.b = 1;
			}
		}
	}
	
	private static class AtoC implements Runnable{
		@Override
		public void run(){
			synchronized(pot){
				pot.a = 0;
				pot.c = 2;
			}
		}
	}
	
	private static class BtoC implements Runnable{
		@Override
		public void run(){
			synchronized(pot){
				pot.b = 1;
				pot.c = 2;
			}
		}
	}
	
	public static void main(String[] args){
		int numThreads = 3;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		executor.execute(new AtoB());
		executor.execute(new AtoC());
		executor.execute(new BtoC());
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
