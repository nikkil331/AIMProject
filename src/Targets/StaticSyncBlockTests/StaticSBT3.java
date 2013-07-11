package StaticSyncBlockTests;

public class StaticSBT3 {
	static int numRuns = 10;
	int x;
	public static void main(String[] args){
		StaticSBT3 sbt = new StaticSBT3();
		for(int i=0; i < numRuns; i++){
			synchronized(sbt){
				synchronized(sbt){
					int y = sbt.x;
				}
			}
		}
	}
}
