package Channels;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Set;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import BaSyxHandler.BaSyxController;
import IotCore.IotCoreController;
import IotMessage.MessageBuilder;

public class Channel extends Thread{

	private boolean channelRunningStatus;
	private String aasIdentifier;
	private int Timer10Minutes = 1000*60*10;//ms 10 Minuten
	private int Timer30Seconds = 1000*30;
	private MessageBuilder messageBuilder = new MessageBuilder();
	private JsonObject aas = new JsonObject();
	private ArrayList<JsonObject> submodelToTransferList = new ArrayList<>();
	private ArrayList<String> relevantSubmodels = new ArrayList<String>();
	private boolean channelInitStatus = false; 

	private static final String bacnetSmSemanticId = "https://th-koeln.de/gart/vocabulary/BACnetDatapointsInformation/1/0";
	private static final String IDSHORT = "idShort";
	private static final String KEYS = "keys";
	private static final String SEMANTICID = "semanticId";
	private static final String VALUE = "value";
	private static final String SUBMODELELEMENTS = "submodelElements";
	private static final int maxNumOfSem = 30; //maximum Number Of SEM For Single Transmission
	
	private static final String TIMESTAMP = "ts";
	private static final String PRESENTVALUE = "presentValue";

	private static final String MqttTopicAasRegistration = "MonKi/Gateway/AasRegistration";
	private static final String MqttTopicUpdateCompleteSubmodel = "MonKi/Gateway/UpdateCompleteSubmodel";
	private static final String MqttTopicUpdateCompleteSubmodelWithSplittedSem = "MonKi/Gateway/UpdateCompleteSubmodelWithSplittedSem";
	private static final String MqttTopicUpdateAllDynamicValues = "MonKi/Gateway/UpdateAllDynamicValues";

	public Channel(String aasId) {
		this.aasIdentifier = aasId; 
		relevantSubmodels.add(bacnetSmSemanticId);
	}

	@Override
	public void run() {
		setChannelStatus(true);
		setAasRegisterInformation();
		setSubmodelToTransferList();
		sendRegisterAasMessage();
		sendCompleteSubmodelsMessages();
		channelInitStatus = true; 
		while (channelRunningStatus == true) {
			sendSubmodelElementsValuesMessage();
			defaultSleep(Timer10Minutes);
		}
	}

	public void stopChannel() {
		setChannelStatus(false);
	}

	private void sendRegisterAasMessage() {
		JsonObject payload  = messageBuilder.getRegisterAasMessage(aas);
		IotCoreController.publishMessage(MqttTopicAasRegistration, payload);
		System.out.println("AAS Registered");
	}

	private void sendCompleteSubmodelsMessages() {
		for (JsonObject submodel : submodelToTransferList) {
			String smIdShort = submodel.get(IDSHORT).getAsString();
			String semanticId = getFirstSemanticIdFromObject(submodel.getAsJsonObject(SEMANTICID));
			if(isSubmodelRelevant(semanticId)) {
				if (hasSubmodelMoreThanXSubmodelElements(submodel,maxNumOfSem)) {
					sendSubmodelInXTransmissions(submodel, smIdShort);
				}
				else {
					sendSubmodelInOneTransmission(submodel, smIdShort);
				}
			}
		}
	}

	private void sendSubmodelElementsValuesMessage() {
		for (JsonObject submodel : submodelToTransferList) {
			String semanticIdToChek = getFirstSemanticIdFromObject(submodel.getAsJsonObject(SEMANTICID));
			if(isSubmodelRelevant(semanticIdToChek)) {
				JsonObject valueObj = BaSyxController.getAllSubmodelElementValues(aasIdentifier, submodel.get(IDSHORT).getAsString());
				valueObj = removeStaticValues(valueObj);
				System.out.println(valueObj);
				JsonObject payload = messageBuilder.getSubmodelElemenentsValuesMessage(valueObj,aasIdentifier,submodel.get(IDSHORT).getAsString());
				IotCoreController.publishMessage(MqttTopicUpdateAllDynamicValues, payload);
				String timeStamp = new SimpleDateFormat("yyyy.MM.dd.HH.mm.ss").format(new java.util.Date());
				System.out.println(timeStamp + " aasId " +aasIdentifier + " update values Message");
			}
		}
	}
	
	private void sendSubmodelInXTransmissions(JsonObject submodel, String smIdShort) {
		boolean countCondition = true; 
		int semCounter = 0;
		JsonArray submodelElements = submodel.getAsJsonArray(SUBMODELELEMENTS);
		submodel.add(SUBMODELELEMENTS, new JsonArray());
		sendSubmodelInOneTransmission(submodel, smIdShort);
		while (countCondition) {
			JsonObject semPayload = new JsonObject(); 
			JsonArray semToSend = new JsonArray();
			for(int i = 0 ; i < maxNumOfSem ; i++) {
				semToSend.add(submodelElements.get(semCounter));
				semCounter++; 
				if (semCounter == submodelElements.size()) {
					countCondition = false; 
					break;
				}
			}
			semPayload.add(SUBMODELELEMENTS, semToSend);
			JsonObject payload2 = messageBuilder.getCompleteSubmodelSplitMessage(semPayload, aasIdentifier, smIdShort);
			IotCoreController.publishMessage(MqttTopicUpdateCompleteSubmodelWithSplittedSem, payload2);
			defaultSleep(Timer30Seconds);
			System.out.println("transmit for " + smIdShort + " send. ");
		}
		System.out.println("transmittion for "+ smIdShort + " completed.");
	}

	private void sendSubmodelInOneTransmission(JsonObject submodel, String smIdShort) {
		JsonObject payload  = messageBuilder.getCompleteSubmodelMessage(submodel,aasIdentifier,smIdShort);
		IotCoreController.publishMessage(MqttTopicUpdateCompleteSubmodel, payload);
		System.out.println("submodel " + smIdShort + " send. ");
		defaultSleep(1000*10);
	}

	private boolean hasSubmodelMoreThanXSubmodelElements(JsonObject sm, int maxNumberOfSem) {
		int numberOfSem = sm.getAsJsonArray(SUBMODELELEMENTS).size();
		if (numberOfSem > maxNumberOfSem) {
			return true; 
		}
		else {
			return false; 
		}
	}

	private boolean isSubmodelRelevant(String semanticIdToCheck) {
		if (relevantSubmodels.contains(semanticIdToCheck)) {
			return true; 
		}
		else {
			return false;
		}
	}

	private String getFirstSemanticIdFromObject(JsonObject semanticIdObject) {
		return semanticIdObject.getAsJsonArray(KEYS).get(0).getAsJsonObject().get(VALUE).getAsString();
	}

	private JsonObject removeStaticValues(JsonObject allValuesObj) {
		JsonObject overallObj = new JsonObject(); 
		Set<String> keys1 = allValuesObj.keySet(); 
		for (String key1 : keys1) {
			JsonElement ele = allValuesObj.get(key1);
			if (ele.getClass() == JsonObject.class) {
				if (allValuesObj.getAsJsonObject(key1).has(PRESENTVALUE)) {
					JsonObject valueObj = new JsonObject(); 
					JsonElement valueElement = allValuesObj.getAsJsonObject(key1).get(PRESENTVALUE);
					Object obj = convertToDataType(valueElement.toString());
					if (obj.getClass() == java.lang.Boolean.class) {
						boolean val = Boolean.parseBoolean(obj.toString());
						valueObj.addProperty(PRESENTVALUE,val);
					}
					else if(obj.getClass() == java.lang.Double.class) {
						double val = Double.parseDouble(obj.toString());
						valueObj.addProperty(PRESENTVALUE,val);
					}
					else if(obj.getClass() == java.lang.Integer.class) {
						Integer val = Integer.parseInt(obj.toString());
						valueObj.addProperty(PRESENTVALUE,val);
					}
					else if(obj.getClass() == java.lang.String.class) {
						valueObj.addProperty(PRESENTVALUE,obj.toString());
					}
					else {
						System.out.println(obj.getClass());
					}
					valueObj.addProperty(TIMESTAMP, getSystemTimestamp());
					overallObj.add(key1, valueObj);
					
				}
			}
		}
		return overallObj;
	}
	
	public Object convertToDataType(String input) {
		input = input.replace("\"", "");
        if (input.equalsIgnoreCase("true") || input.equalsIgnoreCase("false")) {
            return Boolean.parseBoolean(input);
        }
        try {
            return Integer.parseInt(input);
        } catch (NumberFormatException e) {
            try {
                return Double.parseDouble(input);
            } catch (NumberFormatException e2) {
                return input;
            }
        }
    }
	
	private long getSystemTimestamp() {
		return System.currentTimeMillis();
	}

	private void setAasRegisterInformation() {
		aas = BaSyxController.getAas(aasIdentifier);
	}

	private void setSubmodelToTransferList() {
		for(JsonElement ele: BaSyxController.getAllSubmodels(aasIdentifier)) {
			JsonObject submodel = ele.getAsJsonObject();
			if (channelRunningStatus) {

			}
			submodelToTransferList.add(submodel);
		}
	}

	public boolean isChannelRunning() {
		return channelRunningStatus;
	}

	public void setChannelStatus(boolean channelStatus) {
		this.channelRunningStatus = channelStatus;
	}

	public String getAasIdentifier() {
		return aasIdentifier;
	}

	private void defaultSleep(int timer) {
		try {
			Thread.sleep(timer);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public boolean isChannelInitialited() {
		return channelInitStatus;
	}

	public void setChannelInitStatus(boolean channelInitStatus) {
		this.channelInitStatus = channelInitStatus;
	}
}