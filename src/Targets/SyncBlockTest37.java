public class SyncBlockTest37 {
	public static void main(String[] args){
		for(int i = 0; i < args.length && args[i].charAt(0) == '-'; i++){
			if(args[i].equals("-f")) { 
				System.out.println("It was -f");
				String x = args[++i];
			}
			else if (args[i].equals("-t")){
				System.out.println("It was -t");
			}
			else System.out.println("It wasn't -f or -t");
		}
	}
}
