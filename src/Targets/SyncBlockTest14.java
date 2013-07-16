public class SyncBlockTest14 {
	Integer x = 0;
	public synchronized void read(){
		int y = x;
	}
	public synchronized void write(){
		x = 2;
	}
	public synchronized void neither(){
		int y = 5;
	}
	public static void main(String[] args){
		SyncBlockTest14 sbt = new SyncBlockTest14();
		for(int i = 0; i < 10; i++){
			sbt.read();
			sbt.write();
			sbt.neither();
		}
	}
}
