package PartialOrdersTests;

public class POTest3 {
	int a;
	int b;
	int c;
	
	public static void main(String[] args){
		POTest3 pot = new POTest3();
		synchronized(pot){
			pot.a = 1;
			synchronized(pot){
				pot.b = 2;
			}
		}
		
		synchronized(pot){
			pot.b = 2;
			pot.c = 3;
		}
	}
}
