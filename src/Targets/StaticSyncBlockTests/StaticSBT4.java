package StaticSyncBlockTests;

public class StaticSBT4 {
	static int numThreads = 10;
	Integer x = new Integer(0);
	public static void main(String[] args){
		StaticSBT4 sbt = new StaticSBT4();
		for(int i = 0; i < numThreads; i++){
			synchronized(sbt){
				synchronized(sbt.x){
					sbt.x = 5;
				}
			}
		}
	}
}
