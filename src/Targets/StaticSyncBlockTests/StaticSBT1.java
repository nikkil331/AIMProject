package StaticSyncBlockTests;

public class StaticSBT1 {
	static int numRuns = 10;
	int x = 0;
	public static void main(String[] args){
		StaticSBT1 sbt = new StaticSBT1();
		for(int i = 0; i < numRuns; i++){
			synchronized(sbt){
				int y = sbt.x;
			}
		}
	}
}
