package I40RepoComponent;

import com.google.gson.JsonObject;

public class AasTypesRepoConnector extends RepoConnector {

	private static final String filename = "AasTypeRepository.json"; 
	
	
	public AasTypesRepoConnector() {
		// TODO Auto-generated constructor stub
	}

	public JsonObject getAasRepository() {
		return getJsonObjectFromRessource(filename);
	}
}
