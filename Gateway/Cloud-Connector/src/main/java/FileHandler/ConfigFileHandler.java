package FileHandler;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class ConfigFileHandler {
	
	private static final String UTF_8 = "UTF-8";
	
	private JsonObject configObject; 
	
	public ConfigFileHandler(String filename) {
		setConfigObject(filename);
	}

	private void setConfigObject(String filename) {
		try {
			InputStream is = getClass().getClassLoader().getResourceAsStream(filename);
			InputStreamReader reader = new InputStreamReader(is, UTF_8);
			Gson gson = new Gson();
			configObject = gson.fromJson(reader, JsonObject.class);
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		}
	}
	
	public JsonObject getConfigJsonObject() {
		return configObject; 
	}
}