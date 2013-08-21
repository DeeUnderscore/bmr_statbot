package bmrstatbot;

import org.apache.mahout.cf.taste.common.TasteException;

import py4j.GatewayServer;

/**
 * Provide a wrapper allowing Py4j to manipulate SubredditRecommender
 */
public class Py4jWrapper {

	private SubredditRecommender subRecommender;
	
	public Py4jWrapper() throws TasteException{
		subRecommender = new SubredditRecommender();
	}
	
	public SubredditRecommender getRecommender(){
		return subRecommender;
	}
	
	public static void main(String[] args) throws TasteException {
        GatewayServer gatewayServer = new GatewayServer(new Py4jWrapper());
        gatewayServer.start();
	}
}
