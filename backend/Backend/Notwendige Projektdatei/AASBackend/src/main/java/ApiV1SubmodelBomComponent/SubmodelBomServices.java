package ApiV1SubmodelBomComponent;

import java.util.ArrayList;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import ApiV1Component.abstractServices;

public class SubmodelBomServices extends abstractServices{

	//BOM Submodel Terms
	private static final String ENTRYNODE = "EntryNode"; 
	private static final String FIRST = "first";
	private static final String HASPART = "HasPart";
	private static final String ISPARTOF = "IsPartOf"; 
	private static final String SECOND = "second"; 
	private static final String STATEMENTS = "statements"; 

	//AAS Terms
	private static final String ASSETADMINISTRATIONSHELL = "AssetAdministrationShell";
	private static final String IDTYPE = "idType";
	private static final String IDSHORT = "idShort"; 
	private static final String INDEX = "index";
	private static final String INSTANCE = "Instance";
	private static final String IRDI = "IRDI";
	private static final String KEYS = "keys"; 
	private static final String KIND = "kind";
	private static final String LOCAL = "local";
	private static final String SUBMODELELEMENTS = "submodelElements";
	private static final String TYPE = "type";
	private static final String VALUE = "value";

	//BOM API Terms
	private static final String ENTITYAASIDENTIFIER = "EntitiyAasIdentifier";	

	private static final String bomSemanticId = "https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel";

	public SubmodelBomServices() {
		// TODO Auto-generated constructor stub
	}

	public void initialPost(String aasServerAddress, String aasId,String smIdShort, JsonObject values) {
		ArrayList<JsonObject> list = smFactory.createBOMInitialSubmodelElements(values);
		for(JsonObject obj :list) {
			aasServerGate.putSubmodelElementInSubmodel(aasServerAddress, aasId, smIdShort, obj);
		}
	}

	public JsonArray getParents(String aasServerAddress, String aasId,String smIdShort) {
		return getRelationInfo(aasServerAddress, aasId, smIdShort, ISPARTOF);
	}
	
	public JsonArray getChilds(String aasServerAddress, String aasId,String smIdShort) {
		return getRelationInfo(aasServerAddress, aasId, smIdShort, HASPART);
	}

	private JsonArray getRelationInfo(String aasServerAddress, String aasId,String smIdShort, String relationInfo) {
		JsonArray returnArray = new JsonArray(); 
		ArrayList<String> smEleList = new ArrayList<>(); 
		smEleList.add(ENTRYNODE);
		JsonObject entryNode = aasServerGate.getSubmodelElement(aasServerAddress, aasId, smIdShort, smEleList);
		JsonArray statements = entryNode.get(STATEMENTS).getAsJsonArray(); 
		for (JsonElement ele : statements) {
			JsonObject obj = ele.getAsJsonObject(); 
			if (obj.has(IDSHORT) && obj.get(IDSHORT).getAsString().contains(relationInfo)) {
				String childId = obj.get(SECOND).getAsJsonObject().get(KEYS).getAsJsonArray().get(0).getAsJsonObject().get(VALUE).getAsString();
				returnArray.add(childId);
			}
		}
		return returnArray; 
	}

	public void addPartElement(String aasServerAddress, String aasId,String smIdShort, JsonObject values, String partElement) {
		JsonObject submodel = aasServerGate.getSubmodel(aasServerAddress,aasId,smIdShort); 
		JsonArray smElementsTemplate = smFactory.getSubmodelElementsTemplate(bomSemanticId);
		JsonArray statementsTemplate = null;
		JsonObject hasPartObj = null; 
		for (JsonElement jsonElement : smElementsTemplate) {
			JsonObject obj = jsonElement.getAsJsonObject(); 
			if (obj.get(IDSHORT).getAsString().contains(ENTRYNODE)) {
				statementsTemplate = obj.get(STATEMENTS).getAsJsonArray(); 
			}
		}
		for (JsonElement jsonElement : statementsTemplate) {
			JsonObject obj = jsonElement.getAsJsonObject(); 
			if (obj.get(IDSHORT).getAsString().contains(partElement)) {
				hasPartObj = editHasPartTemplate(obj,values,partElement);
			}
		}
		for (int i = 0; i < submodel.get(SUBMODELELEMENTS).getAsJsonArray().size(); i++) {
			String idShort = submodel.get(SUBMODELELEMENTS).getAsJsonArray().get(i).getAsJsonObject().get(IDSHORT).getAsString();
			if (idShort.contains(ENTRYNODE)) {
				submodel.get(SUBMODELELEMENTS).getAsJsonArray().get(i).getAsJsonObject().get(STATEMENTS).getAsJsonArray().add(hasPartObj);
			}
		}
		aasServerGate.writeSubmodelToAASServer(aasServerAddress, submodel, aasId);
	}

	private JsonObject editHasPartTemplate(JsonObject obj, JsonObject values, String partElement ) {
		obj.addProperty(KIND, INSTANCE);
		obj.add(FIRST, createKeysObject(values.get(ENTITYAASIDENTIFIER).getAsString()));
		obj.add(SECOND, createKeysObject(values.get(partElement).getAsString()));
		return obj; 
	}

	private JsonObject createKeysObject(String aasIdentifier) {
		JsonObject retObject = new JsonObject(); 
		JsonArray keys = new JsonArray(); 
		JsonObject aasObject = new JsonObject(); 
		aasObject.addProperty(TYPE, ASSETADMINISTRATIONSHELL);
		aasObject.addProperty(LOCAL, false);
		aasObject.addProperty(VALUE, aasIdentifier);
		aasObject.addProperty(INDEX, 0);
		aasObject.addProperty(IDTYPE, IRDI);
		keys.add(aasObject);
		retObject.add(KEYS, keys);
		return retObject; 
	}
}