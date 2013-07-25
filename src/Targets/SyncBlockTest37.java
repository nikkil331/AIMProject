
public class SyncBlockTest37 {
	int x = 0;
	
	public synchronized void read(int i){
		if(i == 0){
			int y = x;
			return;
		}
		read(i - 1);
	}
	
	public static void main(String[] args){
		SyncBlockTest37 sbt = new SyncBlockTest37();
		sbt.read(10);
	}
}
