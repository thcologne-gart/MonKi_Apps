package LambdaFunctions;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestStreamHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;

import LambdaModels.UpdateDynamicValuesMessage;

public class UpdateDynamicValues extends IotCoreBasics implements RequestStreamHandler {
	
	private static final String urlBackendPostValuesToAas = "/v1/gateway/updateDynamicValues"; 
	
	private static final String SUBMODELIDSHORT = "submodelIdShort";
	private static final String VALUESOBJECT = "valuesObject";
	
	@Override
	public void handleRequest(InputStream inputStream, OutputStream outputStream, Context context) throws IOException{
		JsonNode requestMessage = convert(inputStream);
		UpdateDynamicValuesMessage message = new UpdateDynamicValuesMessage(requestMessage);
		String userId = message.getUserId();
		JsonNode dynamicValues = message.getDynamicValues();
		String fieldDeviceAasId = message.getFieldDeviceAasId();
		String smIdShort = message.getSubmodelIdShort();
		postDynamicValuesToAas(userId, dynamicValues,fieldDeviceAasId,smIdShort);
	}
	
	private void postDynamicValuesToAas(String userId, JsonNode dynamicValuesObj, String fieldDeviceAasId, String smIdShort) {
		String url = urlAWSApiGatewayServiceAddressPrefix + urlBackendPostValuesToAas; 
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put(USERID, userId);
		jsonBody.put(AASIDENTIFIER, fieldDeviceAasId);
		jsonBody.put(SUBMODELIDSHORT,smIdShort);
		jsonBody.set(VALUESOBJECT, dynamicValuesObj);
		System.out.println(url);
		System.out.println(jsonBody);
		httpPost(url, jsonBody);
	}
}