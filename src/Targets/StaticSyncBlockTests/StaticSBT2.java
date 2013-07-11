package StaticSyncBlockTests;

public class StaticSBT2 {
	static int numRuns = 10;
	int x;
	public static void main(String[] args){
		StaticSBT2 sbt = new StaticSBT2();
		for(int i = 0; i < numRuns; i++){
			synchronized(sbt){
				int y = sbt.x;
				synchronized(sbt){}
			}
		}
	}
}
