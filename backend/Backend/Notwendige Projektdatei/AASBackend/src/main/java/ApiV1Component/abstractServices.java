package ApiV1Component;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.reflect.TypeToken;

import BaSyxGateComponent.BaSyxAasServerGate;
import BaSyxGateComponent.BaSyxRegistryGate;
import I40RepoComponent.AasTypesRepoConnector;
import MongoDBComponent.MongoDbConnector;
import MongoDBComponent.MongoDbTsHandler;
import SubmodelGeneratorComponent.SubmodelFactory;

public abstract class abstractServices {

	protected BaSyxRegistryGate registryGate = new BaSyxRegistryGate(); 
	protected BaSyxAasServerGate aasServerGate = new BaSyxAasServerGate(); 
	protected Gson gson = new Gson();
	protected AasTypesRepoConnector reqHandlerRepo = new AasTypesRepoConnector();
	protected JsonObject repository = reqHandlerRepo.getAasRepository(); 
	protected SubmodelFactory smFactory = new SubmodelFactory();
	private static final String mongoDbPassword = "3rNSZmxIte1bTHeN"; 
	private static final String mongoDbConnectionString = "mongodb+srv://bkaemper:" + mongoDbPassword + "@cluster0.zgwztqy.mongodb.net/"; // Ihre MongoDB-Verbindungszeichenfolge hier
	private MongoDbConnector mongoDBConnector = new MongoDbConnector(mongoDbConnectionString);
	protected MongoDbTsHandler mongoHandler = new MongoDbTsHandler(mongoDBConnector); 

	public List<String> convertJsonArrayToList(JsonArray jsonArray) {
		List<String> list = new ArrayList<>();
		for (int i = 0; i < jsonArray.size(); i++) {
			String element = jsonArray.get(i).getAsString();
			list.add(element);
		}
		return list;
	}
	
	public Map<?, ?> convertJsonObjectToMap(JsonObject obj) {
		Type type = new TypeToken<Map<String, Object>>(){}.getType();
		Map<String, String> map = gson.fromJson(obj, type);
		return map;
	}
}