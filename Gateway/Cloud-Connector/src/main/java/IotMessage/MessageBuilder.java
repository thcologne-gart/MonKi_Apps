package IotMessage;

import com.google.gson.JsonObject;

import Gateway.GatewayModel;

public class MessageBuilder {
	
	private static final String GATEWAYINFO = "gatewayInfo";
	private static final String MESSAGEINFO = "messageInfo";
	private static final String MESSAGEPAYLOAD = "messagePayload";
	
	private static final String MESSAGETYPE = "messageType";
		
	private static final String THINGNAME = "ThingName";
	private static final String OBJECTTYPE = "ObjectType";
	private static final String THINGID = "ThingId";
	private static final String GATEWAYAASIDENTIFIER = "GatewayAasIdentifier";
	private static final String USERID = "userId";
	
	private JsonObject gatewayInfo;
	private JsonObject messageInfo; 
	private JsonObject message;
	
	public MessageBuilder() {
		setGatewayInfo();
	}
	
	private void setGatewayInfo() {
		gatewayInfo = new JsonObject();
		gatewayInfo.addProperty(THINGNAME, GatewayModel.getThingName());
		gatewayInfo.addProperty(OBJECTTYPE, GatewayModel.getThingtype());
		gatewayInfo.addProperty(THINGID, GatewayModel.getThingId());
		gatewayInfo.addProperty(GATEWAYAASIDENTIFIER, GatewayModel.getGatewayAasId());
		gatewayInfo.addProperty(USERID, GatewayModel.getUserId());
		
	}
	
	private JsonObject buildMessage(JsonObject messageInfo, JsonObject messagePayload) {
		message = new JsonObject(); 
		message.add(GATEWAYINFO, gatewayInfo);
		message.add(MESSAGEINFO, messageInfo);
		message.add(MESSAGEPAYLOAD, messagePayload);
		return message; 
	}
	
	public JsonObject getRegisterAasMessage(JsonObject payload) {
		messageInfo = new JsonObject();
		messageInfo.addProperty(MESSAGETYPE, "RegisterAasMessage");
		return buildMessage(messageInfo,payload);
	}
	
	public JsonObject getCompleteSubmodelMessage(JsonObject payload, String localAasIdentifier, String smIdShort) {
		messageInfo = new JsonObject();
		messageInfo.addProperty(MESSAGETYPE, "CompleteSubmodelMessage");
		messageInfo.addProperty("aasIdentifier", localAasIdentifier);
		messageInfo.addProperty("submodelIdShort", smIdShort);
		return buildMessage(messageInfo,payload);
	}
	
	public  JsonObject getCompleteSubmodelSplitMessage(JsonObject payload, String localAasIdentifier, String smIdShort) {
		messageInfo = new JsonObject();
		messageInfo.addProperty(MESSAGETYPE, "CompleteSubmodelSplitMessage");
		messageInfo.addProperty("aasIdentifier", localAasIdentifier);
		messageInfo.addProperty("submodelIdShort", smIdShort);
		return buildMessage(messageInfo,payload);
	}
	
	public JsonObject getSubmodelElemenentsValuesMessage(JsonObject payload, String localAasIdentifier, String smIdShort) {
		messageInfo = new JsonObject();
		messageInfo.addProperty(MESSAGETYPE, "AllDynamicSubmodelElementValues");
		messageInfo.addProperty("aasIdentifier", localAasIdentifier);
		messageInfo.addProperty("submodelIdShort", smIdShort);
		return buildMessage(messageInfo,payload);
	}
}