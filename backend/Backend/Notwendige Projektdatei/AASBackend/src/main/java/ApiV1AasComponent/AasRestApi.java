package ApiV1AasComponent;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

@RestController
@RequestMapping(path = "GART/api/v1/AAS")
public class AasRestApi implements IAasRestApi{
	
	private static final String helloServer_GET = "/helloServer";
	
	private static final String REGISTRYADDRESS = "registryAddress";
	private static final String AASSERVERADDRESS = "aasServerAddress";
	private static final String AASIDENTIFIER = "aasIdentifier";
	private static final String SEMANTICIDAASTYPE = "semanticIdAasType";
	private static final String IDSHORT = "idShort"; 
	private static final String AASOBJECT = "aasObject";
	private static final String LOCALHOST = "localhost";
	
	private AasServices serviceController = new AasServices(); 

	public AasRestApi() {
		
	}
	
	@CrossOrigin(origins = "*", methods = RequestMethod.GET)
	@GetMapping(path = helloServer_GET, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> helloServer(){
		ArrayList<String> list = new ArrayList<String>();
		list.add("hello server");
		return list;
	}
	
	@CrossOrigin(origins = "*", methods = RequestMethod.OPTIONS)
	@PostMapping(path = getAllAasIdentifier_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> getAllAasIdentifier(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String registryAddress = body.get(REGISTRYADDRESS).getAsString();
		JsonArray array = serviceController.getAllAasIdentifier(registryAddress); 
		return serviceController.convertJsonArrayToList(array);
	}
	
	@PostMapping(path = getAasByIdentifier_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public Map<?, ?> getAasByIdentifier(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String identifier = body.get(AASIDENTIFIER).getAsString(); 
		JsonObject aasObj = serviceController.getAasByIdentifier(aasServerAddress,identifier);
		return serviceController.convertJsonObjectToMap(aasObj);
	}
	
	@PostMapping(path = getAllAasIdentifierByAasType_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> getallAasIdentifierByAasType(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String registryAddress = body.get(REGISTRYADDRESS).getAsString();
		String semanticIdAasType = body.get(SEMANTICIDAASTYPE).getAsString();
		JsonArray jsonArray = serviceController.getallAasIdentifierByAasType(aasServerAddress,registryAddress,semanticIdAasType); 
		return serviceController.convertJsonArrayToList(jsonArray);
	}
	
	@PostMapping(deleteAasByIdentifier_POST)
	public void deleteAasByIdentifier(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String aasIdentifier = body.get(AASIDENTIFIER).getAsString(); 
		serviceController.deleteAasByIdentifier(aasServerAddress,aasIdentifier); 
	}
	
	@PostMapping(createAasByAasType_POST)
	public String createAasByAasType(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String registryAddress = body.get(REGISTRYADDRESS).getAsString(); 
		String semanticIdAasType = body.get(SEMANTICIDAASTYPE).getAsString();
		String idShort = body.get(IDSHORT).getAsString();
		return serviceController.createAasByAasType(registryAddress,aasServerAddress, idShort, semanticIdAasType,LOCALHOST);
	}
	
	@PostMapping(path = getAasIdShortByIdentifier_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<?> getAasIdShortByIdentifier(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString(); 
		String identifier = body.get(AASIDENTIFIER).getAsString(); 
		JsonArray jsonArray = serviceController.getAasIdShortByIdentifier(aasServerAddress,identifier); 
		return  serviceController.convertJsonArrayToList(jsonArray);
	}
	
	@PostMapping(addAas_POST)
	public String addAas(@RequestBody String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		JsonObject aas = body.get(AASOBJECT).getAsJsonObject();
		return serviceController.addAas(aasServerAddress, aas);
	}

	@PostMapping(getAasSemanticIdByIdentifier_POST)
	public List<String> getAasSemanticIdByIdentifier(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		JsonArray returnArray = serviceController.getAasSemanticIdByIdentifier(aasServerAddress, aasId);
		return serviceController.convertJsonArrayToList(returnArray); 
	}

	
}