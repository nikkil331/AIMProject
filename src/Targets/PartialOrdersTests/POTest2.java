package PartialOrdersTests;

public class POTest2 {
	int a;
	int b;
	int c;
	
	public static void main(String[] args){
		POTest2 pot = new POTest2();
		synchronized(pot){
			pot.a = 1;
			pot.b = 2;
		}
		synchronized(pot){
			pot.b = 2;
			pot.c = 3;
		}
		
		synchronized(pot){
			pot.c = 3;
			pot.a = 1;
		}
	}
}
