package ApiV1SubmodelTsComponent;

import java.util.List;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

@RestController
@RequestMapping(path = "GART/api/v1/Submodel/TimeSeries")
public class SubmodelTimeSeriesRestApi implements ITimeSeriesAPI{

	private static final String AASSERVERADDRESS = "aasServerAddress";
	private static final String REGISTRYADDRESS = "registryAddress";
	private static final String AASIDENTIFIER = "aasIdentifier";
	private static final String SUBMODELREF = "submodelRef";
	private static final String SUBMODELELEMENTPATH = "submodelElementPath";
	private static final String TIMESTAMPSTART = "timestampStart";
	private static final String TIMESTAMPSTOP = "timestampStop";
	private static final String SAMPLINGINTERVAL = "samplingInterval";
	private static final String TIMESERIESNAME = "timeSeriesName";
	private static final String LOCALHOST = "localhost"; 
	
	private TimeSeriesServices serviceController = new TimeSeriesServices(); 
	
	@Override
	public void initializeSubmodel(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasServerAddress = body.get(AASSERVERADDRESS).getAsString();
		String registryAddress = body.get(REGISTRYADDRESS).getAsString();
		String aasId = body.get(AASIDENTIFIER).getAsString();
		serviceController.createTimeSeriesSubmodel(registryAddress,aasServerAddress,LOCALHOST, aasId);
	}
	
	@Override
	public void createTimeSeries(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasId = body.get(AASIDENTIFIER).getAsString();
		String submodelRef = body.get(SUBMODELREF).getAsString();
		String propertyRef = body.get(SUBMODELELEMENTPATH).getAsString();
		int samplingIntervall = body.get(SAMPLINGINTERVAL).getAsInt();
		String timeSeriesName = body.get(TIMESERIESNAME).getAsString();
		serviceController.createTimeSeries(LOCALHOST, aasId, submodelRef, propertyRef, samplingIntervall, timeSeriesName);
	}

	@Override
	public List<?> readTimeSeries(String jsonObjectStr) {
		JsonObject body = new Gson().fromJson(jsonObjectStr, JsonObject.class);
		String aasId = body.get(AASIDENTIFIER).getAsString(); 
		String shortIdSubmodel = body.get(SUBMODELREF).getAsString(); 
		String smePath = body.get(SUBMODELELEMENTPATH).getAsString(); 
		long tsBegin = body.get(TIMESTAMPSTART).getAsLong();
		long tsEnd  = body.get(TIMESTAMPSTOP).getAsLong(); 
		JsonArray jsonArray = serviceController.readTimeSeries(
				LOCALHOST, 
				aasId, 
				shortIdSubmodel, 
				smePath, 
				tsBegin, 
				tsEnd);
		return serviceController.convertJsonArrayToList(jsonArray);
	}

	@Override
	public void updateTimeSeries(String jsonObjectStr) {
		// TODO Auto-generated method stub
	}

	@Override
	public void deleteTimeSeries(String jsonObjectStr) {
		// TODO Auto-generated method stub
	}
}