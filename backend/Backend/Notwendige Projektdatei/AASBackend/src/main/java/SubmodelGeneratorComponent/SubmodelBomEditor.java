package SubmodelGeneratorComponent;

import java.util.ArrayList;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;

public class SubmodelBomEditor extends SubmodelEditor{
	
	//SubmodelTerms
	private static final String ARCHETYPE = "ArcheType";
	private static final String ENTRYNODE = "EntryNode";
	private static final String ENTITYTYPE = "entityType";
	private static final String HASPART = "HasPart";
	private static final String ISPARTOF = "IsPartOf";
	
	//APITerms
	private static final String ENTITYAASIDENTIFIER = "EntitiyAasIdentifier";
	
	public SubmodelBomEditor() {
		// TODO Auto-generated constructor stub
	}
	
	public ArrayList<JsonObject> createBomFromTemplate(JsonObject smTemp, JsonObject values) {
		ArrayList<JsonObject> returnList = new ArrayList<>(); 
		for(JsonElement ele: smTemp.get(SUBMODELELEMENTS).getAsJsonArray()){
			JsonObject obj = ele.getAsJsonObject(); 
			String tempIdShort = obj.get(IDSHORT).getAsString();
			if (tempIdShort.contains(ARCHETYPE)) {
				returnList.add(createArcheType(obj,values));
			}
			if (tempIdShort.contains(ENTRYNODE)) {
				returnList.add(createEntryNode(obj,values));
			}
		}
		return returnList; 
	}
	
	private JsonObject createArcheType(JsonObject temp, JsonObject values) {
		return editProperty(temp, values.get(ARCHETYPE).getAsString());
	}

	private JsonObject createEntryNode(JsonObject temp, JsonObject values) {
		temp.addProperty(ENTITYTYPE, values.get(ENTITYTYPE).getAsString());
		temp.addProperty(KIND, INSTANCE);
		temp.add(ASSET, createKeysObject(values.get(ENTITYAASIDENTIFIER).getAsString()));
		JsonArray hasParts = values.get(HASPART).getAsJsonArray(); 
		JsonArray isPartOf = values.get(ISPARTOF).getAsJsonArray(); 
		String entityAasId = values.get(ENTITYAASIDENTIFIER).getAsString();
		ArrayList<JsonObject> statementList = new ArrayList<>(); 
		for (int i = 0; i < hasParts.size(); i++) {
			String partsAasId = hasParts.get(i).getAsString();
			statementList.add(createHasPartRelationShipElement(temp,entityAasId,partsAasId));
		}
		for (int i = 0; i < isPartOf.size(); i++) {
			String partOfAasId = isPartOf.get(i).getAsString();
			statementList.add(createIsPartOfRelationShipElement(temp,entityAasId,partOfAasId));
		}
		JsonArray newStatements = new JsonArray(); 
		for (JsonElement ele : statementList) {
			JsonObject obj = ele.getAsJsonObject(); 
			newStatements.add(obj);
		}
		temp.add(STATEMENTS, newStatements);
		return temp; 
	}
	
	private JsonObject createRelationShipElement(JsonObject temp,String entityAasId, String partsAasId, String idShort) {
		JsonObject relationShipObj = new JsonObject(); 
		for (int i = 0; i < temp.get(STATEMENTS).getAsJsonArray().size(); i++) {
			JsonObject obj =  temp.get(STATEMENTS).getAsJsonArray().get(i).getAsJsonObject();
			if (obj.get(IDSHORT).getAsString().contains(idShort)) {
				relationShipObj = obj;
				break; 
			}
		}
		relationShipObj.addProperty(KIND, INSTANCE);
		relationShipObj.add(FIRST, createKeysObject(entityAasId));
		relationShipObj.add(SECOND, createKeysObject(partsAasId));
		return relationShipObj; 
	}
	
	private JsonObject createHasPartRelationShipElement(JsonObject temp,String entityAasId, String partsAasId) {
		return createRelationShipElement(temp, entityAasId, partsAasId, HASPART); 
	}
	
	private JsonObject createIsPartOfRelationShipElement(JsonObject temp,String entityAasId, String partsAasId) {
		return createRelationShipElement(temp, entityAasId, partsAasId, ISPARTOF); 
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