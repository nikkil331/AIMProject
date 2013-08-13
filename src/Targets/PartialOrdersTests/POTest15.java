package PartialOrdersTests;


public class POTest15 {
	int a;
	int b;
	int c;
	int d;
	int e;
	int f;
	
	public static void main(String[] args){
		POTest15 pot = new POTest15();
		synchronized(pot){
			pot.e = 4;
			pot.a = 1;
		}
		synchronized(pot){
			pot.a = 0;
			pot.e = 4;
			pot.f = 5;
		}
		synchronized(pot){
			pot.f = 5;
			pot.a = 0;
		}
		synchronized(pot){
			pot.a = 0;
			pot.b = 1;
			pot.e = 4;
		}
		synchronized(pot){
			pot.b = 1;
			pot.c = 2;
		}
		synchronized(pot){
			pot.b = 1;
			pot.d = 3;
		}
		synchronized(pot){
			pot.c = 2;
			pot.d = 3;
			pot.e =4;
		}
	}
}
