package PartialOrdersTests;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class POTest8 {
	int a;
	int b;
	int c;
		
	static POTest8 pot = new POTest8();
		
	private static class AtoB implements Runnable{
		@Override
		public void run(){
			synchronized(pot){
				pot.a = 0;
				synchronized(pot){
					pot.b = 1;
				}
			}
		}
	}
		
	private static class AtoC implements Runnable{
		@Override
		public void run(){
			synchronized(pot){
				pot.a = 0;
				synchronized(pot){
					pot.c = 2;
				}
			}
		}
	}
		
	private static class BtoC implements Runnable{
		@Override
		public void run(){
			synchronized(pot){
				pot.b = 1;
				synchronized(pot){
					pot.c = 2;
				}
			}
		}
	}

	public static void main(String[] args){
		int numThreads = 3;
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		executor.execute(new AtoB());
		executor.execute(new BtoC());
		executor.execute(new AtoC());
		executor.shutdown();
		while(!executor.isTerminated()){}
	}
}
