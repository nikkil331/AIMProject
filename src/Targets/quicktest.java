
public class quicktest {
	int[] arr = {1,2,3,4,5};
	public static void main(String[] args){
		quicktest qt = new quicktest();
		synchronized(qt){
			qt.arr[0]++;
		}
	}
}
