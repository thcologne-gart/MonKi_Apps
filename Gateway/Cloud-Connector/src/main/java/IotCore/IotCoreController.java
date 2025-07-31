package IotCore;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.security.KeyStore;
import java.util.Properties;

import com.amazonaws.services.iot.client.AWSIotException;
import com.amazonaws.services.iot.client.AWSIotMqttClient;
import com.amazonaws.services.iot.client.AWSIotQos;
import com.amazonaws.services.iot.client.sample.sampleUtil.SampleUtil;
import com.amazonaws.services.iot.client.sample.sampleUtil.SampleUtil.KeyStorePasswordPair;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import FileHandler.ConfigFileHandler;

public class IotCoreController {

	private static final String configFilename = "AWSMqttClientConfig.json";
	private static final String CLIENTENDPOINT = "clientEndpoint";
	private static final String CLIENTID = "clientId";
	private static final String CERTIFICATEFILE = "certificateFile";
	private static final String PRIVATEKEYFILE = "privateKeyFile";
	private static final String certsPath = "certs/";

	private ConfigFileHandler configFile;
	private KeyStorePasswordPair pair ;
	private static AWSIotMqttClient awsMqttClient;

	public IotCoreController() {
		configFile = new ConfigFileHandler(configFilename);
		String clientEndpoint = configFile.getConfigJsonObject().get(CLIENTENDPOINT).getAsString();
		String clientId = configFile.getConfigJsonObject().get(CLIENTID).getAsString();
				String certificateFilePath = certsPath + configFile.getConfigJsonObject().get(CERTIFICATEFILE).getAsString();
				String privateKeyFilePath = certsPath + configFile.getConfigJsonObject().get(PRIVATEKEYFILE).getAsString();
				pair = SampleUtil.getKeyStorePasswordPair(
						certificateFilePath,
						privateKeyFilePath);
				awsMqttClient = new AWSIotMqttClient(
						clientEndpoint,
						clientId,
						pair.keyStore,
						pair.keyPassword);


	}

	///////////////////////////////////////////////
	
	private URL getCertificateFilePath() {
		 ClassLoader classLoader = IotCoreController.class.getClassLoader();
		URL resource = null;
		resource = classLoader.getResource("test.crt");
		return resource;
	}
	
	private URL getPrivateKeyFilePath() {
		URL resource = null;
		resource = getClass().getClassLoader().getResource("test.txt");
		return resource;
	}
	
	
	static String PropertyFile = "aws-iot-sdk-samples.properties";
	public String getConfig(String name) {
        Properties prop = new Properties();
        URL resource = null;
		try {
			resource = getClass().getClassLoader().getResource(PropertyFile);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        if (resource == null) {
            return null;
        }
        try (InputStream stream = resource.openStream()) {
        	prop.load(stream);
        } catch (IOException e) {
            return null;
        }
        String value = prop.getProperty(name);
        if (value == null || value.trim().length() == 0) {
            return null;
        } else {
            return value;
        }
    }

	///////////////////////////////////////////////

	public static boolean connectToAwsIotCore() {
		try {
			awsMqttClient.connect();
			return true;
		} catch (AWSIotException e) {
			e.printStackTrace();
			return false;
		}
	}

	public static boolean disconnectToAwsIotCore() {
		try {
			awsMqttClient.disconnect();
			return true;
		} catch (AWSIotException e) {
			e.printStackTrace();
			return false;
		}
	}

	public static boolean isConnectedToAwsIotCore() {
		return awsMqttClient.isCleanSession();
	}

	public static void publishMessage(String topic, JsonObject payload) {
		try {
			awsMqttClient.publish(topic, AWSIotQos.QOS0, payload.toString());
		} catch (AWSIotException e) {
			e.printStackTrace();
		} 
	}
}
