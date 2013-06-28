public class SyncBlockTest1 {
	private boolean field = false;
	public synchronized void t1(int i){
		if(i == 0) return;
		if(i == 1) {
			boolean var = field;
		}
		if (i >= 2) { field = !field;}
		t1(--i);
	}
	
	
	public static void main(String[] args){
		SyncBlockTest1 sbt = new SyncBlockTest1();
		sbt.t1(2);
	}
}

