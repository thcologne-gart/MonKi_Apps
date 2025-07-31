package ApiV1SubmodelBomComponent;

import java.util.List;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

public interface ISubmodelBomRestApi {
	
	static final String initialPost_POST = "/initialPost";
	static final String addHasPartElement_POST = "/addHasPartElement";
	static final String addIsPartOfElement_POST = "/addIsPartOfElement";
	static final String getParents_POST = "/getParents";
	static final String getChilds_POST = "/getChilds";
	
	@PostMapping(initialPost_POST)
	public void initialPost(@RequestBody String jsonObjectStr);
	
	@PostMapping(addHasPartElement_POST)
	public void addHasPartElement(@RequestBody String jsonObjectStr);
	
	@PostMapping(addIsPartOfElement_POST)
	public void addIsPartOfElement(@RequestBody String jsonObjectStr);
	
	@PostMapping(value = getParents_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> getParents(@RequestBody String jsonObjectStr);
	
	@PostMapping(value = getChilds_POST, produces = MediaType.APPLICATION_JSON_VALUE)
	public List<String> getChilds(@RequestBody String jsonObjectStr);
	
	

}
