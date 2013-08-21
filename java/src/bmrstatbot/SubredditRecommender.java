package bmrstatbot;

import java.util.List;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.jdbc.ReloadFromJDBCDataModel;
import org.apache.mahout.cf.taste.impl.recommender.CachingRecommender;
import org.apache.mahout.cf.taste.impl.recommender.GenericBooleanPrefItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.LogLikelihoodSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;

import org.postgresql.ds.PGPoolingDataSource;

import bmrstatbot.Config;

/**
 *  Recommends new subreddit subscriptions to Reddit users
 */
public class SubredditRecommender {
	
	private CachingRecommender recommender;
	
	/**
	 * Create a subreddit recommender with cached item similarties
	 * 
	 * @throws TasteException
	 */
	public SubredditRecommender() throws TasteException{
		PGPoolingDataSource source = getDataSource();
		
		DataModel model = new ReloadFromJDBCDataModel(new BMRStatbotDataModel(source,
				"public.view_user_pref",
				"id",
				"subreddit",
				null));
		
		GenericBooleanPrefItemBasedRecommender genericRecommender =
				new GenericBooleanPrefItemBasedRecommender(
						model, new LogLikelihoodSimilarity(model));
		
		recommender = new CachingRecommender(genericRecommender);
	}
	
	/**
	 * Get the DataSource for the bmrstatbot database
	 * 
	 * @return
	 */
	private PGPoolingDataSource getDataSource() {
		
		Config cfg = Config.getInstance();
		
		PGPoolingDataSource source = new PGPoolingDataSource();
		source.setServerName(cfg.getDbAddress());
		source.setPortNumber(cfg.getDbPort());
		source.setDatabaseName(cfg.getDbName());
		source.setUser(cfg.getDbUsername());
		source.setPassword(cfg.getDbPassword());
		
		return source;
	}
	
	/**
	 * Gets recommendations for a given user
	 * 
	 * @param id The base36 id of the user
	 * @param number Maximum number of recommends to get
	 * @return A list of recommendations
	 * @throws TasteException 
	 */
	public List<RecommendedItem> getRecommendsFor(String id, int number) throws TasteException{
		return recommender.recommend(Base36Util.base36ToLong(id), number);
	}
	
	public void refreshRecommender(){
		recommender.refresh(null);
	}
}
