public class SyncBlockTest43 {
	Integer x = 0;
	
	public synchronized void readOrWrite(boolean isRead){
		if (isRead) read();
		else write();
	}
	
	public void read(){
		int y = x;
	}
	
	public void write(){
		syncedWrite();
	}
	
	public void syncedWrite(){
		synchronized(x){
			x = 5;
		}
	}
	
	public static void main(String[] args){
		SyncBlockTest43 sbt = new SyncBlockTest43();
		sbt.readOrWrite(true);
		sbt.readOrWrite(false);
	}
}
