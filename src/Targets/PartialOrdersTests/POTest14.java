package PartialOrdersTests;

public class POTest14 {
	int a;
	int b;
	int c;
	int d;
	int e;
	int f;
	int g;
	
	public static void main(String[] args){
		POTest14 pot = new POTest14();
		synchronized(pot){
			pot.a = 0;
			pot.d = 3;
		}
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
		
		synchronized(pot){
			pot.e = 4;
			pot.f = 5;
		}
		synchronized(pot){
			pot.g = 5;
			pot.f = 5;
		}
		synchronized(pot){
			pot.f = 5;
			pot.g = 6;
			pot.e = 4;
		}
	}
}
