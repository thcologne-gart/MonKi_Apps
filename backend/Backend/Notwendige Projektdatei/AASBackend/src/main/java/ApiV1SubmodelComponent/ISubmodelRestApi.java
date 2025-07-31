package ApiV1SubmodelComponent;

import java.util.Map;

import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

public interface ISubmodelRestApi {
	
	static final String getSubmodelElementByPath_POST = "/getSubmodelElementByPath";
	static final String getSubmodelElementValue_POST = "/getSubmodelElementValue";
	static final String getSubmodel_GET = "/getSubmodel";
	static final String downloadSubmodelElementValue_POST = "/getSubmodelElementValue/download";
	static final String editSubmodelElementValue_POST = "/editSubmodelElementValue";
	static final String addSubmodelElements_POST = "/addSubmodelElements";
	static final String addSubmodelToAas_POST = "/addSubmodelToAas";
	static final String deleteSubmodel_Post = "/deleteSubmodel";
	static final String editSubmodelElementValues_Post = "/editSubmodelElementValues";
	static final String getSubmodelElementValues_POST = "/getSubmodelElementValues";
	static final String addCompleteSubmodelToAas_POST = "/addCompleteSubmodelToAas";
	static final String addCompleteSubmodelElementsToAas_POST = "/addCompleteSubmodelElementsToAas";
	
	@PostMapping(path = getSubmodelElementByPath_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public Map<?, ?> getSubmodelElementByPath(@RequestBody String jsonObjectStr);
	
	@PostMapping(path = getSubmodelElementValue_POST)
	public Map<?, ?> getSubmodelElementValue(@RequestBody String jsonObjectStr);
	
	@PostMapping(path = getSubmodel_GET, produces = MediaType.APPLICATION_JSON_VALUE)
	public Map<?, ?> getSubmodel(@RequestBody String jsonObjectStr);
	
	@PostMapping(path = downloadSubmodelElementValue_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<byte[]> downloadSubmodelElementValue(@RequestBody String jsonObjectStr);
	
	@PostMapping(editSubmodelElementValue_POST)
	public void editSubmodelElementValue(@RequestBody String jsonObjectStr);
	
	@PostMapping(addSubmodelElements_POST)
	public void addSubmodelElements(@RequestBody String jsonObjectStr);
	
	@PostMapping(addSubmodelToAas_POST)
	public void addSubmodelToAas(@RequestBody String jsonObjectStr);
	
	@PostMapping(addCompleteSubmodelToAas_POST)
	public void addCompleteSubmodelToAas(@RequestBody String jsonObjectStr);
	
	@PostMapping(deleteSubmodel_Post)
	public void deleteSubmodel(@RequestBody String jsonObjectStr);
	
	@PostMapping(editSubmodelElementValues_Post)
	public void editSubmodelElementValues(@RequestBody String jsonObjectStr);
	
	@PostMapping(getSubmodelElementValues_POST)
	public Map<?, ?> getSubmodelElementValues(@RequestBody String jsonObjectStr);

	@PostMapping(addCompleteSubmodelElementsToAas_POST)
	public void addCompleteSubmodelElementsToAas(@RequestBody String jsonObjectStr);
	
}