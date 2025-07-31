package LambdaModels;

import com.fasterxml.jackson.databind.JsonNode;

public class AasRegistrationMessage extends MessageModel{
	
	private static final String IDENTIFICATION = "identification" ;
	private static final String ID = "id" ;
	private static final String IDSHORT = "idShort" ;

	public AasRegistrationMessage(JsonNode requestMessage) {
		super(requestMessage);
	}
	
	public String getAasIdentifier() {
		return getMessagePayload().get(IDENTIFICATION).get(ID).asText();
	}
	
	public String getAasIdShort() {
		return getMessagePayload().get(IDSHORT).asText();
	}
	
	public JsonNode getAasObject() {
		return getMessagePayload();
	}
}