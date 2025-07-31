package ApiV1SubmodelTsComponent;

import java.util.List;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

public interface ITimeSeriesAPI {
	
	public static final String INITIALIZESUBMODEL_POST = "/initializeSubmodel";
	public static final String CREATETIMESERIES_POST = "/createTimeSeries";
	public static final String READTIMESERIES_POST = "/readTimeSeries";
	public static final String UPDATETIMESERIES_POST = "/updateTimeSeries";
	public static final String DELETETIMESERIES_POST = "/deleteTimeSeries";
	
	@PostMapping(INITIALIZESUBMODEL_POST)
	public void initializeSubmodel(@RequestBody String jsonObjectStr);
	
	@PostMapping(CREATETIMESERIES_POST)
	public void createTimeSeries(@RequestBody String jsonObjectStr);
	
	@PostMapping(READTIMESERIES_POST)
	public List<?> readTimeSeries(@RequestBody String jsonObjectStr);
	
	@PostMapping(UPDATETIMESERIES_POST)
	public void updateTimeSeries(@RequestBody String jsonObjectStr);
	
	@PostMapping(DELETETIMESERIES_POST)
	public void deleteTimeSeries(@RequestBody String jsonObjectStr);
	
}