package BaSyxGateComponent;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

import com.google.gson.Gson;

public abstract class BaSyxGate{
	
	//HTTP Variables
	private static final String HTTPGETPUTCOMMAND = "GET";
	protected static final String HTTPPUTCOMMAND = "PUT";
	protected static final String HTTPDELETECOMMAND = "DELETE";
	private static final int ConnectTimeout = 60000;
	private static final int ReadTimeout = 60000;
	protected static final String reqPropertyKey = "Content-Type";
	protected static final String reqPropertyValue = "application/json";
	
	//BaSyx Terms
	protected static final String ADDRESS = "address"; 
	protected static final String ASSETADMINISTRATIONSHELLDESCRIPTOR = "AssetAdministrationShellDescriptor"; 
	protected static final String ENDPOINTS = "endpoints"; 
	protected static final String NAME = "name"; 
	protected static final String MODELTYPE = "modelType";
	
	//AAS Terms
	protected static final String AAS = "aas";
	protected static final String ID = "id";
	protected static final String IDENTIFICATION = "identification";
	protected static final String IDSHORT = "idShort";
	protected static final String KEYS = "keys"; 
	protected static final String SEMANTICID = "semanticId"; 
	protected static final String SHELLS = "shells";
	protected static final String SUBMODEL = "submodel";
	protected static final String SUBMODELS = "submodels";
	protected static final String SUBMODELELEMENTS = "submodelElements";
	protected static final String VALUE = "value"; 
		
	//Encoding Variables
	protected static final String EncodedSlash = "%2F";
	protected static final String Slash = "/";
	protected static final char SLASH = 47;
	
	protected static Gson gson = new Gson();
	
	public BaSyxGate() {
		// TODO Auto-generated constructor stub
	}
	
	protected String httpGetCommand(String urlStr) {
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
	
	protected void httpPutCommand(String urlStr, String content) {
		try {
			URL url = new URL(urlStr);
			HttpURLConnection connection = (HttpURLConnection) url.openConnection();
			connection.setRequestMethod(HTTPPUTCOMMAND);
			connection.setDoOutput(true);
			connection.setDoInput(true);
			connection.setConnectTimeout(ConnectTimeout);
			connection.setReadTimeout(ReadTimeout);
			connection.setRequestProperty(reqPropertyKey, reqPropertyValue);
			OutputStreamWriter writer = new OutputStreamWriter(connection.getOutputStream());
			writer.write(content);
			writer.flush();
			writer.close();
			connection.getResponseCode();
		} catch (ProtocolException e) {
			e.printStackTrace();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	protected void httpDeleteCommand(String urlStr) {
		try {
			URL url = new URL(urlStr);
			HttpURLConnection connection = (HttpURLConnection) url.openConnection();
			connection.setRequestMethod(HTTPDELETECOMMAND);
			connection.setDoOutput(true);
			connection.setDoInput(true);
			connection.setConnectTimeout(ConnectTimeout);
			connection.setReadTimeout(ReadTimeout);
			connection.setRequestProperty(reqPropertyKey, reqPropertyValue);
			OutputStreamWriter writer = new OutputStreamWriter(connection.getOutputStream());
			writer.flush();
			writer.close();connection.getResponseCode();
		} catch (ProtocolException e) {
			e.printStackTrace();
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}