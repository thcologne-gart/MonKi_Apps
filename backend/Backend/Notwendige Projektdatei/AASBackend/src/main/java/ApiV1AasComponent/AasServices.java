package ApiV1AasComponent;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import AasGeneratorComponent.AasGenerator;
import ApiV1Component.abstractServices;
import ApiV1SubmodelTsComponent.TimeSeriesServices;

public class AasServices extends abstractServices{

	private static final String Slash = "/";
	private static final String EncodedSlash = "%2F";
	private static final String DERIVEDFROM = "derivedFrom";
	private static final String KEYS = "keys";
	private static final String VALUE = "value";
	
	private static final String tsSemanticId = "https://admin-shell.io/idta/TimeSeries/1/1";

	public AasServices() {

	}

	public JsonArray getAllAasIdentifier(String registryAddress) {
		return registryGate.getAllAasIdentifier(registryAddress);
	}
	
	public JsonObject getAasByIdentifier(String aasServerAddress, String identifier) { 
		identifier = identifier.replaceAll(Slash, EncodedSlash);
		return aasServerGate.getAasByIdentifier(aasServerAddress, identifier);
	}
	
	public JsonArray getallAasIdentifierByAasType(String aasServerAddress,String registryAddress, String semanticIdAasType) {
	JsonArray aasIdArray = registryGate.getAllAasIdentifier(registryAddress);
	JsonArray returnArray = new JsonArray();
	for (JsonElement ele : aasIdArray) {
		String aasId = ele.getAsString(); 
		JsonObject obj = aasServerGate.getAasByIdentifier(aasServerAddress,aasId);
		String tempSemanticIdAasType = null; 
		if (obj.has(DERIVEDFROM)){
			tempSemanticIdAasType = obj.get(DERIVEDFROM).getAsJsonObject().get(KEYS).getAsJsonArray().get(0).getAsJsonObject().get(VALUE).getAsString();
		}
		if (tempSemanticIdAasType != null && tempSemanticIdAasType.contains(semanticIdAasType)) {
			returnArray.add(aasId);
		}
	}
	return returnArray;
}
	
	public void deleteAasByIdentifier(String aasServerAddress, String aasIdentifier) { 
		aasServerGate.deleteAasByIdentifier(aasServerAddress,aasIdentifier); 
	}

	public String createAasByAasType(String registryAddress, String aasServerAddress, String idShort, String semanticIdAasType, String userSpecificId) {
		AasGenerator aas = new AasGenerator(idShort,semanticIdAasType);
		aasServerGate.writeAASToAASServer(aasServerAddress,aas.getAasInstance());
		JsonArray submodelSemanticIds = repository.get(semanticIdAasType).getAsJsonArray();
		for (JsonElement jsonElement : submodelSemanticIds) {
			String submodelSemanticId = jsonElement.getAsString();
			if (submodelSemanticId.equals(tsSemanticId)) {
				TimeSeriesServices tsServices = new TimeSeriesServices(); 
				tsServices.createTimeSeriesSubmodel(registryAddress, aasServerAddress, userSpecificId, aas.getAasIdentifier());
			}
			else {
				JsonObject sm = smFactory.loadInitialSubmodel(submodelSemanticId);
				aasServerGate.writeSubmodelToAASServer(aasServerAddress, sm , aas.getAasIdentifier());
				registryGate.writeSubmodelInRegistry(registryAddress, aasServerAddress, aas.getAasIdentifier(), sm);
			}
			
		}
		return aas.getAasIdentifier(); 
	}
	
	public JsonArray getAasIdShortByIdentifier(String aasServerAddress, String identifier) { 
		String idShort = getAasByIdentifier(aasServerAddress, identifier).get("idShort").getAsString(); 
		JsonArray jsonArray = new JsonArray();
		jsonArray.add(idShort);
		return jsonArray;
	}
	
	public String addAas(String aasServerAddress, JsonObject aas) {
		aasServerGate.writeAASToAASServer(aasServerAddress, aas);
		return aas.get("identification").getAsJsonObject().get("id").getAsString();
	}
	
	public JsonArray getAasSemanticIdByIdentifier(String aasServerAddress, String aasId) {
		JsonArray returnArray = new JsonArray();
		JsonObject aasObj = aasServerGate.getAasByIdentifier(aasServerAddress, aasId);
		String semanticId = aasObj.get(DERIVEDFROM).getAsJsonObject().get(KEYS).getAsJsonArray().get(0).getAsJsonObject().get(VALUE).getAsString(); 
		returnArray.add(semanticId);
		return  returnArray;
	}
	
	
}