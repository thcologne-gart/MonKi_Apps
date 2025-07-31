package ApiV1SubmodelTsComponent;

import java.util.ArrayList;
import java.util.Date;

import org.eclipse.basyx.submodel.metamodel.map.qualifier.LangString;
import org.eclipse.basyx.submodel.metamodel.map.qualifier.LangStrings;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.SubmodelElementCollection;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import ApiV1Component.abstractServices;
import IdentifierGeneratorComponent.IdentifierGenerator;
import SubmodelGeneratorComponent.TimeSeriesSubmodel;

public class TimeSeriesServices extends abstractServices {
	
	private TimeSeriesSubmodel sm = new TimeSeriesSubmodel();
	
	public void createTimeSeriesSubmodel(String registryAddress, String aasServer, String userSpecificId, String aasId) {
		IdentifierGenerator idGenerator = new IdentifierGenerator(); 
		Gson gsonObj = new Gson();
		String jsonSubmodelStr = gsonObj.toJson(sm.getEmptySubmodel(idGenerator.getIdentifierForSubmodel("TimeSeries")));
		JsonObject smObj = new Gson().fromJson(jsonSubmodelStr, JsonObject.class);
		aasServerGate.writeSubmodelToAASServer(aasServer, smObj, aasId);
		registryGate.writeSubmodelInRegistry(registryAddress, aasServer, aasId, smObj);
		mongoHandler.createTimeSeries(userSpecificId, aasId);
	}
	
	public void createTimeSeries(String aasServer, String aasId, String submodelRef, String propertyRef, int samplingInterval, String tsName) {
		/*TODO
		 * - write to MonkiBridge
		 */
		LangStrings names = new LangStrings();
		names.add(new LangString("en", tsName));
		LangStrings descriptions = new LangStrings();
		long recordCount = 10; 
		String startTime = "";
		String endTime = "";
		String duration = "";
		long samplingRate = 10; 
		String state = ""; 
		String lastUpdate = "";
		String endpoint = ""; 
		String query = "";
		SubmodelElementCollection sec = sm.getSubmodelElementCollectionLinkedSegment(
				tsName, 
				names, 
				descriptions,
				recordCount,
				startTime, 
				endTime, 
				duration, 
				samplingInterval, 
				samplingRate, 
				state, 
				lastUpdate, 
				endpoint, 
				query);
		Gson gsonObj = new Gson();
		String jsonSubmodelStr = gsonObj.toJson(sec);
		JsonObject seObj = new Gson().fromJson(jsonSubmodelStr, JsonObject.class);
		ArrayList<String> list = new ArrayList<String>(); 
		list.add("Segments");
		list.add(tsName);
		aasServerGate.putSubmodelElementInSubmodelByPath(aasServer, aasId, "TimeSeries",list, seObj);
	}
	
	public JsonArray readTimeSeries(String userId,String aasId, String shortIdSubmodel, String smePath, long tsBegin, long tsEnd ) {
		Date startDate = fromUnixTimestamp(tsBegin);
		Date endDate = fromUnixTimestamp(tsEnd);
		return mongoHandler.getTimeSeries(userId, aasId, shortIdSubmodel, smePath, startDate, endDate);
	}
	
	public void updateTimeSeries() {
		
	}
	
	public void deleteTimeSeries() {
		
	}
	
	private Date fromUnixTimestamp(long unixTimestamp) {
		return new Date(unixTimestamp * 1000L); // Unix-Zeitstempel in Millisekunden umwandeln
	}
}