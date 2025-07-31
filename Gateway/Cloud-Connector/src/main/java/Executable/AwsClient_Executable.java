package Executable;

import Application.ApplicationController;
import Application.ApplicationModel;
import Application.ApplicationView;
import BaSyxHandler.BaSyxController;
import Gateway.GatewayModel;
import IotCore.IotCoreController;
import SocketHandler.SocketServer;

public class AwsClient_Executable {

	@SuppressWarnings("unused")
	public static void main(String[] args) {
		GatewayModel gatewayModel = new GatewayModel(); 
		IotCoreController iotCoreController = new IotCoreController();
		BaSyxController baSyxController = new BaSyxController();
		
//		ApplicationModel appModel = new ApplicationModel(); 
//		ApplicationView appView = new ApplicationView(); 
//		ApplicationController appController = new ApplicationController(appModel, appView); 
//		appController.start();
//		
//		SocketServer socketServer = new SocketServer(appController);
//		socketServer.startSocketServer();
	}
}