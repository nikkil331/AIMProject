package StaticSyncBlockTests;

public class StaticSBT6 {
	int x = 0;
	public synchronized void read(int times){
		if(times == 0) return;
		int y = x;
		read(times - 1);
	}
	public static void main(String[] args){
		StaticSBT6 sbt = new StaticSBT6();
		sbt.read(10);
	}
}
