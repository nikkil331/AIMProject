
public class SyncBlockTest28 {
	public static Object x = new Object();
	public static synchronized void readX(){
		synchronized(x){
			Object o = x;
		}
	}
	public static synchronized void writeX(){
		synchronized(x){
			x = new Object();}
	}
	public static void main(String[] args){
		SyncBlockTest28 sbt = new SyncBlockTest28();
		sbt.readX();
		sbt.writeX();
	}
}
