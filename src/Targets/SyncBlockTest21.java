
public class SyncBlockTest21 {
	Integer x = 0;
	
	public Integer getX(){
		return x;
	}
	
	public void setX(Integer y){
		x = y;
	}
	
	public static void main(String[] args){
		SyncBlockTest21 sbt = new SyncBlockTest21();
		synchronized(sbt){
			sbt.getX();
		}
		synchronized(sbt){
			sbt.setX(2);
		}
	}
}
