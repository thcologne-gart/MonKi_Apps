package LambdaFunctions;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.List;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestStreamHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import LambdaModels.AasRegistrationMessage;

public class aasRegistration extends IotCoreBasics  implements RequestStreamHandler {
	
	private static final String urlBackendSnippetGetAllAasIdentifier = "/v1/aas/getallaasidentifier"; 
	private static final String urlBackendSnippetAddAas = "/v1/aas/addaas";
	private static final String urlBackendAddBomSubmodel = "/v1/submodel/addsubmodeltoaas";
	private static final String urlBackendBomInitialPostSnippet = "/v1/submodel/bom/initialpost";
	private static final String urlBackendHasChildRelationToGatewayAas = "/v1/submodel/bom/addhaspartelement";
	
	private static final String AASOBJECT = "aasObject";
	private static final String SEMANTICIDSUBMODEL = "semanticIdSubmodel";
	private static final String ARCHETYPE = "ArcheType";
	private static final String FULL = "Full";
	private static final String ENTITYTYPE = "entityType";
	private static final String SELFMANAGESENTITY = "SelfManagedEntity";
	private static final String ENTITYAASIDENTIFIER = "EntitiyAasIdentifier";
	private static final String ISPARTOF = "IsPartOf";
	private static final String HASPART = "HasPart";
	private static final String SUBMODELIDSHORT = "submodelIdShort";
	private static final String HIERARCHICALSTRUCTURES = "HierarchicalStructures";
	private static final String BOMVALUES = "BomValues";
	
	private static final String submodelHsSemanticId = "https://admin-shell.io/idta/HierarchicalStructures/1/0/Submodel";
	
	@Override
	/*
	 * Takes an InputStream and an OutputStream. Reads from the InputStream,
	 * and copies all characters to the OutputStream.
	 */
	public void handleRequest(InputStream inputStream, OutputStream outputStream, Context context) throws IOException
	{
		JsonNode requestMessage = convert(inputStream);
		AasRegistrationMessage message = new AasRegistrationMessage(requestMessage);
		String userId = message.getUserId();
		String fieldDeviceAasId = message.getAasIdentifier();
		String gatewayAasId = message.getGatewayAasIdentifier();
		boolean registrationStatus = isAasAlreadyRegistered(fieldDeviceAasId,userId);
		if (registrationStatus) {
			//TODO: Logfile AAS Already registrated
			System.out.println("Aas with id: " + fieldDeviceAasId + " is already registered.");
		}
		else{
			addAas(userId,message.getAasObject()); 
			addHierarchicalStructureSubmodel(userId, fieldDeviceAasId);
			hierarchicalStructureInitialPost(userId, fieldDeviceAasId, gatewayAasId);
			addHasChildRelationToGatewayAas(userId, fieldDeviceAasId, gatewayAasId); 
		}
	}

	private boolean isAasAlreadyRegistered(String aasIdenifier, String userId) {
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put(USERID, userId);
		String urlAddress = urlAWSApiGatewayServiceAddressPrefix + urlBackendSnippetGetAllAasIdentifier;
		List<String> responseList = getHttpPostAnswer(urlAddress, jsonBody);
		if (responseList.contains(aasIdenifier)) {
			return true;
		}
		else {
			return false; 
		}
	}
	
	@SuppressWarnings("deprecation")
	private void addAas(String userId, JsonNode aasObject) {
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put(USERID, userId);
		jsonBody.put(AASOBJECT, aasObject);
		String urlAddress = urlAWSApiGatewayServiceAddressPrefix + urlBackendSnippetAddAas;
		httpPost(urlAddress, jsonBody);
	}
	
	private void addHierarchicalStructureSubmodel(String userId, String fieldDeviceAasId) {
		String url = urlAWSApiGatewayServiceAddressPrefix + urlBackendAddBomSubmodel;
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put(USERID, userId);
		jsonBody.put(AASIDENTIFIER, fieldDeviceAasId);
		jsonBody.put(SEMANTICIDSUBMODEL, submodelHsSemanticId);
		httpPost(url, jsonBody);
	}
	
	@SuppressWarnings("deprecation")
	private void hierarchicalStructureInitialPost(String userId, String fieldDeviceAasId, String gatewayAasId) {
		String url = urlAWSApiGatewayServiceAddressPrefix + urlBackendBomInitialPostSnippet;
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		ObjectNode bomValues = objectMapper.createObjectNode();
		ArrayNode hasPartArray = objectMapper.createArrayNode();
		ArrayNode IsPartOfArray = objectMapper.createArrayNode();
		bomValues.put(ARCHETYPE, FULL);
		bomValues.put(ENTITYTYPE, SELFMANAGESENTITY);
		bomValues.put(ENTITYAASIDENTIFIER, fieldDeviceAasId);
		IsPartOfArray.add(gatewayAasId);
		bomValues.put(ISPARTOF, IsPartOfArray);
		bomValues.put(HASPART, hasPartArray);
		jsonBody.put(USERID, userId);
		jsonBody.put(AASIDENTIFIER, fieldDeviceAasId);
		jsonBody.put(SUBMODELIDSHORT,HIERARCHICALSTRUCTURES);
		jsonBody.put(BOMVALUES,bomValues);
		httpPost(url, jsonBody);
	}
	
	@SuppressWarnings("deprecation")
	private void addHasChildRelationToGatewayAas(String userId, String aasIdFieldDevice, String aasIdGateway) {
		String url = urlAWSApiGatewayServiceAddressPrefix + urlBackendHasChildRelationToGatewayAas;
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		ObjectNode bomValuesObj = objectMapper.createObjectNode();
		bomValuesObj.put(ENTITYAASIDENTIFIER, aasIdGateway);
		bomValuesObj.put(HASPART, aasIdFieldDevice);
		jsonBody.put(BOMVALUES, bomValuesObj);
		jsonBody.put(USERID, userId);
		jsonBody.put(AASIDENTIFIER, aasIdGateway);
		jsonBody.put(SUBMODELIDSHORT, HIERARCHICALSTRUCTURES);
		httpPost(url, jsonBody);
	}	
}