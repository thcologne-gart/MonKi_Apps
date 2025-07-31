package LambdaFunctions;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public abstract class IotCoreBasics {
	
	protected static final String urlAWSApiGatewayServiceAddressPrefix = "https://svmiv1rcci.execute-api.us-east-1.amazonaws.com/dev";
	
	protected static final String USERID = "userId";
	protected static final String AASIDENTIFIER = "aasIdentifier";
	
	private static final String POST = "POST";
	private static final String HTTPGETPUTCOMMAND = "GET";
	private static final String CONTENTTYPE= "Content-Type";
	private static final String APPLICATIONJSON = "application/json";
	private static final int ConnectTimeout = 60000;
	private static final int ReadTimeout = 60000;
	
	protected JsonNode convert(InputStream inputStream) throws IOException {
		BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
		StringBuilder stringBuilder = new StringBuilder();
		String line;
		while ((line = reader.readLine()) != null) {
			stringBuilder.append(line);
		}
		String jsonString = stringBuilder.toString();
		ObjectMapper mapper = new ObjectMapper();
		JsonNode actualObj = mapper.readTree(jsonString);
		return actualObj; 
	}
	
	@SuppressWarnings("unchecked")
	protected static List<String> getHttpPostAnswer(String urlString, ObjectNode jsonBody) {
		List<String> responseList = new ArrayList<>();
		try {
			URL url = new URL(urlString);
			HttpURLConnection connection = (HttpURLConnection) url.openConnection();
			connection.setRequestMethod(POST);
			connection.setRequestProperty(CONTENTTYPE, APPLICATIONJSON);
			connection.setDoOutput(true);
			ObjectMapper objectMapper = new ObjectMapper();
			OutputStream os = connection.getOutputStream();
			objectMapper.writeValue(os, jsonBody);
			os.flush();
			os.close();
			int responseCode = connection.getResponseCode();
			if (responseCode == HttpURLConnection.HTTP_OK) {
                InputStream responseStream = connection.getInputStream();
                responseList = objectMapper.readValue(responseStream, List.class);
                responseStream.close();
            } else {
                System.out.println("Request failed with response code: " + responseCode);
            }
			connection.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return responseList; 
	}

	protected void httpPost(String urlString, ObjectNode jsonBody) {
		System.out.println(urlString);
		try {
			URL url = new URL(urlString);
			HttpURLConnection connection = (HttpURLConnection) url.openConnection();
			connection.setRequestMethod(POST);
			connection.setRequestProperty(CONTENTTYPE, APPLICATIONJSON);
			connection.setDoOutput(true);
			ObjectMapper objectMapper = new ObjectMapper();
			OutputStream os = connection.getOutputStream();
			objectMapper.writeValue(os, jsonBody);
			os.flush();
			os.close();
			int responseCode = connection.getResponseCode();
			if (responseCode == HttpURLConnection.HTTP_OK) {
				System.out.println("Request good: " + responseCode);
            } else {
                System.out.println("Request failed with response code: " + responseCode);
            }
			connection.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	protected static String httpGetCommand(String urlStr) {
		StringBuffer response = new StringBuffer();
		try {
			URL url = new URL(urlStr);
			HttpURLConnection connection = (HttpURLConnection) url.openConnection();
			connection.setRequestMethod(HTTPGETPUTCOMMAND);
			connection.setDoOutput(true);
			connection.setConnectTimeout(ConnectTimeout);
			connection.setReadTimeout(ReadTimeout);
			int responseCode = connection.getResponseCode();
			if (responseCode == HttpURLConnection.HTTP_OK) { 
				BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
				String inputLine;
				while ((inputLine = in.readLine()) != null) {
					response.append(inputLine);
				}
				in.close();
			} else {
				System.out.println("GET request did not work: " + urlStr);
			}
		} catch (ProtocolException e) {
			e.printStackTrace();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return response.toString();
	}

}
