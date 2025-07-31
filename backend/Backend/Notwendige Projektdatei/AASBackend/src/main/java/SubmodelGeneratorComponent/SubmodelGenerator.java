package SubmodelGeneratorComponent;

import com.google.gson.JsonObject;

import I40RepoComponent.SubmodelTemplatesRepoConnector;
import IdentifierGeneratorComponent.IdentifierGenerator;

import com.google.gson.JsonArray;

public class SubmodelGenerator {
	
	//AAS Terms
	private static final String ID = "id";
	private static final String IDENTIFICATION = "identification";
	private static final String IDSHORT = "idShort";
	private static final String INSTANCE = "Instance";
	private static final String KIND = "kind";
	private static final String SUBMODELELEMENTS = "submodelElements";
	
	private JsonObject submodel;
	
	private SubmodelTemplatesRepoConnector submodelHandler = new SubmodelTemplatesRepoConnector(); 
	
	private IdentifierGenerator idGenerator = new IdentifierGenerator(); 
	
	public SubmodelGenerator() {
		
	}
	
	private void loadSubmodelTemplate(String semanticId) {
		submodel = submodelHandler.getSubmodelTemplate(semanticId);
	}
	
	private void addIdentifier() {
		String id = idGenerator.getIdentifierForSubmodel(submodel.get(IDSHORT).getAsString()); 
		submodel.get(IDENTIFICATION).getAsJsonObject().addProperty(ID, id);
	}

	private void editSubmodelKindStatus() {
		submodel.addProperty(KIND, INSTANCE);
	}
	
	private void removeSubmodelElements() {
		JsonArray emptyArray = new JsonArray(); 
		submodel.add(SUBMODELELEMENTS, emptyArray);
	}
	
	public JsonObject getSubmodelInstance(String semanticId) {
		loadSubmodelTemplate(semanticId);
		addIdentifier(); 
		editSubmodelKindStatus();
		removeSubmodelElements();
		return submodel ;
	}
	
	public JsonObject getSubmodelTemplate(String semanticId) {
		loadSubmodelTemplate(semanticId);
		return submodel ;
	}	
}