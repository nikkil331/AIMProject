public class SyncBlockTest9 {
	One one = new One();
	Two two = new Two();
	private class One{
		int x;
	}
	
	private class Two{
		int x;
	}
	
	public static void main(String[] args){
		SyncBlockTest9 sbt = new SyncBlockTest9();
				
		synchronized(sbt.one){
			sbt.one.x = 5;
			synchronized(sbt.two){
				sbt.one = sbt.new One();
				sbt.two.x = 3;
			}
		}
	}

}
