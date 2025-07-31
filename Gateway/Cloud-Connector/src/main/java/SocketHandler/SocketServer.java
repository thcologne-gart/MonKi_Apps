package SocketHandler;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

import Application.ApplicationController;

public class SocketServer {
	
	private static final String DISCONNECTIOTCORE = "disconnectIotCore";
	private static final String CONNECTIOTCORE = "connectIotCore";
	private static final String STARTCHANNELS = "startChannels";
	private static final String STOPCHANNELS = "stopChannels";

	private int portNumber = 5001;
	private ApplicationController appController;

	private boolean runningStatus = false;

	public SocketServer(ApplicationController appController) {
		this.appController = appController; 

	}

	public void startSocketServer(){
		runningStatus = true;
		try (ServerSocket serverSocket = new ServerSocket(portNumber)) {
			System.out.println("Server gestartet. Warte auf Verbindung auf Port " + portNumber + "...");
			waitForClientConnection(serverSocket);
		} catch (IOException e) {
			System.err.println("Fehler beim Starten des Servers: " + e.getMessage());
		}
	}

	public void waitForClientConnection(ServerSocket serverSocket) {
		while (runningStatus) {
			try (Socket clientSocket = serverSocket.accept();
					PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
					BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))) {
				System.out.println("Client verbunden.");
				manageInputLine(out,in);
				System.out.println("Client getrennt.");
			} catch (IOException e) {
				System.err.println("Fehler bei der Kommunikation mit dem Client: " + e.getMessage());
			}
		}
	}

	private void manageInputLine(PrintWriter out, BufferedReader in) {
		String inputLine;
		try {
			while ((inputLine = in.readLine()) != null) {
				if (inputLine.contains(DISCONNECTIOTCORE)) {
					disconnectIotCore(out);
				}
				else if (inputLine.contains(CONNECTIOTCORE)) {
					connectIotCore(out);
				}
				else if (inputLine.contains(STARTCHANNELS)) {
					startChannels(out);
				}
				else if (inputLine.contains(STOPCHANNELS)) {
					stopChannels(out);
				}
				else {
					inputError(out);
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	private void inputError(PrintWriter out) {
		System.out.println("Eingabe fehlerhaft");
		out.print("Server kann die Eingabe nicht verarbeiten.");
	}
	
	private void disconnectIotCore(PrintWriter out) {
		appController.disconnectToAws();
		out.println("Disconneted to Aws IotCore");
	}
	
	private void connectIotCore(PrintWriter out) {
		appController.connectToAws();
		out.println("Conneted to Aws IotCore");
	}
	
	private void startChannels(PrintWriter out) {
		appController.startChannels();
		out.println("channels started");
	}
	
	private void stopChannels(PrintWriter out) {
		appController.stopChannels();
		out.println("channels stoped");
		
	}
}