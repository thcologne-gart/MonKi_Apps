package SubmodelGeneratorComponent;

import java.util.ArrayList;
import java.util.Set;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

public class SubmodelEditor {
	
	protected static final String ASSET = "asset";
	protected static final String ASSETADMINISTRATIONSHELL = "AssetAdministrationShell";
	protected static final String IDSHORT = "idShort";
	protected static final String INSTANCE = "Instance";
	protected static final String KIND = "kind";
	protected static final String NAME = "name";
	
	protected static final String SUBMODELELEMENTS = "submodelElements";
	protected static final String SUBMODELELEMENTCOLLECTION = "SubmodelElementCollection";
	protected static final String VALUE = "value";
	protected static final String VALUETYPE = "valueType";
	
	protected static final String DATAOBJECTTYPE = "dataObjectType";
	protected static final String MODELTYPE = "modelType";
	protected static final String MULTILANGUAGEPROPERTY = "MultiLanguageProperty";
	protected static final String PROPERTY = "Property";
	protected static final String STATEMENTS = "statements";
	protected static final String STRING_lowercase = "string";
	protected static final String STRING_firstcaseUp = "String";
	protected static final String FIRST = "first";
	protected static final String SECOND = "second";
	protected static final String TYPE = "type";
	protected static final String LOCAL = "local";
	protected static final String INDEX = "index";
	protected static final String IDTYPE = "idType";
	protected static final String IRDI = "IRDI";
	protected static final String KEYS = "keys";

	public SubmodelEditor() {

	}

	public ArrayList<JsonObject> editSmElementsBySmElementValues(JsonObject smTemp, JsonObject smElementValues) {
		ArrayList<JsonObject> returnList = new ArrayList<>(); 
		Set<String> keySet = smElementValues.keySet();
		for(JsonElement ele: smTemp.get(SUBMODELELEMENTS).getAsJsonArray()){
			JsonObject obj = ele.getAsJsonObject(); 
			String tempIdShort = obj.get(IDSHORT).getAsString();
			if (keySet.contains(tempIdShort)) {
				returnList.add(editValues(obj,smElementValues));
			}
		}
		return returnList; 
	}
	
	//TODO aufräumen
	protected JsonObject editValues(JsonObject obj, JsonObject smElementValues) {
		String modelType = obj.get(MODELTYPE).getAsJsonObject().get(NAME).getAsString();
		String tempIdShort = obj.get(IDSHORT).getAsString();
		if (modelType.equals(PROPERTY)) {
			String value = smElementValues.get(tempIdShort).getAsString(); 
			return editProperty(obj,value); 
		}
		else if (modelType.equals(MULTILANGUAGEPROPERTY)) {
			JsonArray value = smElementValues.get(tempIdShort).getAsJsonArray(); 
			return editMultiLanguageProperty(obj,value);   
		}
		else if (modelType.equals(SUBMODELELEMENTCOLLECTION)) {
			JsonArray sec = obj.get(VALUE).getAsJsonArray(); 
			JsonArray returnArray = new JsonArray(); 
			Set<String> keySet = smElementValues.get(tempIdShort).getAsJsonObject().keySet();
			for (JsonElement ele : sec) {
				JsonObject secObj = ele.getAsJsonObject();
				String tempIdShort2 = secObj.get(IDSHORT).getAsString();
				if (keySet.contains(tempIdShort2)) {
					returnArray.add(editValues(secObj,smElementValues.get(tempIdShort).getAsJsonObject()));
					obj.add(VALUE, returnArray);
					obj.addProperty(KIND, INSTANCE);
				}
			}
			return obj;  
		}
		else {
			System.out.println("Implementierung fehlt für: " + modelType + " in " + this.getClass().toString());
			return null; 
		}
	}
	
	protected JsonObject editProperty(JsonObject obj, String value) {
		obj.addProperty(VALUE, value);
		obj.addProperty(KIND, INSTANCE);
		obj = replaceValueTypeIfWrong(obj);
		return obj; 
	}
	
	protected JsonObject editMultiLanguageProperty(JsonObject obj, JsonArray value) {
		obj.add(VALUE, value);
		obj.addProperty(KIND, INSTANCE);
		obj = replaceValueTypeIfWrong(obj);
		return obj; 
	}
	
	protected JsonObject replaceValueTypeIfWrong(JsonObject obj) {
		if (obj.has(VALUETYPE) && obj.get(VALUETYPE).getClass() == JsonObject.class) {
			String valueType = obj.get(VALUETYPE).getAsJsonObject().get(DATAOBJECTTYPE).getAsJsonObject().get(NAME).getAsString();
			if (valueType.contains(STRING_firstcaseUp)) {
				valueType = STRING_lowercase; 
			}
			if (valueType.length() > 0) {
				obj.addProperty(VALUETYPE, valueType);
			}
			else{
				obj.addProperty(VALUETYPE, STRING_lowercase);
			}
		}
		return obj; 
	}
}