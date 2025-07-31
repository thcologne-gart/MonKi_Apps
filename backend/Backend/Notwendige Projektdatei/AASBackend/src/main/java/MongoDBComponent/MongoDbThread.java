package MongoDBComponent;

import java.sql.Date;

public class MongoDbThread extends Thread{
	
	private MongoDbTsHandler tsHandler; 
	
	private String userId = "";
	private String aasId = "";
	private String shortIdSm = "";
	private String smePath = "";
	private String[] smePaths;
	private Date date = null;
	private Date[] dates = null;
	private Object value = null;
	private Object[] values = null;
	private boolean transferSingleEntry = false; 
	
	public MongoDbThread(MongoDbConnector connector) {
		 tsHandler = new MongoDbTsHandler(connector);
	}

	public void run() {
		if (transferSingleEntry) {
			tsHandler.insertEntry(
					userId, 
					aasId, 
					shortIdSm, 
					smePath, 
					date, 
					value);
		}
		else {
			tsHandler.insertManyEntries(
					userId, 
					aasId, 
					shortIdSm, 
					smePaths, 
					dates, 
					values);
		}
	}
	
	public void setUserId(String userId) {
		this.userId = userId;
	}

	public void setAasId(String aasId) {
		this.aasId = aasId;
	}

	public void setShortIdSm(String shortIdSm) {
		this.shortIdSm = shortIdSm;
	}

	public void setSmePath(String smePath) {
		this.smePath = smePath;
	}
	
	public void setDate(Date date) {
		this.date = date;
	}

	public void setValue(Object value) {
		this.value = value;
	}

	public void setTransferSingleEntry(boolean transferSingleEntry) {
		this.transferSingleEntry = transferSingleEntry;
	}

	
	public void setSmePaths(String[] smePaths) {
		this.smePaths = smePaths;
	}
	

	public void setDates(Date[] dates) {
		this.dates = dates;
	}
	

	public void setValues(Object[] values) {
		this.values = values;
	}
}