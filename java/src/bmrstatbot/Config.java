package bmrstatbot;

import java.io.File;
import java.io.IOException;

import org.ini4j.InvalidFileFormatException;
import org.ini4j.Wini;

/**
 *  Configuration object for the Java side of bmrstatbot
 */
public class Config {
	private static final Config INSTANCE;
	
    static {
        try {
            INSTANCE = new Config("config/config.ini");
        } catch (Exception e) {
            throw new ExceptionInInitializerError(e);
        }
    }
    
	private String dbUsername;
	private String dbPassword;
	private String dbAddress;
	private int dbPort;
	private String dbName;
	
	
	private Config(String path) throws InvalidFileFormatException, IOException{
		 Wini ini = new Wini(new File(path));
		 
		 dbUsername = ini.get("database", "user");
		 dbPassword = ini.get("database", "password");
		 String addressAndPort = ini.get("database", "address");
		 
		 // This is minimal validation, so junk will still result in bad things
		 if(addressAndPort.contains(":")){
			 String[] addressPortSplit = addressAndPort.split(":");
			 dbAddress = addressPortSplit[0];
			 dbPort = Integer.parseInt(addressPortSplit[1]);
		 }
		 else{
			 dbAddress = addressAndPort;
			 dbPort = 0; // 0 causes PGSQL to assume default 
		 }
		  
		 dbName = ini.get("database", "name");
	}
	
	
	public String getDbUsername() {
		return dbUsername;
	}

	public String getDbPassword() {
		return dbPassword;
	}

	public String getDbAddress() {
		return dbAddress;
	}

	public String getDbName() {
		return dbName;
	}
	
	public int getDbPort() {
		return dbPort;
	}

	
	public static Config getInstance(){
		return INSTANCE;
	}


}
