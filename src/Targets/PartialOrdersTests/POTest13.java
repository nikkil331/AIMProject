package PartialOrdersTests;

public class POTest13 {
	int a;
	int b;
	int c;
	int d;
	
	public static void main(String[] args){
		POTest13 pot = new POTest13();
		synchronized(pot){
			pot.a = 0;
			pot.c = 2;
		}
		
		synchronized(pot){
			pot.a = 0;
			pot.b = 1;
		}
		
		synchronized(pot){
			pot.b = 1;
			pot.c = 2;
		}
		synchronized(pot){
			pot.c = 2;
			pot.d = 3;
		}
		synchronized(pot){
			pot.d = 3;
			pot.a = 1;
		}
	}
}
