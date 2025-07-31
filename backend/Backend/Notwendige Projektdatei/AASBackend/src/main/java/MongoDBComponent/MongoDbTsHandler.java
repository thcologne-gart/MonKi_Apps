package MongoDBComponent;

import java.util.Date;

import org.bson.Document;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.mongodb.client.FindIterable;

public class MongoDbTsHandler {

	private static final String VALUE = "value";
	private static final String TS = "ts";
	private static final String DATE = "date";
	private static final String TIMESERIES = "TimeSeries-";

	private MongoDbQueryManager queryManager = new MongoDbQueryManager();
	private MongoDbConnector connector;

	public MongoDbTsHandler(MongoDbConnector connector) {
		this.connector = connector;
	}

	public void createTimeSeries( String userSpecificId, String aasId) {
		String databasename = getMongoDatabaseName(userSpecificId);
		this.connector.createTimeSeriesDatabaseCollection(databasename, aasId);
	}

	public void insertEntry(String userId, String aasId, String shortIdSubmodel, String smePath, Date date, Object value) {
		String databasename = getMongoDatabaseName(userId);
		queryManager.insertTimeSeriesValue(
				this.connector.getCollection(databasename, aasId), 
				shortIdSubmodel,
				smePath, 
				date,
				value);
	}

	public void insertManyEntries(String userId, String aasId, String shortIdSubmodel, String[] smePaths, Date[] dates, Object[] values) {
		String databasename = getMongoDatabaseName(userId);
		queryManager.insertManyTimeSeriesValues(
				this.connector.getCollection(databasename, aasId), 
				shortIdSubmodel, 
				smePaths,
				dates, 
				values);
	}

	public JsonArray getTimeSeries(String userId, String aasId, String shortIdSubmodel, String smePath, Date tsBegin, Date tsEnd) {
		String databasename = getMongoDatabaseName(userId);
		FindIterable<Document> list =  queryManager.getManyTimeSeriesValues(
				this.connector.getCollection(databasename, aasId),
				shortIdSubmodel, 
				smePath,
				tsBegin,
				tsEnd);
		JsonArray returnArray = new JsonArray();
		for (Document document : list) {
			JsonObject obj = new JsonObject(); 
			obj.addProperty(DATE, document.getDate(TS).getTime());
			Object value = getValueFromMonoDb(document);
			if(value.getClass() == java.lang.Integer.class || value.getClass() == java.lang.Double.class )
			{
				obj.addProperty(VALUE, (Number) value);
			}
			else if(value.getClass() == java.lang.Boolean.class) {
				obj.addProperty(VALUE, (Boolean) value);
			}
			returnArray.add(obj);
		} 
		return returnArray;
	}

	public void updateTimeSeriesElement(String aasId, String smePath, Date timestamp, Object value) {
		/*
		 *TODO
		 */
	}

	public void deleteTimeSeries(String aasId, String smePath) {
		/*
		 * TODO
		 */
	}

	public void deleteTimeSeriesEntry(String aasId, String smePath, Date timestamp) {
		/*
		 * TODO
		 */
	}

	public void closeMongoConnection() {
		this.connector.close();
	}

	private String getMongoDatabaseName(String userSpecificId) {
		return TIMESERIES+userSpecificId; 
	}

	private Object getValueFromMonoDb(Document document) {
		if (document.get(VALUE).getClass() == java.lang.Integer.class) {
			return document.getInteger(VALUE);
		}
		else if(document.get(VALUE).getClass() == java.lang.Double.class) {
			return document.getDouble(VALUE);
		}
		else if(document.get(VALUE).getClass() == java.lang.Boolean.class) {
			return document.getBoolean(VALUE);
		}
		else {
			System.out.println("Mongo kann Datenformat nicht bearbeiten");
		}
		return null;
	}
}