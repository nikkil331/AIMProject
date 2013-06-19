import java.util.concurrent.Callable;


public class Counter implements Callable<Integer> {
	private final int from;
	private final int to;
	
	public Counter(int from, int to){
		this.from = from;
		this.to = to;
	}
	
	@Override
	public Integer call() throws Exception {
		int sum = 0;
		for(int i = from; i <= to; i++){
			sum+=i;
		}
		return sum;
	}



}
