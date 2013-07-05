public class SyncBlockTest33 {
	String s = "string";
	public void read(){
		String sprime = s;
	}
	public void write(){
		s = "string";
	}
	public void neither(){}
	public static void main(String[] args){
		for(int i = 0; i < 100; i++){
			SyncBlockTest33 sbt1 = new SyncBlockTest33();
			SyncBlockTest33 sbt2 = new SyncBlockTest33();
			SyncBlockTest33 sbt3 = new SyncBlockTest33();
			
			synchronized(sbt1.s){
				sbt1.read();
				synchronized(sbt2){
					sbt1.write();
					sbt2.neither();
					synchronized(sbt3){
						sbt2.read();
						sbt3.neither();
					}
				}
			}
		}
	}
}
