package Application;

import java.util.ArrayList;
import java.util.Iterator;

import BaSyxHandler.BaSyxController;
import Channels.Channel;
import IotCore.IotCoreController;

public class ApplicationController extends Thread{
	
	private static final int timerForChannel = 5 * 1000;//ms 1 Minute
	
	private ApplicationModel model = new ApplicationModel(); 
	private ApplicationView view = new ApplicationView(); 
	
	public ApplicationController(ApplicationModel model, ApplicationView view) {
		this.model = model; 
		this.view = view; 
	}
	
	@Override
	public void run() {
		connectToAws();
		startChannels();
	}
	
	public void connectToAws() {
		if (IotCoreController.connectToAwsIotCore() == true) {
			model.setConnectionStatusAws(true);
		}
		else {
			model.setConnectionStatusAws(false);
		}
	}
	
	public void disconnectToAws() {
		if (IotCoreController.disconnectToAwsIotCore() == true) {
			model.setConnectionStatusAws(false);
		}
		else {
			model.setConnectionStatusAws(true);
		}
	}
	
	public void startChannels() {
		ArrayList<String> aasIdList = BaSyxController.getAllAasIdentifier();
		for (String aasId : aasIdList) {
			System.out.println("|||||||||||||||||||||||||||||||||||||||||||||");
			System.out.println("Start Channel for " + aasId);
			Channel channel = new Channel(aasId);
			channel.start();
			model.addChannel(aasId, channel);
			while (channel.isChannelInitialited() == false) {
				try {
					Thread.sleep(timerForChannel);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
			System.out.println("Channel for " + aasId + " is initialized");
		}
	}
	
	public void stopChannels() {
		ArrayList<String> aasIdList = BaSyxController.getAllAasIdentifier();
		for (String aasId : aasIdList) {
			model.getChannel(aasId).stopChannel();
		}
	}
}