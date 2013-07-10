public class SyncBlockTest36 {
	Integer[] arr = {1,2,3,4,5,6,7};
	public static void main(String[] args){
		SyncBlockTest36 sbt = new SyncBlockTest36();
		synchronized(sbt.arr){
			sbt.arr[0] = 2;
		}
	}

}
