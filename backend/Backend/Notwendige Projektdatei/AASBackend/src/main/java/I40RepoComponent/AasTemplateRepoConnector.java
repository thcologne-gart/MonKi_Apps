package I40RepoComponent;

import com.google.gson.JsonObject;

public class AasTemplateRepoConnector extends RepoConnector {
	
	private static final String filename = "AasTemplate.json"; 
	
	public AasTemplateRepoConnector() {
		// TODO Auto-generated constructor stub
	}

	public JsonObject getAasTemplate() {
		return getJsonObjectFromRessource(filename);
	}
}
