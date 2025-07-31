package BaSyxHandler;

import java.util.ArrayList;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import BaSyxGateComponent.BaSyxAasServerGate;
import BaSyxGateComponent.BaSyxRegistryGate;
import FileHandler.ConfigFileHandler;

public class BaSyxController {
	
	private static final String configFilename = "BaSyxConfig.json"; 
	private static final String REGISTRYADDRESS = "RegistryAddress";
	private static final String AASSERVERADDRESS = "AasServerAddress";
	private ConfigFileHandler configFile; 
	private static String registryAddress;
	private static String aasServerAddress;
	
	public static BaSyxRegistryGate registryGate = new BaSyxRegistryGate(); 
	public static BaSyxAasServerGate aasServerGate = new BaSyxAasServerGate(); 
	
	private static ArrayList<String> allAasIdentifier = new ArrayList<String>();
	
	public BaSyxController() {
		configFile = new ConfigFileHandler(configFilename);
		registryAddress = configFile.getConfigJsonObject().get(REGISTRYADDRESS).getAsString();
		aasServerAddress = configFile.getConfigJsonObject().get(AASSERVERADDRESS).getAsString();
		setAllAasIdentifierList();
	}
	
	public void setAllAasIdentifierList() {
		String onlyAcceptedAasId = "th-koeln.de/gart/aas/1698680654";
		JsonArray array = registryGate.getAllAasIdentifier(registryAddress);
		for (JsonElement ele : array) {
			if (ele.getAsString().equals(onlyAcceptedAasId)) {
				System.out.println("nur die hier: " + ele.getAsString());
				allAasIdentifier.add(ele.getAsString());
			}
			else {
				System.out.println("die hier nicht: " + ele.getAsString());
			}
		}
	}
	
	public static ArrayList<String> getAllAasIdentifier(){
		return allAasIdentifier;
	}
	
	public static JsonObject getAas(String aasId) {
		return aasServerGate.getAasByIdentifier(aasServerAddress, aasId);
	}
	
	public static JsonObject getCompleteSubmodel(String aasId, String smIdShort) {
		return aasServerGate.getSubmodel(aasServerAddress, aasId, smIdShort);
	}
	
	public static JsonObject getAllSubmodelElementValues(String aasId, String smIdShort) {
		return aasServerGate.getSubmodelElementValues(aasServerAddress, aasId, smIdShort);
	}
	
	public static JsonArray getAllSubmodels(String aasId) {
		return aasServerGate.getSubmodelsArray(aasServerAddress, aasId);
	}
}