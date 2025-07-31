package I40RepoComponent;

import com.google.gson.JsonObject;

public class SubmodelTemplatesRepoConnector extends RepoConnector{

	private static final String pathPart1 = "SubmodelTemplates";
	private static final String thkoelnSnippet = "th-koeln.de/gart";
	private static final String idtaSnippet = "admin-shell.io/idta"; 
	private static final String zveiSnippet = "admin-shell.io/zvei"; 


	public SubmodelTemplatesRepoConnector() {
		
	}

	public JsonObject getSubmodelTemplate(String submodelSemanticId) {
		if (submodelSemanticId.contains(thkoelnSnippet)) {
			return getThKoelnSubmodel(submodelSemanticId);
		}
		else if (submodelSemanticId.contains(idtaSnippet)) {
			return getIDTASubmodel(submodelSemanticId);
		}
		else if (submodelSemanticId.contains(zveiSnippet)) {
			return getZVEISubmodel(submodelSemanticId);
		}
		else {
			System.out.println("error: " +  submodelSemanticId + " ist nicht im Repo");
		}
		return null; 
	}
	
	private JsonObject getThKoelnSubmodel(String submodelSemanticId) {
		String[] splittedStr1 = submodelSemanticId.split("https://th-koeln.de/gart/vocabulary/");
		String[] splittedStr2 = splittedStr1[1].split(String.valueOf(SLASH));
		String orgaName = "th-koeln";
		return getJsonObjectFromRessource(getPath(orgaName, splittedStr2)); 
	}
	
	private JsonObject getIDTASubmodel(String submodelSemanticId) {
		String[] splittedStr1 = submodelSemanticId.split("https://admin-shell.io/idta/");
		String[] splittedStr2 = splittedStr1[1].split(String.valueOf(SLASH));
		String orgaName = "idta";
		return getJsonObjectFromRessource(getPath(orgaName, splittedStr2));
	}
	
	private JsonObject getZVEISubmodel(String submodelSemanticId) {
		String[] splittedStr1 = submodelSemanticId.split("https://admin-shell.io/zvei/");
		String[] splittedStr2 = splittedStr1[1].split(String.valueOf(SLASH));
		String orgaName = "zvei";
		return getJsonObjectFromRessource(getPath(orgaName, splittedStr2)); 
	}
	
	private String getPath(String orgaName, String[] splittedStr) {
		String submodelName = splittedStr[0];
		String version = splittedStr[1];
		String revision = splittedStr[2];
		String endPath = pathPart1 + 
				SLASH + 
				orgaName + 
				SLASH + 
				submodelName + 
				SLASH + 
				version + 
				SLASH + 
				revision + 
				SLASH + 
				submodelName + ".json"; 
		return endPath; 
	}
}