package ApiV1SubmodelComponent;

import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

@RestController
@RequestMapping(path = "GART/api/v1/Submodel")
public class SubmodelRestApi implements ISubmodelRestApi{

	private static final String AASSERVERADDRESS = "aasServerAddress";
	private static final String REGISTRYADDRESS = "registryAddress";
	private static final String AASIDENTIFIER = "aasIdentifier";
	private static final String SUBMODELIDSHORT = "submodelIdShort";
	private static final String SUBMODELELEMENTIDSHORT = "submodelElementIdShort"; 
	private static final String VALUE = "value";
	private static final String SEMANTICIDSUBMODEL = "semanticIdSubmodel";
	private static final String SUBMODELELEMENTS = "submodelElements";
	private static final String SUBMODELElEMENTVALUES = "submodelElementsValue"; 
	private static final String SUBMODELELEMENTSTOEDIT = "submodelElementsToEdit"; 
	private static final String COMPLETESUBMODEL = "completeSubmodel";
	
	private SubmodelServices serviceController = new SubmodelServices(); 

	public SubmodelRestApi() {

	}

	@PostMapping(path = getSubmodelElementByPath_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public Map<?, ?> getSubmodelElementByPath(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		String submodelIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonArray submodelElementIdShorts = body.get(SUBMODELELEMENTIDSHORT).getAsJsonArray();
		JsonObject obj = serviceController.getSubmodelElementByPath(aasServerAddress,aasIdentifier, submodelIdShort, submodelElementIdShorts );
		return serviceController.convertJsonObjectToMap(obj);
	}

	@PostMapping(path = getSubmodelElementValue_POST)
	public Map<?, ?> getSubmodelElementValue(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		String submodelIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonArray submodelElementIdShorts = body.get(SUBMODELELEMENTIDSHORT).getAsJsonArray();
		JsonObject obj = serviceController.getSubmodelElementByPath(aasServerAddress,aasIdentifier, submodelIdShort, submodelElementIdShorts );
		return serviceController.convertJsonObjectToMap(obj);
	}

	@PostMapping(path = getSubmodel_GET, produces = MediaType.APPLICATION_JSON_VALUE)
	public Map<?, ?> getSubmodel(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonObject obj = serviceController.getSubmodel(aasServerAddress, aasId, smIdShort); 
		return serviceController.convertJsonObjectToMap(obj);
	}
	
	@PostMapping(path = downloadSubmodelElementValue_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<byte[]> downloadSubmodelElementValue(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		String submodelIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonArray submodelElementIdShorts = body.get(SUBMODELELEMENTIDSHORT).getAsJsonArray();
		return serviceController.downloadSubmodelElementValue(aasServerAddress,aasIdentifier, submodelIdShort, submodelElementIdShorts );
	}
	
	@PostMapping(editSubmodelElementValue_POST)
	public void editSubmodelElementValue(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonArray smElementIdShorts = body.get(SUBMODELELEMENTIDSHORT).getAsJsonArray();
		String value = body.get(VALUE).getAsString();
		serviceController.editSubmodelElementValue(aasServerAddress, aasId, smIdShort, smElementIdShorts, value); 
	}

	@PostMapping(addSubmodelElements_POST)
	public void addSubmodelElements(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		String smSemanticId = body.get(SEMANTICIDSUBMODEL).getAsString();
		JsonObject smElements = body.get(SUBMODELElEMENTVALUES).getAsJsonObject();
		serviceController.addSubmodelElements(aasServerAddress, aasId, smIdShort,smSemanticId, smElements); 
	}
	
	@PostMapping(addSubmodelToAas_POST)
	public void addSubmodelToAas(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String registryAddress = body.get(REGISTRYADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smSemanticId = body.get(SEMANTICIDSUBMODEL).getAsString();
		serviceController.addSubmodelToAas(registryAddress, aasServerAddress, aasId, smSemanticId); 
	}

	@PostMapping(deleteSubmodel_Post)
	public void deleteSubmodel(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		serviceController.deleteSubmodel(aasServerAddress, aasId, smIdShort); 
	}
	
	@PostMapping(editSubmodelElementValues_Post)
	public void editSubmodelElementValues(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonArray submodelElementsToEdit = body.get(SUBMODELELEMENTSTOEDIT).getAsJsonArray();
		serviceController.editSubmodelElementValues(aasServerAddress,aasId,smIdShort,submodelElementsToEdit); 
	}

	@PostMapping(getSubmodelElementValues_POST)
	public Map<?, ?> getSubmodelElementValues(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonObject obj = serviceController.getSubmodelElementValues(aasServerAddress,aasId,smIdShort);
		return serviceController.convertJsonObjectToMap(obj);
	}

	@PostMapping(addCompleteSubmodelToAas_POST)
	public void addCompleteSubmodelToAas(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String registryAddress = body.get(REGISTRYADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		JsonObject sm = body.get(COMPLETESUBMODEL).getAsJsonObject(); 
		serviceController.addCompleteSubmodelToAas(registryAddress, aasServerAddress, aasId, sm); 
	}

	@PostMapping(addCompleteSubmodelElementsToAas_POST)
	public void addCompleteSubmodelElementsToAas(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String registryAddress = body.get(REGISTRYADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		JsonArray submodelElements = body.get(SUBMODELELEMENTS).getAsJsonArray();
		serviceController.addCompleteSubmodelElements(registryAddress, aasServerAddress, aasId, smIdShort, submodelElements);
	}
}