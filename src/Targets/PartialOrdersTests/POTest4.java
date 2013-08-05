package PartialOrdersTests;

public class POTest4 {
	int a;
	int b;
	int c;
	int d;
	
	public synchronized void read1(){
		a = 0;
		d = 3;
	}
	
	public synchronized void read2(){
		d = 3;
	}
	
	public synchronized void read3(){
		a = 0;
		b = 1;
	}
	
	public synchronized void read4(){
		b = 1;
		d = 3;
	}
	
	public synchronized void read5(){
		b = 1;
		c = 2;
	}
	
	public static void main(String[] args){
		POTest4 pot = new POTest4();
		pot.read2();
		pot.read4();
		pot.read1();
		pot.read5();
		pot.read3();
	}
}
