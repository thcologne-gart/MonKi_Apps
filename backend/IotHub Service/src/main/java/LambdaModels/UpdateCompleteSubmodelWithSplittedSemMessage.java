package LambdaModels;

import com.fasterxml.jackson.databind.JsonNode;

public class UpdateCompleteSubmodelWithSplittedSemMessage extends UpdateCompleteSubmodelMessage{

	public UpdateCompleteSubmodelWithSplittedSemMessage(JsonNode requestMessage) {
		super(requestMessage);
	}
	
	public JsonNode getSubmodelElementsObject() {
		return getMessagePayload();
	}
}