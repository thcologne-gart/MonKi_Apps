package Gateway;

import FileHandler.ConfigFileHandler;

public class GatewayModel {
	
	private static final String configFilename = "GatewayConfig.json";
	private static final String THINGNAME = "ThingName";
	private static final String THINGTYPE = "Thingtype";
	private static final String THINGID = "ThingId";
	private static final String GATEWAYAASID = "GatewayAasId";
	private static final String USERID = "UserId";
	
	private static String ThingName = "";
	private static String Thingtype = "";
	private static String ThingId = "";
	private static String GatewayAasId = "";
	private static String UserId = "";
	
	private ConfigFileHandler configFile;
	
	public GatewayModel() {
		configFile = new ConfigFileHandler(configFilename);
		ThingName = configFile.getConfigJsonObject().get(THINGNAME).getAsString();
		Thingtype = configFile.getConfigJsonObject().get(THINGTYPE).getAsString();
		ThingId = configFile.getConfigJsonObject().get(THINGID).getAsString();
		GatewayAasId = configFile.getConfigJsonObject().get(GATEWAYAASID).getAsString();
		UserId = configFile.getConfigJsonObject().get(USERID).getAsString();
	}

	public static String getUserId() {
		return UserId;
	}

	public static String getGatewayAasId() {
		return GatewayAasId;
	}

	public static String getThingId() {
		return ThingId;
	}

	public static String getThingtype() {
		return Thingtype;
	}

	public static String getThingName() {
		return ThingName;
	}
}