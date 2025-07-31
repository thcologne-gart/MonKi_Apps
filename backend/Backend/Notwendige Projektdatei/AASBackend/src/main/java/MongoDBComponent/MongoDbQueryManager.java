package MongoDBComponent;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.bson.Document;
import org.bson.conversions.Bson;

import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;

public class MongoDbQueryManager {
	
	private static final String TS = "ts";
	private static final String IDSHORTSUBMODELELEMENTPATH = "shortIdPath";
	private static final String VALUE = "value";
	private static final String IDSHORTSUBMODEL = "idShortSubmodel";
	
	public MongoDbQueryManager() {
		
	}

	public void insertTimeSeriesValue(MongoCollection<Document> collection, String submodelName,  String shortIdPath,Date date, Object value){
		Document doc = new Document();
		doc.append(TS, date);
		doc.append(IDSHORTSUBMODELELEMENTPATH, shortIdPath);
		doc.append(IDSHORTSUBMODEL, submodelName);
		doc.append(VALUE, value);
		collection.insertOne(doc);		
	}
	
	public void insertManyTimeSeriesValues(MongoCollection<Document> collection, String submodelName,  String[] shortIdPaths,Date[] dates, Object[] values){
		List<Document> docs = new ArrayList<Document>();
		Document doc;
		for (int i = 0 ; i<values.length; i++) {
			doc = new Document();
			doc.append(TS, dates[i]);
			doc.append(IDSHORTSUBMODELELEMENTPATH, shortIdPaths[i]);
			doc.append(IDSHORTSUBMODEL, submodelName);
			doc.append(VALUE, values[i]);
			docs.add(doc);
		}
		collection.insertMany(docs);
	}
	
	public FindIterable<Document> getManyTimeSeriesValues(MongoCollection<Document> collection, String idShortSubmodel, String smePath, Date tsBegin, Date tsEnd) {
		Bson submodelPathFilter = Filters.eq(IDSHORTSUBMODEL, idShortSubmodel);
		Bson smePathFilter = Filters.eq(IDSHORTSUBMODELELEMENTPATH, smePath);
		Bson tsBeginFilter = Filters.gte(TS, tsBegin);
		Bson tsEndFilter = Filters.lte(TS, tsEnd);
		Bson allFilters = Filters.and(submodelPathFilter,smePathFilter,tsBeginFilter,tsEndFilter);
		return collection.find(allFilters);
	}
	
	public void deleteCompleteTimeSeries(MongoCollection<Document> collection, String idShortSubmodel, String smePath) {
		Bson submodelFilter = Filters.eq(IDSHORTSUBMODEL, idShortSubmodel);
		Bson semPathFilter = Filters.eq(IDSHORTSUBMODELELEMENTPATH, smePath);
		Bson allFilter = Filters.and(submodelFilter,semPathFilter);
		collection.deleteMany(allFilter);
	}	
	
	//TODO
	public void deletePartlyTimeSeries(MongoCollection<Document> collection, String idShortSubmodel, String smePath, Date tsBegin, Date tsEnd) {
		Bson submodelPathFilter = Filters.eq(IDSHORTSUBMODEL, idShortSubmodel);
		Bson smePathFilter = Filters.eq(IDSHORTSUBMODELELEMENTPATH, smePath);
		Bson tsBeginFilter = Filters.gte(TS, tsBegin);
		Bson tsEndFilter = Filters.lte(TS, tsEnd);
		Bson allFilters = Filters.and(submodelPathFilter,smePathFilter,tsBeginFilter,tsEndFilter);
		collection.deleteMany(allFilters);
	}
}