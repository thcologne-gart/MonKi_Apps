package I40RepoComponent;

import java.io.IOException;
import java.io.InputStream;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

public abstract class RepoConnector {

	protected static final String repoName = "GART-I4.0Repositorium";
	protected static final char SLASH = 47;

	public RepoConnector() {
		// TODO Auto-generated constructor stub
	}
	
	protected JsonObject getJsonObjectFromRessource(String endPath) {
		String path = repoName + SLASH + endPath;
		InputStream is = getFileAsIOStream(path);
		String fileContent = null;
		try {
			fileContent = new String( is.readAllBytes() );
		} catch (IOException e) {
			e.printStackTrace();
		}
		return convertStringToJson(fileContent);
	}
	
	private JsonObject convertStringToJson(String jsonString) {
		JsonObject jsonObject = new Gson().fromJson(jsonString, JsonObject.class);
		return jsonObject;
	}
	
	private InputStream getFileAsIOStream(final String fileName){
		InputStream ioStream = this.getClass()
				.getClassLoader()
				.getResourceAsStream(fileName);
		if (ioStream == null) {
			throw new IllegalArgumentException(fileName + " is not found");
		}
		return ioStream;
	}
}