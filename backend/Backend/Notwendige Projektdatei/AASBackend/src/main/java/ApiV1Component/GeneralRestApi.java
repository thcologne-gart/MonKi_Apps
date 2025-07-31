package ApiV1Component;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "")
public class GeneralRestApi {
	
	private static final String root = "/";

	public GeneralRestApi() {

	}
	
	@GetMapping(path = root)
	public String errorResponseGet() {
		return "MonKi-Root-errorResponseGet";
	}
	
	@PostMapping(path = root)
	public String errorResponsePost() {
		return "MonKi-Root-errorResponsePost";
	}
	
	@PutMapping(path = root)
	public String errorResponsePut() {
		return "MonKi-Root-errorResponsePut";
	}
	
	@DeleteMapping(path = root)
	public String errorResponseDelete() {
		return "MonKi-Root-errorResponseDelete";
	}
}