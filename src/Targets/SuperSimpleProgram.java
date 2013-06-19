public class SuperSimpleProgram {
	private static int x;
	public static void main(String[] args){
	    x = 0;
     	    x = simpleMethod(x);
		
	}
	public static int simpleMethod(int y){
		while(y < 5){
			y++;
		}
		return y;
	}
	
}
