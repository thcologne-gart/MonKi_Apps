package LambdaFunctions;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestStreamHandler;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class IotClientConnectionStatus extends IotCoreBasics  implements RequestStreamHandler {
	
	private static final String urlApiServiceSetGWConnectionInformationSnippet = "/v1/gateway/setGatewayConnectionStatus";
	
	//Mandatory Entries
	private static final String CLIENTID = "clientId";
	private static final String TIMESTAMP = "timestamp";
	private static final String EVENTTYPE = "eventType";
	
	//Optional Entries
	private static final String IPADDRESS = "ipAddress";
	
	private static final String CONNECTED = "connected";
	private static final String DISCONNECTED = "disconnected";
	

	@Override
	/*
	 * Takes an InputStream and an OutputStream. Reads from the InputStream,
	 * and copies all characters to the OutputStream.
	 */
	public void handleRequest(InputStream inputStream, OutputStream outputStream, Context context) throws IOException
	{
		JsonNode requestMessage = convert(inputStream);
		String msgEventType = requestMessage.get(EVENTTYPE).asText();
		if (msgEventType.equals(CONNECTED)) {
			proceedConnectedEvent(requestMessage); 
		}
		else if(msgEventType.equals(DISCONNECTED)) {
			proceedDisconnectedEvent(requestMessage);
		}
		else {
			System.out.println("Fehler in message. Eventtype ist nicht verarbeitbar: ");
			System.out.println(requestMessage.toString());
		}
	}
	
	private void proceedConnectedEvent(JsonNode requestMessage) {
		String msgClientId = requestMessage.get(CLIENTID).asText();
		long msgtimestamp = requestMessage.get(TIMESTAMP).asLong();
		String msgEventType = requestMessage.get(EVENTTYPE).asText();
		String msgIpAddress = requestMessage.get(IPADDRESS).asText();
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put("clientId", msgClientId);
		jsonBody.put("timestamp", msgtimestamp);
		jsonBody.put("ipAddress", msgIpAddress);
		jsonBody.put("eventType", msgEventType);
		String urlAddress = urlAWSApiGatewayServiceAddressPrefix + urlApiServiceSetGWConnectionInformationSnippet;
		System.out.println(urlAddress);
		System.out.println(jsonBody);
		httpPost(urlAddress, jsonBody);
	}
	
	private void proceedDisconnectedEvent(JsonNode requestMessage) {
		String msgClientId = requestMessage.get(CLIENTID).asText();
		long msgtimestamp = requestMessage.get(TIMESTAMP).asLong();
		String msgEventType = requestMessage.get(EVENTTYPE).asText();	
		ObjectMapper objectMapper = new ObjectMapper();
		ObjectNode jsonBody = objectMapper.createObjectNode();
		jsonBody.put("clientId", msgClientId);
		jsonBody.put("timestamp", msgtimestamp);
		jsonBody.put("eventType", msgEventType);
		String urlAddress = urlAWSApiGatewayServiceAddressPrefix + urlApiServiceSetGWConnectionInformationSnippet;
		System.out.println(urlAddress);
		System.out.println(jsonBody);
		httpPost(urlAddress, jsonBody);
	}
}