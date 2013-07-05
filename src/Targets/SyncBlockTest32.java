import java.util.List;
import java.util.ArrayList;

public class SyncBlockTest32 {
	List<String> list = new ArrayList<String>();
	static Object o = new Object();
	public static void main(String[] args){
		SyncBlockTest32 sbt = new SyncBlockTest32();
		String s = "hello";
		s = "goodbye";
		sbt.list.add(s);
		/*synchronized(sbt){
			s = "hello again";
		}*/
		synchronized(sbt.o){}
	}
}
