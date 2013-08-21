/** @file BMRStatbotData.java
 * 
 */

package bmrstatbot;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.sql.DataSource;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.jdbc.PostgreSQLBooleanPrefJDBCDataModel;

/** 
 * PostgreSQLBooleanPrefJDBCDataModel overridden to handle base36 ids 
 */
public class BMRStatbotDataModel extends PostgreSQLBooleanPrefJDBCDataModel {
	
	public BMRStatbotDataModel() throws TasteException {
	}

	public BMRStatbotDataModel(DataSource dataSource, String preferenceTable,
			String userIDColumn, String itemIDColumn, String timestampColumn) {
		super(dataSource, preferenceTable, userIDColumn, itemIDColumn, timestampColumn);
	}

	public BMRStatbotDataModel(DataSource dataSource) {
		super(dataSource);
	}

	public BMRStatbotDataModel(String dataSourceName) throws TasteException {
		super(dataSourceName);
	}

	/**
	 *  Get a string base36 identifier from the db and cast it to a long
	 */
	@Override
	protected long getLongColumn(ResultSet rs, int position) throws SQLException {		
		return Base36Util.base36ToLong(rs.getString(position));
	}
	
	/**
	 *  Encode a long as a base36 string and write to db
	 */
	@Override
	protected void setLongParameter(PreparedStatement stmt, int position, long value) throws SQLException {
		stmt.setString(position, Base36Util.longToBase36(value));
	
	}
	
}