public class SyncBlockTest9 {
	private class One{
		int x;
	}
	
	private class Two{
		int x;
	}
	
	public static void main(String[] args){
		SyncBlockTest9 sbt = new SyncBlockTest9();
		One one = sbt.new One();
		Two two = sbt.new Two();
		
		synchronized(one){
			int a = one.x;
			synchronized(two){
				one.x = 5;
				int b = two.x;
			}
		}
	}

}
