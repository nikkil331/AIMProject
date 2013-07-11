package StaticSyncBlockTests;

public class StaticSBT5 {
	static int numThreads = 10;
	int x;
	
	public synchronized int read(){
		return x;
	}
	
	public static void main(String[] args){
		StaticSBT5 sbt1 = new StaticSBT5();
		StaticSBT5 sbt2 = new StaticSBT5();
		for(int i = 0; i < numThreads; i++){
			sbt1.read();
			sbt2.read();
		}
	}
}
