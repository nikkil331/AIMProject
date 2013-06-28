public class SyncBlockTest19 {
	private String s = "";
	public static void main(String[] args){
		SyncBlockTest19 sbt = new SyncBlockTest19();
		synchronized(sbt.s){
			sbt.s = "written";
		}
	}
}
