package SubmodelGeneratorComponent;

import org.eclipse.basyx.submodel.metamodel.api.identifier.IdentifierType;
import org.eclipse.basyx.submodel.metamodel.api.reference.enums.KeyElements;
import org.eclipse.basyx.submodel.metamodel.map.Submodel;
import org.eclipse.basyx.submodel.metamodel.map.identifier.Identifier;
import org.eclipse.basyx.submodel.metamodel.map.qualifier.AdministrativeInformation;
import org.eclipse.basyx.submodel.metamodel.map.qualifier.LangString;
import org.eclipse.basyx.submodel.metamodel.map.qualifier.LangStrings;
import org.eclipse.basyx.submodel.metamodel.map.reference.Key;
import org.eclipse.basyx.submodel.metamodel.map.reference.Reference;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.SubmodelElementCollection;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.MultiLanguageProperty;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.property.Property;
import org.eclipse.basyx.submodel.metamodel.map.submodelelement.dataelement.property.valuetype.ValueType;

public class TimeSeriesSubmodel extends Submodel{

	private static final String SEMANTICIDSTR = "https://admin-shell.io/idta/TimeSeries/1/1";
	private static final Identifier identifier = new Identifier(IdentifierType.IRI, SEMANTICIDSTR);
	private static final Reference SEMANTICID = new Reference(identifier, KeyElements.GLOBALREFERENCE, false);
	private static final String SUBMODELIDSHORT = "TimeSeries";
	private static final String descriptionEnLanguage = "en";
	private static final String descriptionEnText = "Contains time series data and references to time series data to discover and semantically describe them along the asset lifecycle.";
	private static final String descriptionDeLanguage = "de";
	private static final String descriptionDeText = "Enthält Zeitreihendaten und Referenzen auf Zeitreihendaten, um diese entlang des Asset Lebenszyklus aufzufinden und semantisch zu beschreiben.";
	private static final String version = "1";
	private static final String revision = "1";
	
	public TimeSeriesSubmodel() {
		
	}
	
	private void setSubmodelIdentification(String identifier) {
		final IdentifierType identifierType = IdentifierType.IRI;
		setIdentification(identifierType, identifier);
	}
	
	private void setSubmodelIdShort() {
		setIdShort(SUBMODELIDSHORT);
	}
	
	private void setSubmodelSemanticId() {
		setSemanticId(SEMANTICID);
	}
	
	private void setSubmodelDescription() {
		LangStrings descriptions = new LangStrings(); 
		final LangString descriptionEn = new LangString(descriptionEnLanguage, descriptionEnText);
		final LangString descriptionDe = new LangString(descriptionDeLanguage, descriptionDeText);
		descriptions.add(descriptionEn);
		descriptions.add(descriptionDe);
		setDescription(descriptions);
	}
	
	private void setSubmodelAdministration() {
		AdministrativeInformation adminInfos = new AdministrativeInformation(version, revision);
		setAdministration(adminInfos);
	}

	private void setMandatorySubmodelElements() {
		setSubmodelElementCollectionMetaData();
		setSubmodelElementCollectionSegements();
	}
	
	private void setSubmodelElementCollectionMetaData() {
		SubmodelElementCollection sec = new SubmodelElementCollection(); 
		sec.setOrdered(false);
		sec.setAllowDuplicates(false);
		final String semanticIdStringMetaData = "https://admin-shell.io/idta/TimeSeries/Metadata/1/1";
		final Reference semanticIdMetaData = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringMetaData, IdentifierType.IRI));
		sec.setSemanticId(semanticIdMetaData);
//		sec.setQualifiers(TODO);
		final String idShort = "Metadata";
		sec.setIdShort(idShort);
		sec.setCategory(null);
//		sec.setValue(TODO);
		this.addSubmodelElement(sec);
	}

	private void setSubmodelElementCollectionSegements() {
		SubmodelElementCollection sec = new SubmodelElementCollection(); 
		sec.setOrdered(false);
		sec.setAllowDuplicates(true);
		final String semanticIdStringSegements = "https://admin-shell.io/idta/TimeSeries/Segments/1/1";
		final Reference semanticIdSegements = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringSegements, IdentifierType.IRI));
		sec.setSemanticId(semanticIdSegements);
//		sec.setQualifiers(TODO);
		final String idShort = "Segments";
		sec.setIdShort(idShort);
		sec.setCategory(null);
		this.addSubmodelElement(sec);
	}
	
	public SubmodelElementCollection getSubmodelElementCollectionLinkedSegment(
			String name, 
			LangStrings names,
			LangStrings descriptions,
			long recordCount, 
			String startTime,
			String endTime, 
			String duration,
			long samplingInterval,
			long samplingRate,
			String state,
			String lastUpdate, 
			String endpoint, 
			String query) {
		SubmodelElementCollection sec = new SubmodelElementCollection(); 
		sec.setOrdered(false);
		sec.setAllowDuplicates(false);
		final String semanticIdStringSegements = "https://admin-shell.io/idta/TimeSeries/Segments/LinkedSegment/1/1";
		final Reference semanticIdSegements = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringSegements, IdentifierType.IRI));
		sec.setSemanticId(semanticIdSegements);
//		sec.setQualifiers(TODO);
		final String idShort = name;
		sec.setIdShort(idShort);
		sec.setCategory(null);
		sec.addSubmodelElement(createMLPName(names));
		sec.addSubmodelElement(createMLPDescriptions(descriptions));
		sec.addSubmodelElement(createPropRecordCount(recordCount));
		sec.addSubmodelElement(createPropStartTime(startTime));
		sec.addSubmodelElement(createPropEndTime(endTime));
		sec.addSubmodelElement(createPropDuration(duration));
		sec.addSubmodelElement(createPropSamplingInterval(samplingInterval));
		sec.addSubmodelElement(createPropSamplingRate(samplingRate));
		sec.addSubmodelElement(createPropState(state));
		sec.addSubmodelElement(createPropLastUpdate(lastUpdate));
		sec.addSubmodelElement(createPropEndpoint(endpoint));
		sec.addSubmodelElement(createPropQuery(query));
		return sec;
	}
	
	private Property createPropQuery(String query) {
		final String semanticIdStringQuery= "https://admin-shell.io/idta/TimeSeries/Segment/Query/1/1";
		final Reference semanticIdQuery = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringQuery, IdentifierType.IRI));
		return createProperty(query, semanticIdQuery, "Query", "PARAMETER", ValueType.String);
	}
	
	private Property createPropEndpoint(String endpoint) {
		final String semanticIdStringEndpoint = "https://admin-shell.io/idta/TimeSeries/Segment/Endpoint/1/1";
		final Reference semanticIdEndpoint = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringEndpoint, IdentifierType.IRI));
		return createProperty(endpoint, semanticIdEndpoint, "Endpoint", "PARAMETER", ValueType.String);
	}
	
	private Property createPropLastUpdate(String lastUpdate) {
		final String semanticIdStringLastUpdate = "https://admin-shell.io/idta/TimeSeries/Segment/LastUpdate/1/1";
		final Reference semanticIdLastUpdate = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringLastUpdate, IdentifierType.IRI));
		return createProperty(lastUpdate, semanticIdLastUpdate, "LastUpdate", "VARIABLE", ValueType.DateTimeStamp);
	}
	
	private Property createPropState(String state) {
		final String semanticIdStringState = "https://admin-shell.io/idta/TimeSeries/Segment/State/1/1";
		final Reference semanticIdState = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringState, IdentifierType.IRI));
		return createProperty(state, semanticIdState, "State", "PARAMETER", ValueType.String);
	}
	
	private Property createPropSamplingRate(long samplingRate) {
		final String semanticIdStringSamplingRate = "https://admin-shell.io/idta/TimeSeries/Segment/SamplingRate/1/1";
		final Reference semanticIdSamplingRate = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringSamplingRate, IdentifierType.IRI));
		return createProperty(samplingRate, semanticIdSamplingRate, "SamplingRate", "PARAMETER", ValueType.Int64);
	}
	
	private Property createPropSamplingInterval(long samplingInterval) {
		final String semanticIdStringSi = "https://admin-shell.io/idta/TimeSeries/Segment/SamplingInterval/1/1";
		final Reference semanticIdSi = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringSi, IdentifierType.IRI));
		return createProperty(samplingInterval, semanticIdSi, "SamplingInterval", "PARAMETER", ValueType.Int64);
	}
	
	private Property createPropDuration(String duration) {
		final String semanticIdStringDuration = "https://admin-shell.io/idta/TimeSeries/Segment/Duration/1/1";
		final Reference semanticIdDuration = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringDuration, IdentifierType.IRI));
		return createProperty(duration, semanticIdDuration, "Duration", "VARIABLE", ValueType.String);
	}
	
	private Property createPropStartTime(String startTime) {
		final String semanticIdStringTs = "https://admin-shell.io/idta/TimeSeries/Segment/StartTime/1/1";
		final Reference semanticIdTs = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringTs, IdentifierType.IRI));
		return createProperty(startTime, semanticIdTs, "StartTime", "VARIABLE", ValueType.DateTimeStamp);
	}
	
	private Property createPropEndTime(String endTime) {
		final String semanticIdStringTs = "https://admin-shell.io/idta/TimeSeries/Segment/EndTime/1/1";
		final Reference semanticIdTs = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringTs, IdentifierType.IRI));
		return createProperty(endTime, semanticIdTs, "EndTime", "VARIABLE", ValueType.DateTimeStamp);
	}
	
	private MultiLanguageProperty createMLPName(LangStrings langStrings){
		final String semanticIdStringName = "https://admin-shell.io/idta/TimeSeries/Segment/Name/1/1";
		final Reference semanticIdName = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringName, IdentifierType.IRI));
		return createMultiLanguageProperty(langStrings, semanticIdName, "Name", "PARAMETER"); 
	}
	
	private MultiLanguageProperty createMLPDescriptions(LangStrings langStrings){
		final String semanticIdStringDescr = "https://admin-shell.io/idta/TimeSeries/Segment/Description/1/1";
		final Reference semanticIdDescr = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringDescr, IdentifierType.IRI));
		return createMultiLanguageProperty(langStrings, semanticIdDescr, "Description", "PARAMETER"); 
	}
	
	private Property createPropRecordCount(long value) {
		final String semanticIdStringRecordCount = "https://admin-shell.io/idta/TimeSeries/Segment/RecordCount/1/1";
		final Reference semanticIdRecordCount = new Reference(new Key(KeyElements.CONCEPTDESCRIPTION, true, semanticIdStringRecordCount, IdentifierType.IRI));
		return createProperty(value, semanticIdRecordCount, "RecordCount", "VARIABLE", ValueType.Int64);
	}
	
	private Property createProperty(Object value, Reference ref, String idShort, String category,ValueType valueType) {
		Property prop = new Property(); 
		prop.setValue(value);
		prop.setSemanticId(ref);
//		prop.setQualifiers(TODO);
		prop.setIdShort(idShort);
		prop.setCategory(category);
		prop.setValueType(valueType);
		return prop; 
	}
	
	private MultiLanguageProperty createMultiLanguageProperty(LangStrings value, Reference ref, String idShort, String category) {
		MultiLanguageProperty mlp = new MultiLanguageProperty();
		mlp.setValue(value);
		mlp.setSemanticId(ref);
//		sec.setQualifiers(TODO);
		mlp.setIdShort(idShort);
		mlp.setCategory(category);
		return mlp; 
	}
	
	public Submodel getEmptySubmodel(String identifier) {
		setSubmodelSemanticId();
		setSubmodelIdShort();
		setSubmodelDescription();
		setSubmodelAdministration(); 
		setMandatorySubmodelElements();
		setSubmodelIdentification(identifier);
		return this;
	}
	

}