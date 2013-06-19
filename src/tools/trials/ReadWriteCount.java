import rr.state.ShadowVar;

public class ReadWriteCount implements ShadowVar{
		private Integer read = 0;
		private Integer write = 0;
			
		public int getRead(){
			return read;
		}
		
		public int getWrite(){
			return write;
		}
		public ReadWriteCount incRead(){
			read++;
			return this;
		}
		public ReadWriteCount incWrite(){
			write++;
			return this;
		}
	}