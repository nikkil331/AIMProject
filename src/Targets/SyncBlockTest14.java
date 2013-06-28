public class SyncBlockTest14 {
	String x = "";
	public synchronized void read(){
		String y = x;
	}
	public synchronized void write(){
		x = "written";
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
