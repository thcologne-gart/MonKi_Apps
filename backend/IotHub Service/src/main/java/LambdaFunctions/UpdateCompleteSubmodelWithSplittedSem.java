package LambdaFunctions;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestStreamHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import LambdaModels.UpdateCompleteSubmodelWithSplittedSemMessage;

public class UpdateCompleteSubmodelWithSplittedSem extends IotCoreBasics implements RequestStreamHandler{
	
	private static final String SUBMODELIDSHORT = "submodelIdShort";
	private static final String SUBMODELELEMENTS = "submodelElements";
	
	private static final String urlBackendPostSubmodelElementToAas = "/v1/gateway/addCompleteSubmodelelementsToAas";

	@Override
	public void handleRequest(InputStream inputStream, OutputStream outputStream, Context context) throws IOException{
		JsonNode requestMessage = convert(inputStream);
		UpdateCompleteSubmodelWithSplittedSemMessage message = new UpdateCompleteSubmodelWithSplittedSemMessage(requestMessage);
		String userId = message.getUserId();
		JsonNode submodelElements = message.getSubmodelElementsObject();
		String fieldDeviceAasId = message.getFieldDeviceAasId();
		String smIdShort = message.getSubmodelIdShort();
		postSubmodelElementsToAas(userId, submodelElements,fieldDeviceAasId, smIdShort);
	}
	
	@SuppressWarnings("deprecation")
	private void postSubmodelElementsToAas(String userId, JsonNode submodelElements, String fieldDeviceAasId, String smIdShort) {
		String url = urlAWSApiGatewayServiceAddressPrefix + urlBackendPostSubmodelElementToAas; 
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put(USERID, userId);
		jsonBody.put(AASIDENTIFIER, fieldDeviceAasId);
		jsonBody.put(SUBMODELIDSHORT, smIdShort);
		jsonBody.put(SUBMODELELEMENTS,submodelElements.get(SUBMODELELEMENTS));
		httpPost(url, jsonBody);
		System.out.println("fieldDeviceAasId: " + fieldDeviceAasId);
		System.out.println("submodel ID Short: " + smIdShort);
		System.out.println(url);
		System.out.println(jsonBody);
	}
}
