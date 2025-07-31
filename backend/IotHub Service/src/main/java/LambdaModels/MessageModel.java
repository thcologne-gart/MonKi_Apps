package LambdaModels;

import com.fasterxml.jackson.databind.JsonNode;

public class MessageModel {
	
	private static final String GATEWAYINFO = "gatewayInfo" ;
	private static final String MESSAGEINFO = "messageInfo" ;
	private static final String MESSAGEPAYLOAD = "messagePayload" ;
	private static final String MESSAGETYPE = "messageType" ;
	private static final String GATEWAYAASIDENTIFIER = "GatewayAasIdentifier" ;
	private static final String USERID = "userId" ;
	
	
	private JsonNode gatewayInfo;
	private JsonNode messageInfo; 
	private JsonNode messagePayload; 
	private String messageType; 
	
	public MessageModel(JsonNode requestMessage ) {
		gatewayInfo = requestMessage.get(GATEWAYINFO);
		messageInfo = requestMessage.get(MESSAGEINFO);
		messagePayload = requestMessage.get(MESSAGEPAYLOAD);
		messageType = messageInfo.get(MESSAGETYPE).asText();
	}

	protected JsonNode getGatewayInfo() {
		return gatewayInfo;
	}

	protected JsonNode getMessagePayload() {
		return messagePayload;
	}
	
	public JsonNode getMessageInfo() {
		return messageInfo;
	}

	protected String getMessageType() {
		return messageType;
	}
	
	public String getGatewayAasIdentifier() {
		return getGatewayInfo().get(GATEWAYAASIDENTIFIER).asText();
	}
	
	public String getUserId() {
		return getGatewayInfo().get(USERID).asText();
	}
}