
public class SyncBlockTest30 {
	public static void main(String[] args){
		Object o = new Object();
		synchronized(o){
			o.toString();
			o = new Object();
		}
	}
}
