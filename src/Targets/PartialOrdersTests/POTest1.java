package PartialOrdersTests;

public class POTest1 {
	int a;
	int b;
	int c;
	int d;
	
	public static void main(String[] args){
		POTest1 pot = new POTest1();
		synchronized(pot){
			pot.a = 1;
			pot.c = 3;
		}
		synchronized(pot){
			pot.b = 2;
			pot.d = 4;
		}
		synchronized(pot){
			pot.a = 1;
			pot.b = 2;
		}
		synchronized(pot){
			pot.b = 2;
			pot.c = 3;
		}
	}
}
