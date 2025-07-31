package MongoDBComponent;

import java.util.ArrayList;

import org.bson.Document;

import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.CreateCollectionOptions;
import com.mongodb.client.model.TimeSeriesOptions;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;

public class MongoDbConnector {

	private static final String TS = "ts";
	private static final String IDSHORTSUBMODELELEMENTPATH = "shortIdPath";
	private static final String IDSHORTSUBMODEL = "idShortSubmodel";

	private static MongoClient mongoClient;

	public MongoDbConnector(String connectionString) {
		mongoClient = MongoClients.create(connectionString);
	}

	public MongoDatabase getDatabase(String databaseName) {
		return mongoClient.getDatabase(databaseName);

	}

	public MongoCollection<Document> getCollection(String databaseName, String collectionName) {
		return mongoClient.getDatabase(databaseName).getCollection(collectionName);
	}

	public void createCollection(String databaseName, String collectionName) {
		MongoDatabase database = getDatabase(databaseName);
		boolean collectionExists = database.listCollectionNames().into(new ArrayList<>()).contains(collectionName);
		if (!collectionExists) {
			database.createCollection(collectionName);
		} else {
			System.out.println("Sammlung bereits vorhanden: " + collectionName);
		}
	}
	
	public void createTimeSeriesDatabaseCollection(String databaseName, String collectionName) {
		MongoDatabase database = getDatabase(databaseName);
		boolean collectionExists = database.listCollectionNames().into(new ArrayList<>()).contains(collectionName);
		if (!collectionExists) {
			TimeSeriesOptions tsOptions = new TimeSeriesOptions(TS);
			tsOptions.metaField(IDSHORTSUBMODEL);
			tsOptions.metaField(IDSHORTSUBMODELELEMENTPATH);
			CreateCollectionOptions collOptions = new CreateCollectionOptions().timeSeriesOptions(tsOptions);
			database.createCollection(collectionName, collOptions);
		}
	}
	
	public MongoCollection<Document> getMongoCollection(String databaseName, String collectionName) {
		MongoDatabase database = getDatabase(databaseName);
		MongoCollection<Document> collection = database.getCollection(collectionName);
		return collection; 
	}

	public void close() {
		mongoClient.close();
	}    
}