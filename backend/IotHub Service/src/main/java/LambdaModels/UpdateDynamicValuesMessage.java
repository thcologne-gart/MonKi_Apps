package LambdaModels;

import com.fasterxml.jackson.databind.JsonNode;

public class UpdateDynamicValuesMessage extends MessageModel{
	
	private static final String AASIDENTIFIER = "aasIdentifier";
	private static final String SUBMODELIDSHORT ="submodelIdShort";

	public UpdateDynamicValuesMessage(JsonNode requestMessage) {
		super(requestMessage);
	}
	
	public JsonNode getDynamicValues() {
		return getMessagePayload();
	}
	
	public String getFieldDeviceAasId() {
		return getMessageInfo().get(AASIDENTIFIER).asText();
	}
	
	public String getSubmodelIdShort() {
		return getMessageInfo().get(SUBMODELIDSHORT).asText();
	}

}
