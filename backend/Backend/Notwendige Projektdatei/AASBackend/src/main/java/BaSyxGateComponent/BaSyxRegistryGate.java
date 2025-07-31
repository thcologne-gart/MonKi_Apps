package BaSyxGateComponent;

import java.util.ArrayList;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class BaSyxRegistryGate extends BaSyxGate{
	
//	private static final String REGISTRY = "registry";
//	private static final String apiTerm = "api" + SLASH + "v1" + SLASH + "registry"; 

	public BaSyxRegistryGate() {

	}
	
	public JsonObject getAasDescriptor(String registryAddress,String aasId) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String urlStr = registryAddress + SLASH + aasId;
		return gson.fromJson(httpGetCommand(urlStr), JsonObject.class); 
	}
	
	public JsonArray getAasSubmodelDescriptors(String registryAddress,String aasId) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String urlStr = registryAddress + SLASH + aasId + SLASH + SUBMODELS;
		return gson.fromJson(httpGetCommand(urlStr), JsonArray.class); 
	}
	
	public void writeSubmodelInRegistry(String registryAddress,String aasAddress, String aasId, JsonObject submodel ) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String submodelId = submodel.get("identification").getAsJsonObject().get("id").getAsString();
		submodelId = submodelId.replaceAll(Slash, EncodedSlash);
		String submodelIdShort = submodel.get("idShort").getAsString();
		String urlStr = registryAddress + SLASH 
				+ aasId					+ SLASH 
				+ SUBMODELS 			+ SLASH 
				+ submodelId;
		JsonArray endpointsArray = new JsonArray() ;
		JsonObject endpointObject = new JsonObject(); 
		String endPointAddress = aasAddress + SLASH 
				+ "aasServer" 				+ SLASH
				+ "shells"					+ SLASH
				+ aasId 					+ SLASH
				+ "aas"						+ SLASH
				+ SUBMODELS					+ SLASH
				+ submodelIdShort			+ SLASH
				+ SUBMODEL;
		endpointObject.addProperty("address", endPointAddress);
		endpointObject.addProperty("type", "http");
		endpointsArray.add(endpointObject);
		JsonObject registrySmObject = new JsonObject();
		registrySmObject.addProperty("idShort",submodelIdShort );
		registrySmObject.add("identification", submodel.get("identification").getAsJsonObject());
		registrySmObject.add("semanticId", submodel.get("semanticId").getAsJsonObject());
		registrySmObject.add("endpoints", endpointsArray);
		httpPutCommand(urlStr, registrySmObject.toString());
	}

	public JsonArray getAllAasIdentifier(String registryAddress) {
		JsonArray jsonArray = new JsonArray(); 
		for (JsonElement ele : gson.fromJson(httpGetCommand(registryAddress), JsonArray.class)) {
			JsonObject obj = ele.getAsJsonObject();
			String identifier = obj.get(IDENTIFICATION).getAsJsonObject().get(ID).getAsString();
			jsonArray.add(identifier); 
		}
		return jsonArray; 
	}
	
	public ArrayList<String> getSubmodelEnpointListBySemanticId(String registryAddress, String semanticIdTarget){
		ArrayList<String> list = new ArrayList<String>(); 
		JsonArray aasEntries = gson.fromJson(httpGetCommand(registryAddress), JsonArray.class);
		for (JsonElement ele : aasEntries) {
			JsonObject aas = ele.getAsJsonObject();
			JsonArray smEntries = aas.get(SUBMODELS).getAsJsonArray();
			for(JsonElement ele2:smEntries) {
				JsonObject smEntry = ele2.getAsJsonObject();
				JsonArray semanticIdEntries = smEntry.get(SEMANTICID).getAsJsonObject().get(KEYS).getAsJsonArray();
				for(JsonElement ele3:semanticIdEntries) {
					JsonObject semanticIdEntry = ele3.getAsJsonObject();
					String semanticId = semanticIdEntry.getAsJsonObject().get(VALUE).getAsString();
					if (semanticId.contains(semanticIdTarget)) {
						String smEndpoint = smEntry.get(ENDPOINTS).getAsJsonArray().get(0).getAsJsonObject().get(ADDRESS).getAsString();
						list.add(smEndpoint);
					}
				}
			}
		}
		return list; 
	}
}