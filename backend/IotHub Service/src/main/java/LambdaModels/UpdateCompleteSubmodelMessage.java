package LambdaModels;

import com.fasterxml.jackson.databind.JsonNode;

public class UpdateCompleteSubmodelMessage extends MessageModel{
	
	private static final String AASIDENTIFIER = "aasIdentifier";
	private static final String SUBMODELIDSHORT ="submodelIdShort";

	public UpdateCompleteSubmodelMessage(JsonNode requestMessage) {
		super(requestMessage);
		// TODO Auto-generated constructor stub
	}
	
	public JsonNode getCompleteSubmodel() {
		return getMessagePayload();
	}
	
	public String getFieldDeviceAasId() {
		return getMessageInfo().get(AASIDENTIFIER).asText();
	}
	
	public String getSubmodelIdShort() {
		return getMessageInfo().get(SUBMODELIDSHORT).asText();
	}
}