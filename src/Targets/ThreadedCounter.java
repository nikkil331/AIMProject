import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.*;
/*
 * uses multithreading to find the sum of integers
 * up to a given number
 */
public class ThreadedCounter {
	private static int numThreads = 5;
	
	public static void main(String[] args) throws InterruptedException, ExecutionException{
		long startTime = System.currentTimeMillis();
		int num = Integer.parseInt(args[0]);
		if(num < numThreads){
			numThreads = 1;
		}
		ExecutorService executor = Executors.newFixedThreadPool(numThreads);
		List<Future<Integer>> threads = new ArrayList<Future<Integer>>();
		for(int i = 0; i < num; i += num/numThreads + 1){
			Callable<Integer> thread = new Counter(i, Math.min(i + num/numThreads, num));
			Future<Integer> answer = executor.submit(thread);
			threads.add(answer);
		}
		
		Integer sum = 0;
		
		for(Future<Integer> thread : threads){
			sum +=  thread.get();
		}
		
		System.out.println("Runtime = " + (System.currentTimeMillis() - startTime));
		System.out.println(sum);
		executor.shutdown();
	}
}
