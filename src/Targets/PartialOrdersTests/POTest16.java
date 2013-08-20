package PartialOrdersTests;

public class POTest16 {
	int a;
	int b;
	int c;
	int d;
	int e;
	int f;
	int g;
	
	public static void main(String[] args){
		POTest16 pot = new POTest16();
		synchronized(pot){
			pot.b = 1;
			pot.d = 3;
			pot.g = 6;
		}
		synchronized(pot){
			pot.g = 6;
			pot.d = 3;
		}
		synchronized(pot){
			pot.c = 2;
			pot.e = 4;
		}
		synchronized(pot){
			pot.a = 0;
			pot.f = 5;
		}
		synchronized(pot){
			pot.a = 0;
			pot.b = 1;
			pot.c = 2;
		}
		synchronized(pot){
			pot.c = 2;
			pot.a = 0;
		}
	}
}
