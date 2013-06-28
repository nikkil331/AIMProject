
public class SyncBlockTest {
	boolean field = false;
	public synchronized void t1(int i){
		if(i == 0) return;
		if(i == 1) {
			boolean var = field;
		}
		if (i >= 2) { field = !field;}
		t1(--i);
	}
	
	private static class Test2{
		public int r = 5;
	}
	
	public static void main(String[] args){
		SyncBlockTest sbt = new SyncBlockTest();
		sbt.t1(2);
		Integer k = new Integer(0);
		synchronized(k){
			//isn't recognized as an access //put hook in for method entrance and exit?
			int c = k; 
		}
		Test2 t2 = new Test2();
		synchronized(t2){
			int rr = t2.r;
		}
	}
}
