package LambdaFunctions;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestStreamHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import LambdaModels.UpdateCompleteSubmodelMessage;

public class UpdateCompleteSubmodel extends IotCoreBasics implements RequestStreamHandler {
	
	private static final String COMPLETESUBMODEL = "completeSubmodel";
	private static final String IDSHORT = "idShort";
	
	private static final String urlBackendPostCompleteSubmodelToAas = "/v1/submodel/addcompletesubmodeltoaas";
	
	@Override
	public void handleRequest(InputStream inputStream, OutputStream outputStream, Context context) throws IOException{
		JsonNode requestMessage = convert(inputStream);
		UpdateCompleteSubmodelMessage message = new UpdateCompleteSubmodelMessage(requestMessage);
		String userId = message.getUserId();
		JsonNode completeSubmodel = message.getCompleteSubmodel();
		String fieldDeviceAasId = message.getFieldDeviceAasId();
		postCompleteSubmodelToAas(userId, completeSubmodel,fieldDeviceAasId);
	}
	
	@SuppressWarnings("deprecation")
	private void postCompleteSubmodelToAas(String userId, JsonNode completeSubmodel, String fieldDeviceAasId) {
		String url = urlAWSApiGatewayServiceAddressPrefix + urlBackendPostCompleteSubmodelToAas; 
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put(USERID, userId);
		jsonBody.put(AASIDENTIFIER, fieldDeviceAasId);
		jsonBody.put(COMPLETESUBMODEL, completeSubmodel);
		jsonBody.put(IDSHORT, completeSubmodel.get(IDSHORT).asText());
		httpPost(url, jsonBody);
		System.out.println(jsonBody);
		System.out.println("fieldDeviceAasId: " + fieldDeviceAasId);
		System.out.println("submodel ID Short: " + completeSubmodel.get(IDSHORT).asText());
	}
}