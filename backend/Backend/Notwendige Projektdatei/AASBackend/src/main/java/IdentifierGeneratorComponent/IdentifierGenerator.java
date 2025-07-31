package IdentifierGeneratorComponent;

public class IdentifierGenerator {

	private static final String identifierPart1 = "th-koeln.de/gart/";
	private static final String aas = "aas/";
	private static final String submodel = "submodel/";
	private static final String fs = "/"; //seperator

	public IdentifierGenerator() {
		// TODO Auto-generated constructor stub
	}
	
	//UnixTimeStampOfCreation[ms]
	private String getUnixTimeStamp() {
		Long uts = System.currentTimeMillis();
		return Long.toString(uts);
	}

	public String getIdentifierForAas() {
		return identifierPart1 + aas + getUnixTimeStamp();
	}
	
	public String getIdentifierForSubmodel(String submodelIdShort) {
		return identifierPart1 + submodel + submodelIdShort + fs + getUnixTimeStamp();
	}
}