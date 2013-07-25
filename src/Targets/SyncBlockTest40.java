public class SyncBlockTest40 {
	int x = 5;
	public synchronized void read(boolean wantFirst){
		if(wantFirst) { 
			int y = x;
		}
		else readAgain();
	}
	
	public void readAgain(){
		int y = x;
	}
	public static void main(String[] args){
		SyncBlockTest40 sbt = new SyncBlockTest40();
		sbt.read(true);
		sbt.read(false);
	}
}
