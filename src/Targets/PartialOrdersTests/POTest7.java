package PartialOrdersTests;

public class POTest7 {
	private static class Obj{
		int field1;
		int field2;
	}
	public static void main(String[] args){
		Obj o1 = new Obj();
		Obj o2 = new Obj();
		synchronized(o1){
			o1.field1 = 1;
			synchronized(o2){
				o2.field2 = 2;
				o2.field1 = 1;
			}
			o1.field2 = 2;
		}
	}
}
