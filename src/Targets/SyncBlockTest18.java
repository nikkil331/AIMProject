
public class SyncBlockTest18 {
	Test x = new Test();
	public class Test{}
	public static void main(String[] args){
		SyncBlockTest18 sbt = new SyncBlockTest18();
		synchronized(sbt.x){
			sbt.x = sbt.new Test();
		}
	}
}
