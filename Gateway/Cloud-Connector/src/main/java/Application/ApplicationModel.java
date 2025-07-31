package Application;

import java.util.HashMap;

import Channels.Channel;

public class ApplicationModel {
	

	private HashMap<String, Channel> channelsMap = new  HashMap<>(); 
	private boolean connectionStatusAws = false;
	private boolean runningStatusChannels = false;
	
	public ApplicationModel() {
		
	}
	
	public Channel getChannel(String aasId) {
		return channelsMap.get(aasId);
	}
	
	public void addChannel(String aasId, Channel channel) {
		channelsMap.put(aasId, channel);
	}
	
	public void removeChannel(String aasId) {
		channelsMap.remove(aasId);
	}

	public boolean getConnectionStatusAws() {
		return connectionStatusAws;
	}

	public void setConnectionStatusAws(boolean connectionStatusAws) {
		this.connectionStatusAws = connectionStatusAws;
	}

	public boolean getRunningStatusChannels() {
		return runningStatusChannels;
	}

	public void setRunningStatusChannels(boolean runningStatusChannels) {
		this.runningStatusChannels = runningStatusChannels;
	}
}