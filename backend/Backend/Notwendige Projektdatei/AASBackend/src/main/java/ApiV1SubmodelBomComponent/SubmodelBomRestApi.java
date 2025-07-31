package ApiV1SubmodelBomComponent;

import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

@RestController
@RequestMapping(path = "GART/api/v1/Submodel/BOM")
public class SubmodelBomRestApi implements ISubmodelBomRestApi{
	
	private static final String initialPost_POST = "/initialPost";
	private static final String addHasPartElement_POST = "/addHasPartElement";
	private static final String addIsPartOfElement_POST = "/addIsPartOfElement";
	private static final String getParents_POST = "/getParents";
	private static final String getChilds_POST = "/getChilds";
	
	private SubmodelBomServices serviceController = new SubmodelBomServices(); 
	
	private static final String AASSERVERADDRESS = "aasServerAddress";
	private static final String AASIDENTIFIER = "aasIdentifier";
	private static final String SUBMODELIDSHORT = "submodelIdShort";
	private static final String BOMVALUES = "BomValues"; 
		
	public SubmodelBomRestApi() {
		
	}
	
	@PostMapping(initialPost_POST)
	public void initialPost(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		JsonObject values = body.get(BOMVALUES).getAsJsonObject(); 
		serviceController.initialPost(aasServerAddress,aasIdentifier,smIdShort,values);
	}

	@PostMapping(addHasPartElement_POST)
	public void addHasPartElement(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		JsonObject values = body.get(BOMVALUES).getAsJsonObject(); 
		serviceController.addPartElement(aasServerAddress,aasIdentifier,smIdShort,values,"HasPart");
	}
	
	@PostMapping(addIsPartOfElement_POST)
	public void addIsPartOfElement(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		JsonObject values = body.get(BOMVALUES).getAsJsonObject(); 
		serviceController.addPartElement(aasServerAddress,aasIdentifier,smIdShort,values,"IsPartOf");
	}
	
	@PostMapping(value = getParents_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> getParents(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		JsonArray arr = serviceController.getParents(aasServerAddress, aasIdentifier, smIdShort); 
		return serviceController.convertJsonArrayToList(arr);
	}
	
	@PostMapping(value = getChilds_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> getChilds(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String smIdShort = body.get(SUBMODELIDSHORT).getAsString();
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString();
		JsonArray arr = serviceController.getChilds(aasServerAddress, aasIdentifier, smIdShort);
		return serviceController.convertJsonArrayToList(arr);
	}
}