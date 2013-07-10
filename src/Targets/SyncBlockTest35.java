public class SyncBlockTest35 {
	Integer[] arr = {1,2,3,4,5,6,7};
	public static void main(String[] args){
		SyncBlockTest35 sbt = new SyncBlockTest35();
		synchronized(sbt.arr[0]){
			sbt.arr[0] = 2;
		}
	}
}
