package bmrstatbot;

/**
 * Helper functions for translating base36 strings to longs and vice versa
 * 
 * This is useful because the db stores keys as base36 strings (the way Reddit
 * supplies them), yet Mahout wants longs
 */
public final class Base36Util {
	
	private Base36Util(){}
	
	/**
	 * Convert a string in base36 to corresponding long
	 * 
	 * @param in A string containing a base36 id
	 * @return long corresponding to the in string
	 */
	public static long base36ToLong(String in){
		return Long.parseLong(in, 36);
	}
	
	/**
	 * Convert a long to a lowercase base36 string
	 * 
	 * @param in long to be converted
	 * @return Lowercase id corresponding to the in long
	 */
	
	public static String longToBase36(long in){
		return Long.toString(in, 36).toLowerCase();
	}
}
