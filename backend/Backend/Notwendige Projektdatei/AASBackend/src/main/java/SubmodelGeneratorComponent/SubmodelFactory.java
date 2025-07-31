package SubmodelGeneratorComponent;

import java.util.ArrayList;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import IdentifierGeneratorComponent.IdentifierGenerator;

public class SubmodelFactory {
	
	private static final String bomSemanticId = "https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel";
	
	//AAS Terms
	private static final String SUBMODELENDPOINTS = "submodelElements";
	
	private SubmodelGenerator generator = new SubmodelGenerator(); 
	private SubmodelEditor editor = new SubmodelEditor();
	private SubmodelBomEditor bomEditor = new SubmodelBomEditor(); 
	private TimeSeriesSubmodel tsSubmodel = new TimeSeriesSubmodel(); 
	
	public SubmodelFactory() {
		// TODO Auto-generated constructor stub
	}
	
	public JsonObject loadInitialSubmodel(String semanticId) {
		return generator.getSubmodelInstance(semanticId);
	}
	
	public ArrayList<JsonObject> createSubmodelElementsByValues(String semanticId, JsonObject smElementValues) {
		JsonObject smTemp = generator.getSubmodelTemplate(semanticId);
		return editor.editSmElementsBySmElementValues(smTemp, smElementValues);
	}
	
	public ArrayList<JsonObject> createBOMInitialSubmodelElements(JsonObject values){
		JsonObject smTemp = generator.getSubmodelTemplate(bomSemanticId);
		return bomEditor.createBomFromTemplate(smTemp, values);
	}
	
	public JsonObject loadTimeSeriesSubmodel() {
		Gson gsonObj = new Gson();
		IdentifierGenerator idGenerator = new IdentifierGenerator(); 
		String jsonSubmodelStr = gsonObj.toJson(tsSubmodel.getEmptySubmodel(idGenerator.getIdentifierForSubmodel("TimeSeries")));
		JsonObject smObj = new Gson().fromJson(jsonSubmodelStr, JsonObject.class);
		return smObj;
	}
	
	public JsonArray getSubmodelElementsTemplate(String semanticId) {
		JsonArray smElementsTemplate = generator.getSubmodelTemplate(semanticId).get(SUBMODELENDPOINTS).getAsJsonArray();
		return smElementsTemplate; 
	}
}