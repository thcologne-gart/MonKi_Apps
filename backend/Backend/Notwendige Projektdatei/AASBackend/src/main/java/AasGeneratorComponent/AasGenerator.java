package AasGeneratorComponent;

import com.google.gson.JsonObject;

import I40RepoComponent.AasTemplateRepoConnector;
import IdentifierGeneratorComponent.IdentifierGenerator;

import com.google.gson.JsonArray;

public class AasGenerator {
	
	private JsonObject aasInstance; 
	
	private IdentifierGenerator idGenerator = new IdentifierGenerator();
	
	private AasTemplateRepoConnector aasTemplateHandler; 
	
	private static final String IDENTIFICATION = "identification"; 
	private static final String ID = "id";
	private static final String IDTYPE = "idType";
	private static final String IRI = "IRI";
	private static final String IDSHORT = "idShort";
	private static final String DERIVEDFROM = "derivedFrom";
	private static final String TYPE = "type";
	private static final String ASSETADMINISTRATIONSHELL = "AssetAdministrationShell";
	private static final String LOCAL = "local";
	private static final String VALUE = "value";
	private static final String KEYS = "keys";
	
	public AasGenerator(String idShort,String derivedFrom) {
		this.aasTemplateHandler = new AasTemplateRepoConnector();
		this.aasInstance = aasTemplateHandler.getAasTemplate(); 
		setId(); 
		setIdShort(idShort); 
		setDerivedFrom(derivedFrom); 
	}
	
	private void setId() {
		String aasIdentifier = idGenerator.getIdentifierForAas();
		this.aasInstance.get(IDENTIFICATION).getAsJsonObject().addProperty(ID, aasIdentifier);
		this.aasInstance.get(IDENTIFICATION).getAsJsonObject().addProperty(IDTYPE, IRI);
	}
	
	private void setIdShort(String idShort) {
		this.aasInstance.addProperty(IDSHORT, idShort);
	}
	
	private void setDerivedFrom(String derivedFrom) {
		JsonObject keyObject = new JsonObject(); 
		keyObject.addProperty(TYPE, ASSETADMINISTRATIONSHELL);
		keyObject.addProperty(LOCAL, false);
		keyObject.addProperty(VALUE, derivedFrom);
		keyObject.addProperty(IDTYPE, IRI);
		JsonArray keysArray = new JsonArray(); 
		keysArray.add(keyObject);
		JsonObject keysObject = new JsonObject();
		keysObject.add(KEYS, keysArray);
		this.aasInstance.add(DERIVEDFROM, keysObject);
	}
	
	public JsonObject getAasInstance() {
		return aasInstance;
	}
	
	public String getAasIdentifier() {
		return aasInstance.get(IDENTIFICATION).getAsJsonObject().get(ID).getAsString();
	}
}