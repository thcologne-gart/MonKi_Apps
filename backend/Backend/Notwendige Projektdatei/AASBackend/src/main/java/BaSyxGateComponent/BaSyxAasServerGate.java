package BaSyxGateComponent;

import java.util.ArrayList;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

public class BaSyxAasServerGate extends BaSyxGate {
	
	public BaSyxAasServerGate() { 
		
	}
	
	public void writeAASToAASServer(String aasServeraddress, JsonObject aas) {
		String aasIdentifier = getAASIdentifier(aas).replaceAll(Slash, EncodedSlash);
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier; 
		httpPutCommand(urlStr, aas.toString());
	}
	
	public void writeSubmodelToAASServer(String aasServeraddress, JsonObject submodel, String aasIdentifier) {
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS + SLASH + getSubmodelIdShort(submodel);  
		httpPutCommand(urlStr, submodel.toString());
	}
	
	public JsonArray getSubmodelsArray(String aasServeraddress, String aasIdentifier) {
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS ; 
		return gson.fromJson(httpGetCommand(urlStr), JsonArray.class);  
	}
	
	public JsonObject getSubmodel(String aasServeraddress, String aasId, String smIdShort) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasId + SLASH + AAS + SLASH + SUBMODELS + SLASH + smIdShort + SLASH + SUBMODEL;
		String response = httpGetCommand(urlStr);
		return gson.fromJson(response, JsonObject.class);
	}
	
	public JsonObject getAasByIdentifier(String aasServeraddress, String identifier) {
		identifier = identifier.replaceAll(Slash, EncodedSlash);
		String getCommandStr = aasServeraddress + SLASH + SHELLS + SLASH +  identifier + SLASH + AAS;
		return gson.fromJson(httpGetCommand(getCommandStr), JsonObject.class); 
	}
	
	public JsonObject getSubmodelElement(String aasServeraddress, String aasIdentifier, String submodelIdShort, ArrayList<String> submodelElementIdShorts) {
		String str = ""; 
		for (String submodelElement : submodelElementIdShorts) {
			str = str + submodelElement +SLASH; 
		}
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String url =  aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS + SLASH + submodelIdShort + SLASH + SUBMODEL + SLASH + SUBMODELELEMENTS + SLASH + str; 
		return gson.fromJson(httpGetCommand(url), JsonObject.class); 
	}

	public String getSubmodelElementValue(String aasServeraddress, String aasIdentifier, String submodelIdShort, ArrayList<String> submodelElementIdShorts) {
		String str = ""; 
		for (String submodelElement : submodelElementIdShorts) {
			str = str + submodelElement +SLASH; 
		}
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String url =  aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS + SLASH + submodelIdShort + SLASH + SUBMODEL + SLASH + SUBMODELELEMENTS + SLASH + str + SLASH + VALUE; 
		return httpGetCommand(url); 
	}
	
	public void deleteAasByIdentifier(String aasServeraddress, String aasIdentifier) {
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String url =  aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier;
		System.out.println(url);
		httpDeleteCommand(url);
	}
	
	public void editSubmodelElementValue(String aasServeraddress, String aasIdentifier, String submodelIdShort, ArrayList<String> submodelElementIdShorts, String value) {
		String str = ""; 
		for (String submodelElement : submodelElementIdShorts) {
			str = str + submodelElement + SLASH; 
		}
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String url =  aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS + SLASH + submodelIdShort + SLASH + SUBMODEL + SLASH + SUBMODELELEMENTS + SLASH + str + VALUE;
		httpPutCommand(url, value);
	}
		
	//TODO das sollte man in die Registry auslagern wenn sich bei dieser die semanticIds automatisch updaten
	public String getSubmodelSemanticId(String aasServeraddress, String aasIdentifier, String submodelIdShort) {
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String url =  aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS + SLASH + submodelIdShort + SLASH + SUBMODEL;
		String smStr = httpGetCommand(url);
		JsonObject sm = gson.fromJson(smStr, JsonObject.class);
		return sm.get(SEMANTICID).getAsJsonObject().get(KEYS).getAsJsonArray().get(0).getAsJsonObject().get(VALUE).getAsString(); 
	}
	
	public void putSubmodelElementInSubmodel(String aasServeraddress, String aasId,String smIdShort, JsonObject smEle) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String smEleIdShort = smEle.get(IDSHORT).getAsString(); 
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasId + SLASH + AAS + SLASH + SUBMODELS + SLASH + smIdShort + SLASH + SUBMODEL + SLASH + SUBMODELELEMENTS + SLASH + smEleIdShort;  
		httpPutCommand(urlStr, smEle.toString()); 
	}
	
	public void putSubmodelElementInSubmodelByPath(String aasServeraddress, String aasId,String smIdShort, ArrayList<String> seShortIdPath, JsonObject smEle) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String smEleIdShort = "";
		for (String seShortId : seShortIdPath) {
			smEleIdShort = smEleIdShort + Slash + seShortId;
		}
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasId + SLASH + AAS + SLASH + SUBMODELS + SLASH + smIdShort + SLASH + SUBMODEL + SLASH + SUBMODELELEMENTS + smEleIdShort;  
		httpPutCommand(urlStr, smEle.toString()); 
	}
	
	private String getAASIdentifier(JsonObject aas) {
		return aas.get(IDENTIFICATION).getAsJsonObject().get(ID).getAsString(); 
	}
	
	private String getSubmodelIdShort(JsonObject sm) {
		return sm.get(IDSHORT).getAsString(); 
	}
	
	public void deleteSubmodel(String aasServeraddress, String aasIdentifier, String submodelIdShort) {
		aasIdentifier = aasIdentifier.replaceAll(Slash, EncodedSlash);
		String url =  aasServeraddress + SLASH + SHELLS + SLASH + aasIdentifier + SLASH + AAS + SLASH + SUBMODELS + SLASH + submodelIdShort;
		httpDeleteCommand(url);
	}
	
	public JsonObject getSubmodelElementValues(String aasServeraddress, String aasId, String smIdShort) {
		aasId = aasId.replaceAll(Slash, EncodedSlash);
		String urlStr = aasServeraddress + SLASH + SHELLS + SLASH + aasId + SLASH + AAS + SLASH + SUBMODELS + SLASH + smIdShort + SLASH + SUBMODEL + SLASH + "values";
		String response = httpGetCommand(urlStr);
		return gson.fromJson(response, JsonObject.class);
	}
}