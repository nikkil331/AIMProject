
public class SyncBlockTest28 {
	public static Integer x = 0;
	public static synchronized void readX(){
		int y = x;
	}
	public static synchronized void writeX(){
		x++;
	}
	public static void main(String[] args){
		SyncBlockTest28 sbt = new SyncBlockTest28();
		sbt.readX();
		sbt.writeX();
	}
}
