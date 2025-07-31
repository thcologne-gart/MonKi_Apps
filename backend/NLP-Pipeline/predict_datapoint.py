import json
import pandas as pd
import requests
import time

# Aufruf NLP Pipeline zum Labeln der Grundfunktion -> Text Classification
def label_grundfunktion(submodel_df):
    for index, row in submodel_df.iterrows():
        text = row["NLPText"]
        headers = {
            'Authorization': 'Bearer BWKspKrXvGhLerysCyfYISapWopuGGPTDRxAowpKsiPugTuTqNLQrSPTJEvGkOsVQLIGyBEaNHymluAgZpRClVFJdQuRgvMGIpnWBPTAxnEIZGgthUdywhaqoGIZsewN',
            'Content-Type': 'application/json',
        }

        json_data = {
            'inputs': text,
            'parameters': {
                'top_k': None,
            },
        }
        api_url = 'https://h26lgs9gt0v7kmap.eu-west-1.aws.endpoints.huggingface.cloud'
        response = requests.post(api_url, headers=headers, json=json_data)

        encoded_response = json.loads(response.content.decode("utf-8"))
        # Erste Eintrag der Liste hat den höchsten Wert
        label_digit = encoded_response[0]['label']
        label_score = encoded_response[0]['score']
        label_mapping = {
            'LABEL_0': 'Andere Anlagen',
            'LABEL_1': 'Befördern',
            'LABEL_2': 'Kälte versorgen',
            'LABEL_3': 'Luft versorgen',
            'LABEL_4': 'Medien versorgen',
            'LABEL_5': 'Sichern',
            'LABEL_6': 'Strom versorgen',
            'LABEL_7': 'Wärme versorgen'
        }
        label_name = label_mapping.get(label_digit)

        #row['LabelGrundfunktion'] = label_name
        #row['ScoreGrundfunktion'] = label_score

        submodel_df.at[index, 'LabelGrundfunktion'] = label_name
        submodel_df.at[index, 'ScoreGrundfunktion'] = label_score


    return submodel_df

# Aufruf NLP Pipeline zum Labeln der zweiten Ebene -> Text Classification
def label_ebene_zwei(submodel_df, index, hf_url, label_mapping):
    text = submodel_df.at[index, "NLPText"]
    headers = {
        'Authorization': 'Bearer BWKspKrXvGhLerysCyfYISapWopuGGPTDRxAowpKsiPugTuTqNLQrSPTJEvGkOsVQLIGyBEaNHymluAgZpRClVFJdQuRgvMGIpnWBPTAxnEIZGgthUdywhaqoGIZsewN',
        'Content-Type': 'application/json',
    }

    json_data = {
        'inputs': text,
        'parameters': {
            'top_k': None,
        },
    }
    response = requests.post(hf_url, headers=headers, json=json_data)

    encoded_response = json.loads(response.content.decode("utf-8"))
    label_digit = encoded_response[0]['label']
    label_score = encoded_response[0]['score']
    label_name = label_mapping.get(label_digit)
    submodel_df.at[index, 'LabelZweiteEbene'] = label_name
    submodel_df.at[index, 'ScoreZweiteEbene'] = label_score
    return submodel_df
# Labeln Komponente -> Text Classification
def label_komponente(submodel_df, index, hf_url, label_mapping):
    text = submodel_df.at[index, "NLPText"]
    #print(text)
    headers = {
        'Authorization': 'Bearer BWKspKrXvGhLerysCyfYISapWopuGGPTDRxAowpKsiPugTuTqNLQrSPTJEvGkOsVQLIGyBEaNHymluAgZpRClVFJdQuRgvMGIpnWBPTAxnEIZGgthUdywhaqoGIZsewN',
        'Content-Type': 'application/json',
    }

    json_data = {
        'inputs': text,
        'parameters': {
            'top_k': None,
        },
    }
    response = requests.post(hf_url, headers=headers, json=json_data)

    encoded_response = json.loads(response.content.decode("utf-8"))
    label_digit = encoded_response[0]['label']
    label_score = encoded_response[0]['score']
    label_name = label_mapping.get(label_digit)
    submodel_df.at[index, 'LabelKomponente'] = label_name
    submodel_df.at[index, 'ScoreKomponente'] = label_score
    return submodel_df

# Labeln Datenpunkt Ebene -> Zero Shot mit NLI
def label_datapoint(submodel_df, index, hf_url, candidate_labels):
    # Candidate Labels sind die weiter unten spezifiierten möglichen Label des Datenpunkts
    # für eine Komponente. Diese werden mit der Hypothese verknüpft. Dann NLI mit dem Datenpunkt (Name / Description)
    hypothese = 'Der Datenpunkt beschreibt: {}.'
    text = submodel_df.at[index, "NLPText"]

    headers = {
        'Authorization': 'Bearer BWKspKrXvGhLerysCyfYISapWopuGGPTDRxAowpKsiPugTuTqNLQrSPTJEvGkOsVQLIGyBEaNHymluAgZpRClVFJdQuRgvMGIpnWBPTAxnEIZGgthUdywhaqoGIZsewN',
        'Content-Type': 'application/json',
    }

    json_data = {
        'inputs': text,
        'parameters': {
            'candidate_labels': candidate_labels,
            'hypothesis_template': hypothese
        }
    }
    response = requests.post(hf_url, headers=headers, json=json_data)
    encoded_response = json.loads(response.content.decode("utf-8"))
    #print(encoded_response)
    label_name = encoded_response['labels'][0]
    label_score = encoded_response['scores'][0]
    submodel_df.at[index, 'LabelDatenpunkt'] = label_name
    submodel_df.at[index, 'ScoreDatenpunkt'] = label_score
    return submodel_df
    
# Auslesen jedes Datenpunkts aus dem Teilmodell BACNet Datapoint. Sind alles Collections, 
# welche hier nacheinander ausgelesen werden
#def read_smc(submodel_element, aas_id, submodel_id):
def read_smc(submodel_element, submodel_id):
    values = submodel_element['value']

    for element in values:
        if element['idShort'] == 'ObjectIdentifier':
            object_identifier = element['value']
        elif element['idShort'] == 'ObjectName':
            object_name = element['value']
        elif element['idShort'] == 'ObjectType':
            object_type= element['value']
        elif element['idShort'] == 'Description':
            description = element['value']
        elif element['idShort'] == 'Units':
            unit = element['value']
        elif element['idShort'] == 'PresentValue':
            present_value = element['value']

    text = description + '; ' + object_name
    text = text.lower()      

    collection = pd.DataFrame(
        {
            #"AASId": aas_id,
            "SubmodelId": submodel_id,
            "ObjectIdentifier": object_identifier,
            "ObjectName": object_name,
            "ObjectType": object_type,
            "Description": description,
            "Unit": unit,
            "PresentValue": present_value,
            "NLPText": text,
        }, index = [0]
    )
    return collection

# Einlesen des NLP Teilmodells (ist "leer"), wird befüllt mit Inhalten der NLP Pipeline
def read_nlp_submodel():
    submodel_file = "nlp_classification_result_submodel_instanz_mit_anlage.json"
    with open(submodel_file, 'r') as file:
        data = json.load(file)
    aas = data["assetAdministrationShells"]
    submodel_for_aas = aas[0]["submodels"][0]
    #aas_submodels = aas[0]["submodels"]
    submodel = data["submodels"][0]
    return submodel, submodel_for_aas

# Für jeden Datenpunkt des BACNet Teilmodells wird eine Collection mit den Ergebnisse
# im NLP Teilmodell angelegt
# Geht das schöner?
def create_nlp_submodel_collections(submodel_df):
    all_classified_datapoint_collections = []
    for index, row in submodel_df.iterrows():

        #print(row)

        nlp_submodel, submodel_for_aas = read_nlp_submodel()
        collection_classified_datapoint = nlp_submodel["submodelElements"][0]
        collection_classified_datapoint['idShort'] = 'ClassifiedDatapoint-' + row['ObjectName']
        collection_classified_datapoint['value'][0]['value'][0]['value'][0]['value'] = row['LabelGrundfunktion']
        collection_classified_datapoint['value'][0]['value'][0]['value'][1]['value'] = row['ScoreGrundfunktion']
        collection_classified_datapoint['value'][1]['value'][0]['value'][0]['value'] = row['LabelZweiteEbene']
        collection_classified_datapoint['value'][1]['value'][0]['value'][1]['value'] = row['ScoreZweiteEbene']
        collection_classified_datapoint['value'][2]['value'][0]['value'][0]['value'] = row['LabelKomponente']
        collection_classified_datapoint['value'][2]['value'][0]['value'][1]['value'] = row['ScoreKomponente']
        collection_classified_datapoint['value'][3]['value'][0]['value'][0]['value'] = row['LabelDatenpunkt']
        collection_classified_datapoint['value'][3]['value'][0]['value'][1]['value'] = row['ScoreDatenpunkt']
        
        collection_classified_datapoint['value'][4]['value'][0]['value'][0]['value'] = row['LabelAnlage']
        collection_classified_datapoint['value'][4]['value'][0]['value'][1]['value'] = row['ScoreAnlage']
        
        collection_classified_datapoint['value'][5]['value'] = row['NLPText']
        #collection_classified_datapoint['value'][5]['value'][0]['value'][1]['value'] = row['AIDRelation']
        collection_classified_datapoint['value'][7]['value'] = row['ObjectName']
        collection_classified_datapoint['value'][8]['value'] = row['ObjectType']
        collection_classified_datapoint['value'][9]['value'] = row['Description']

        all_classified_datapoint_collections.append(collection_classified_datapoint)
    nlp_submodel, submodel_for_aas = read_nlp_submodel()
    nlp_submodel["submodelElements"] = all_classified_datapoint_collections

    #return nlp_submodel, submodel_for_aas
    return nlp_submodel
# Auslesen der Verwaltungsschale, die an die NLP Pipeline übergeben wird
def read_aas(aas_file):
    #with open(aas_file, 'r') as file:
    #    predict_data = json.load(file)
    predict_data = aas_file

    # Folgenden Zeilen nicht benötigt bei Submodel
    #predict_aas = predict_data["assetAdministrationShells"]
    #predict_aas_submodels = predict_aas[0]["submodels"]
    #predict_submodels_ids = []
    #for submodel in predict_aas_submodels:
        #predict_submodels_ids.append(submodel["keys"][0]["value"])
    # Abspeichern aller Teilmodelle
    #predict_submodels = predict_data["submodels"]
    #number_of_submodels = len(predict_submodels)

    submodel_df = pd.DataFrame(
        columns= [
            #"AASId",
            "SubmodelId",
            "ObjectIdentifier",
            "ObjectName",
            "ObjectType",
            "Description",
            "Units",
            "PresentValue",
            "LabelGrundfunktion",
            "ScoreGrundfunktion",
            "LabelZweiteEbene",
            "ScoreZweiteEbene", 
            "LabelKomponente",
            "ScoreKomponente",
            "LabelDatenpunkt",
            "ScoreDatenpunkt",
        ]
    )
    #aas_id = predict_aas[0]["identification"]["id"]
    """
    for submodel in predict_submodels:
        submodel_id = submodel["identification"]["id"]
        submodel_semantic_id_dict = submodel['semanticId']
        submodel_semantic_id = submodel_semantic_id_dict['keys'][0]['value']
        # Wenn Semantic ID des Teilmodells = diesem ist, starte nlp
        if submodel_semantic_id == 'https://th-koeln.de/gart/vocabulary/SubmodelBACnetDatapointInformation':
            submodel_elements = submodel["submodelElements"]
            number_datapoints = len(submodel_elements)
            for submodel_element in submodel_elements:
                collection = read_smc(submodel_element, aas_id, submodel_id)
                submodel_df = pd.concat([submodel_df, collection], ignore_index=True)
    """
    submodel_id = predict_data["identification"]["id"]
    submodel_semantic_id_dict = predict_data['semanticId']
    submodel_semantic_id = submodel_semantic_id_dict['keys'][0]['value']
    # Wenn Semantic ID des Teilmodells = diesem ist, starte nlp
    if submodel_semantic_id == 'https://th-koeln.de/gart/vocabulary/SubmodelBACnetDatapointInformation':
        submodel_elements = predict_data["submodelElements"]
        number_datapoints = len(submodel_elements)
        for submodel_element in submodel_elements:
            #collection = read_smc(submodel_element, aas_id, submodel_id)
            collection = read_smc(submodel_element, submodel_id)
            submodel_df = pd.concat([submodel_df, collection], ignore_index=True)
    # URL für Inference Endpoint Datenpunkt
    hf_url_datenpunkt = 'https://lvrwzsv3ieuogb1e.eu-west-1.aws.endpoints.huggingface.cloud'    

    # Mögliche Label aller Komponente
    # -> erweitern wenn zu ende gelabelt
    #Wärme verteilen
    labelDruckhaltestation = ['Messwert', 'Störmeldung']
    labelHeizkreisAllgemein = ['Alarmmeldung', 'Anforderung', 'Ausschaltzeit', 'Device-Description', 'Einschaltzeit', 
        'Externe Vorrangschaltung', 'Grenzwert Frost', 'Grenzwert Temperatur', 'Heizkurve', 
        'Hysterese Frostschutz', 'Hysterese Heizkreis', 'Messwert Außentemperatur', 'Messwert Feuchte', 
        'Messwert Leistung', 'Messwert Temperatur', 'Messwert Volumenstrom', 'Messwert Windgeschwindigkeit',
        'Messwert Wärmeleistung', 'Nachlaufdauer Klappe Wärmetauscher', 'Nachtabsenkung Tage', 
        'Quittierung', 'Reglerparameter', 'Restlaufzeit Nutzzeitverlängerung', 'Rückmeldung Aufheizbetrieb',
        'Rückmeldung Betrieb', 'Rückmeldung Betriebsart', 'Rückmeldung Betriebsstunden', 
        'Rückmeldung Frostschutz', 'Rückmeldung Frostschutz Handschalter', 'Rückmeldung Handschaltung',
        'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Nachtabsenkung', 
        'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Regelabweichung', 'Rückmeldung Restwärmeoptimierung',
        'Rückmeldung Tagbetrieb', 'Rückmeldung Zeitprogramm', 'Schaltbefehl Anlage', 'Schaltbefehl Betriebsart',
        'Schaltbefehl Gleitendes Schalten', 'Schaltbefehl Nachtabsenkung', 'Schaltbefehl Nutzzeitverlängerung', 
        'Schaltbefehl Optimierung', 'Schaltbefehl Start Stop Optimierung', 'Schaltbefehl Zeitprogramm', 
        'Sollwert Abschalten Stützbetrieb', 'Sollwert Aufheizzeit', 'Sollwert Außentemperatur', 
        'Sollwert Außentemperatur Abschalten Heizung', 'Sollwert Außentemperatur Einschalten Heizung', 
        'Sollwert Außentemperatur Start StoppAktiv', 'Sollwert Delta T Vorlauf Rücklauf', 'Sollwert Economy', 
        'Sollwert Ferien', 'Sollwert Frostschutz', 'Sollwert Grenztemperatur Start Stopp', 
        'Sollwert Hysterese Aufheizbetrieb', 'Sollwert Hysterese Nachtabsenkung', 'Sollwert Komfort', 
        'Sollwert Laufzeit Blockierschutz', 'Sollwert Maximale Aufheizzeit', 'Sollwert Minimale Außentemperatur', 
        'Sollwert Nacht', 'Sollwert Nachtabsenkung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Schutzbetrieb', 
        'Sollwert Speicherfähigkeit', 'Sollwert StandBy Nacht', 'Sollwert StandBy Tag', 
        'Sollwert Stützbetrieb Nacht', 'Sollwert Stützbetrieb Nacht Hysterese', 'Sollwert Stützbetrieb Tag Hysterese', 
        'Sollwert Stützbetrieb-Tag', 'Sollwert Tag', 'Sollwert Temperatur', 'Sollwert Temperatur Start Aufheizen', 
        'Sollwert Zeitkonstante', 'Sollwert Überhöhung Hydraulische Weiche', 'Sollwert Überhöhung Wärmeanforderung', 
        'Sollwertverschiebung', 'Stellbefehl', 'Stunden Sollwert Außentemperatur', 'Störmeldung', 
        'Stützbetrieb Nacht Erreicht', 'Stützbetrieb Tag Erreicht']
    labelHeizkurve = ['Aufheizbetrieb', 'Außentemperatur X1', 'Außentemperatur X2', 'Außentemperatur X3', 
        'Außentemperatur X4', 'Messwert Außentemperatur', 'Rückmeldung Managementbedieneinrichtung', 
        'Rückmeldung Verschiebung', 'Sollwert', 'Sollwert Fußpunkt', 'Sollwert Krümmung', 'Sollwert X1', 
        'Sollwert X2', 'Sollwert X3', 'Sollwert X4', 'Sollwert Y1', 'Sollwert Y2', 'Sollwert Y3', 
        'Sollwert Y4', 'Sollwertverschiebung', 'Steilheit', 'Stützbetrieb X1', 'Stützbetrieb X2', 
        'Stützbetrieb X3', 'Stützbetrieb X4', 'Stützbetrieb Y1', 'Stützbetrieb Y2', 'Stützbetrieb Y3', 
        'Stützbetrieb Y4', 'Stützpunkt X1', 'Stützpunkt X2', 'Stützpunkt X3', 'Stützpunkt X4', 
        'Stützpunkt Y1', 'Stützpunkt Y2', 'Stützpunkt Y3', 'Stützpunkt Y4']
    labelKMZ = ['Messwert Kälteleistung', 'Messwert Kältemenge', 'Messwert Rücklauftemperatur', 
        'Messwert Volumen', 'Messwert Volumenstrom', 'Messwert Vorlauftemperatur']
    labelRaum = ['Fensteranteil', 'Freigabe Externer Sollwert', 'Freigabe Heizung', 'Freigabe Optimum-Stopp', 
        'Freigabe Raumkorrektur', 'Freigabe Stellantrieb', 'Freigabe Stützbetrieb Nacht', 
        'Freigabe Stützbetrieb Nacht Ventil', 'Freigabe Stützbetrieb Tag', 'Freigabe Stützbetrieb Tag Ventil', 
        'Freigabe Zeitprogramm', 'Messwert CO2', 'Messwert Raumtemperatur', 'Präsenzmelder', 
        'Rückmeldung Absenkbetrieb', 'Rückmeldung Aufheizbetrieb', 'Rückmeldung Handschaltung', 
        'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Normalbetrieb', 'Schaltbefehl Raumkorrektur', 
        'Schaltbefehl Ventil', 'Sollwert Absenkbetrieb', 'Sollwert CO3', 'Sollwert Raumkorrektur', 
        'Sollwert Raumtemperatur Nacht', 'Sollwert Raumtemperatur Normalbetrieb', 
        'Sollwert Raumtemperatur Schutzbetrieb', 'Sollwert Raumtemperatur Tag', 'Sollwert Stützbetrieb Nacht', 
        'Sollwert Stützbetrieb-Tag', 'Sollwert minimale Raumtemperatur', 'Sollwertsteller', 
        'Sollwertverschiebung', 'Stellbefehl', 'Störmeldung']
    labelRegler = ['Abtastzeit', 'Außentemperatur Errechnet', 'D-Anteil', 'I-Anteil', 'P-Anteil', 'Proportionalband', 'Reglerausgang', 'Reglereingang', 'Reset', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Regelabweichung', 'Schaltbefehl', 'Sollwert Nachstellzeit', 'Sollwert Regler', 'Sollwert Regler Max', 'Sollwert Regler Min', 'Stellbefehl', 'Störmeldung', 'Verschiebung']
    labelÜbertrager = ['Heizkörperexponent', 'Rückmeldung Heizdecke', 'Rückmeldung Ventil-Zone', 'Schaltbefehl Heizdecke', 'Schaltbefehl Ventil Zone', 'Vorregelung Deckenstrahlplatten Messwert Temperatur', 'Vorregelung Deckenstrahlplatten Sollwert', 'Vorregelung Deckenstrahlplatten Status', 'Vorregelung Deckenstrahlplatten Stellbefehl', 'Vorregelung Deckenstrahlplatten Temperatur Max', 'Vorregelung Deckenstrahlplatten Temperatur Min', 'Vorregelung Deckenstrahlplatten Temperaturdifferenz', 'Vorregelung Deckenstrahlplatten Zeit']
    labelVentil = ['Laufzeit Ventil', 'Laufzeit-3-Punkt-Antrieb', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sicherheit', 'Sollwert', 'Sollwert Handschaltung', 'Sollwert Mischventil', 'Sollwert Stellsignal Max', 'Sollwert Stellsignal Min', 'Stellbefehl', 'Stellbefehl Max', 'Stellbefehl Min', 'Stellbefehl Mischventil', 'Störmeldung']
    labelWMZ = ['Messwert Durchfluss', 'Messwert Kältemenge', 'Messwert Leistung', 'Messwert Rücklauftemperatur', 'Messwert Temperaturdifferenz', 'Messwert Volumenstrom', 'Messwert Vorlauftemperatur', 'Messwert Wärmeleistung', 'Messwert Wärmemenge', 'Messwert Wärmemenge-Energie', 'Messwert Wärmemenge-Volumen', 'Störmeldung']
    labelWWB = ['Alarmmeldung', 'Anzahl Stufen', 'Ausschalttemperatur', 'Ausschaltzeit', 'Blockierschutz', 'Einschalttemperatur', 'Einschaltzeit', 'Freigabe', 'Handschaltung Legionellen', 'Hysterese Sollwert Warmwasserbereitung', 'Legionellenschaltung Tage', 'Messwert Wassertemperatur', 'Messwert Zapftemperatur', 'Messwert Zirkulationstemperatur', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Handschaltung Auto', 'Rückmeldung Legionellenschaltung', 'Rückmeldung Legionellenschaltung Handschaltung', 'Rückmeldung Legionellenschaltung Handschaltung Auto', 'Schaltbefehl', 'Schaltbefehl Legionellenschaltung', 'Sollwert Maximiale Laufzeit Legionellen', 'Sollwert Temperatur Legionellen', 'Sollwert Warmwasserbereitung', 'Sollwert Zirkulationstemperatur', 'Sollwert Zirkulationstemperatur Legionellen', 'Stellbefehl', 'Störmeldung', 'Warnmeldung Legionellen', 'Wartungsmeldung', 'Wochenprogramm']
    labelVorlauf = ['Anhebung Vorlauftemperatur', 'Arbeitspunkt', 'Frostschutz Vorlauftemperatur', 'Messwert Vorlauftemperatur', 'Messwert Vorlauftemperatur Errechnet', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Regelabweichung', 'Schaltbefehl Dämpfung', 'Schaltbefehl Optimierung', 'Sollwert Maximale Vorlauftemperatur', 'Sollwert Minimale Vorlauftemperatur', 'Sollwert Nachtabsenkung Vorlauftemperatur', 'Sollwert Vorlauftemperatur', 'Sollwert Vorlauftemperatur Errechnet', 'Sollwertkorrektur-Vorlauftemperatur', 'Störmeldung']
    labelRücklauf = ['Arbeitspunkt', 'Grenzwert Winteranfahren', 'Messwert Rücklauftemperatur', 'Rücklauf Begrenzung', 'Rücklauftemperatur Errechnet', 'Schaltbefehl Begrenzung', 'Schaltbefehl Frostschutz', 'Sollwert Frostschutz', 'Sollwert Maximale Rücklauftemperatur', 'Sollwert Minimale Rücklauftemperatur', 'Sollwert Rücklauftemperatur', 'Sollwert Rücklauftemperatur Errechnet', 'Störmeldung']
    labelPumpe = ['Alarmmeldung', 'Anforderung', 'Anzahl Schaltungen', 'Blockierschutz', 'Freigabe', 'Hysterese Frostschutz', 'Messwert Drehzahl', 'Messwert Druck', 'Messwert Durchfluss', 'Messwert Energieverbrauch', 'Messwert Förderhöhe', 'Messwert Leistung', 'Messwert Leistungsaufnahme', 'Messwert Stromaufnahme', 'Messwert Temperatur', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Reset Wartungsintervall', 'Rückmeldung Auto', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Handschaltung Pumpe', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Zeitprogramm', 'Schaltbefehl', 'Schaltbefehl Blockierschutz', 'Schaltbefehl Wechsel Doppelpumpe', 'Schalthysterese', 'Sollwert', 'Sollwert Drehzahl', 'Sollwert Frostschutz', 'Sollwert Intervall Blockierschutz', 'Sollwert Laufzeit Blockierschutz', 'Sollwert Nachlaufzeit', 'Sollwert Nacht', 'Sollwert Pumpe Ein Außentemperatur', 'Sollwert Reset Betriebsstunden', 'Sollwert Tag', 'Stellbefehl', 'Störmeldung', 'Wartungsintervall', 'Wartungsmeldung', 'Übersteuerung']

    # Wärme speichern
    labelSpeicher = ['Ausschaltgrenzwert', 'Einschaltgrenzwert', 'Messwert Außentemperatur', 'Messwert Speichertemperatur', 'Messwert Speichertemperatur Mitte', 'Messwert Speichertemperatur Oben', 'Messwert Speichertemperatur Unten', 'Rückmeldung Handschaltung', 'Schaltbefehl', 'Schaltdifferenz', 'Sollwert Speichertemperatur', 'Sollwert Speichertemperatur Oben', 'Sollwert Speichertemperatur Unten', 'Störmeldung', 'Vorrangschaltung']

    # Wärme erzeugen
    labelBhkw = ['Blockierschutz', 'Laufzeit Nächste Wartung', 'Messwert Abgastemperatur', 'Messwert Drehzahl', 'Messwert Druck', 'Messwert Frequenz', 'Messwert Gas', 'Messwert Klappe', 'Messwert Lambda', 'Messwert Leistung', 'Messwert Spannung', 'Messwert Strom', 'Messwert Temperatur', 'Messwert Temperatur Generator', 'Messwert Wärmemenge', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Netzparallel', 'Rückmeldung Start', 'Rückmeldung Ventil', 'Rückmeldung Ölnachspeisung Aktiv', 'Schaltbefehl Anlage', 'Seriennummer', 'Sollwert Leistung', 'Stellbefehl', 'Störmeldung', 'Warnmeldung', 'Wartungsmeldung']
    labelKessel = ['Alarmmeldung', 'Anforderung', 'Anzahl Schaltungen', 'Ausschaltdifferenz', 'Blockierschutz', 'Freigabe', 'Messwert Druck', 'Messwert Gas', 'Messwert Leistung', 'Messwert Temperatur', 'Reglerparameter', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Heizperiode', 'Rückmeldung Klappe', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Modulationsgrad', 'Rückmeldung Not Aus', 'Rückmeldung Ventil', 'Rückmeldung Zeitprogramm', 'Schaltbefehl Anlage', 'Schaltbefehl Heizperiode Nach Datum', 'Schaltbefehl Heizperiode Nach Temperatur', 'Schaltbefehl Klappe', 'Schaltbefehl Sommer Monat Ein', 'Schaltbefehl Winter Monat Ein', 'Schalthysterese', 'Seriennummer', 'Sollwert Abschaltung', 'Sollwert Einschalten Sommer', 'Sollwert Kesselanzahl', 'Sollwert Laufzeit', 'Sollwert Leistung', 'Sollwert Modulation', 'Sollwert Sommer Tag', 'Sollwert Temperatur', 'Stellbefehl Anlage', 'Stellbefehl Klappe', 'Stellbefehl Ventil', 'Störmeldung', 'Warnmeldung', 'Wartungsmeldung', 'Zähler Wärmemenge', 'Übersteuerung']
    labelPelletkessel = ['Messwert Abgastemperatur', 'Messwert Außentemperatur', 'Messwert Primärluft', 'Messwert Sauerstoff', 'Messwert Sekundärluft', 'Messwert Temperatur', 'Messwert Temperatur Einschubrohr', 'Messwert-Drehzahl ', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Schaltbefehl', 'Sollwert Temperatur', 'Störmeldung']
    labelWärmepumpe = ['Blockierschutz', 'Messwert Wasserspiegel Förderbrunnen', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsbereit', 'Rückmeldung Betriebsstunden', 'Rückmeldung Blockierschutz Brunnenpumpe', 'Rückmeldung Blockierschutz Umwälzpumpe', 'Rückmeldung Handschaltung', 'Rückmeldung Umschaltventil Zu', 'Rückmeldung Umschaltventil-Auf', 'Schaltbefehl', 'Stellbefehl', 'Störmeldung', 'Zähler Strom', 'Zähler Wärmemenge']
    labelWärmeversorgerAllgemein = ['Alarmmeldung', 'Freigabe Betrieb Comfort Economy', 'Freigabe Betrieb Winter', 'Freigabe Filter', 'Freigabe Sondertageprogramm', 'Freigabe Wärmeerzeuger', 'Messwert Außentemperatur', 'Mindestausschaltzeit', 'Mindesteinschaltzeit', 'Optimierung', 'Quittierung', 'Regelparameter', 'Rückmeldung Betrieb', 'Rückmeldung Erzeuger', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe', 'Rückmeldung Sommer Winter', 'Rückmeldung Start Stopp', 'Rückmeldung Wärmeanforderung', 'Rückmeldung Zeitprogramm', 'Schaltbefehl', 'Schaltbefehl Klappe', 'Schaltbefehl Sommer Winter', 'Schaltbefehl Wärmeanforderung', 'Sollwert Außentemperatur Abschaltung Nacht', 'Sollwert Außentemperatur Abschaltung Tag', 'Sollwert Temperatur', 'Sollwert Wärmeanforderung', 'Sollwert Wärmebedarf', 'Sollwert Zeit Berechnung', 'Sollwert glt', 'Störmeldung', 'Vorrangschaltung', 'Zeitangabe', 'Zähler Gas', 'Übersteuerung']

    #Wärme beziehen
    labelFernwärme = ['Alarmmeldung', 'Anforderung', 'Blockierschutz', 'Freigabe', 'Heizkurve', 'Messwert Außentemperatur', 'Messwert Drehzahl', 'Messwert Druck', 'Messwert Leistung', 'Messwert Rücklauftemperatur', 'Messwert Rücklauftemperatur Primär', 'Messwert Rücklauftemperatur Sekundär', 'Messwert Temperatur', 'Messwert Vorlauftemperatur', 'Messwert Vorlauftemperatur Primär', 'Messwert Vorlauftemperatur Sekundär', 'Messwert-Durchfluss ', 'Offset Vorlauftemperatur', 'Reglerparameter', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe', 'Rückmeldung Pumpe', 'Rückmeldung Regelabweichung', 'Rückmeldung Ventil', 'Schaltbefehl Anlage', 'Schaltbefehl Klappe', 'Schaltbefehl Pumpe', 'Schaltbefehl Ventil', 'Sollwert Außentemperatur Ein Aus', 'Sollwert Nachlaufzeit Pumpe', 'Sollwert Nacht', 'Sollwert Rücklauftemperatur', 'Sollwert Rücklauftemperaturbegrenzung', 'Sollwert Temperatur', 'Sollwert Ventil', 'Sollwert Vorlauftemperatur', 'Sollwert Vorlauftemperaturbegrenzung', 'Sollwertverschiebung', 'Stellbefehl Pumpe', 'Stellbefehl Ventil', 'Störmeldung', 'Warnmeldung', 'Zähler']

    #Luft verteilen
    labelAuslass = ['Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Zeitverzögerung']
    labelRaumRlt = ['Alarme Zurück Gestellt', 'Alarmmeldung', 'Messwert CO2', 'Messwert Feuchte', 'Messwert Raumtemperatur', 'Rückmeldung Betrieb', 'Rückmeldung Fensterkontakt', 'Rückmeldung Handschaltung', 'Rückmeldung Kommunikation', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Präsenzmelder', 'Rückmeldung Trennwandkontakt', 'Rückmeldung Ventil', 'Schalthysterese', 'Sollwert Ausschaltverzögerung', 'Sollwert CO2 Max', 'Sollwert CO2 Min', 'Sollwert CO3', 'Sollwert Feuchte', 'Sollwert Raumtemperatur', 'Störmeldung', 'Warnmeldung Temperatur Niedrig', 'Warnmeldung-CO2-Hoch', 'Warnmeldung-Feuchte', 'Warnmeldung-Temperatur-Hoch']
    labelVsrAbluftZuluft = ['Messwert Volumenstrom', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Volumenstrom', 'Stellbefehl']
    labelVsrRaum = ['Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Stellbefehl']

    #Luft bereitstellen
    labelAbluftAllgemein = ['Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Luftqualität', 'Messwert Temperatur', 'Messwert Volumenstrom', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Stellsignal', 'Rückmeldung Zeitprogramm', 'Schaltbefehl Anlage', 'Sollwert CO2 Konzentration', 'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Temperatur', 'Sollwert Volumenstrom', 'Sollwert Zeitverzögerung', 'Stellbefehl', 'Störmeldung', 'Warnmeldung-Feuchte', 'Wartungsmeldung', 'Werkseinstellungen']
    labelFilter = ['Alarmmeldung', 'Messwert Druck', 'Störmeldung', 'Wartungsmeldung']
    labelAbluftklappe = ['Alarmmeldung', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Schaltbefehl', 'Stellbefehl', 'Störmeldung']
    labelAbluftventilator = ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlsausführkontrolle', 'Laufüberwachung', 'Messwert Druck', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Reperaturschalter', 'Rückmeldung Reset Betriebsstunden', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung', 'Wartungsmeldung']
    labelAußenluftklappe = ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückemldung Stellsignal', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Managementbedieneinrichtung', 'Schaltbefehl', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung']
    labelBefeuchter = ['Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Befeuchten', 'Stellbefehl', 'Störmeldung']
    labelErhitzer = ['Alarmmeldung Frostschutz', 'Befehlsausführkontrolle', 'Freigabe', 'Messwert Energieverbrauch', 'Messwert Leistung', 'Messwert Temperatur', 'Messwert Volumen', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Schaltbefehl Blockierschutz', 'Schaltbefehl Frostschutz', 'Sollwert Dauerfreigabe', 'Sollwert Frostschutz', 'Sollwert Laufzeit Blockierschutz', 'Sollwert Nachstellzeit', 'Sollwert Stellsignal', 'Sollwert Temperatur', 'Spühlzeit', 'Stellbefehl ', 'Stellbefehl Ventil', 'Störmeldung']
    labelReglerRlt = ['D-Anteil', 'Grenzwert Regler', 'Hysterese', 'I-Anteil', 'P-Anteil', 'Proportionalband', 'Reglerausgang', 'Reglereingang', 'Reset', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Regelabweichung', 'Schaltbefehl', 'Sollwert Nachstellzeit', 'Sollwert Regler', 'Sollwert Regler Max', 'Sollwert Regler Min', 'Stellbefehl', 'Störmeldung', 'Stützwert', 'Totzone', 'Wirksinn']
    labelFortluftklappe = ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung']
    labelGerätAllgemein = ['Alarmmeldung', 'Anforderung Tableau', 'Anlagenuhr', 'Ausschaltzeit', 'Einschaltzeit', 'Messwert Außenfeuchte', 'Messwert Außentemperatur', 'Quittierung', 'Rückmeldung Anfahrbetrieb', 'Rückmeldung Anlage Fern', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Entfeuchtung', 'Rückmeldung Freie Nachtkühlung', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Präsenzmelder', 'Rückmeldung Restlaufzeit Nutzzeitverlängerung', 'Rückmeldung Spülen', 'Rückmeldung Zeitprogramm', 'Schaltbefehl', 'Schaltbefehl Anlage', 'Schaltbefehl Anlage Fern', 'Schaltbefehl Nachtkühlung', 'Schaltbefehl Nutzzeitverlängerung', 'Schaltbefehl Quittierung', 'Schaltbefehl Tagesprogramm', 'Schaltbefehl Zeitprogramm', 'Schalthysterese', 'Sollwert Auskühlschutz', 'Sollwert Feuchte', 'Sollwert Freie Nachtkühlung', 'Sollwert Kühlbedarf', 'Sollwert Maximale Einschaltverzögerung', 'Sollwert Minimale Einschaltverzögerung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Spülzeit', 'Sollwert Wärmebedarf', 'Stellbefehl', 'Störmeldung', 'Zurücksetzten', 'Übersteuert']
    labelKlappe = ['Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung']
    labelKMZRlt = ['Messwert Kälteleistung', 'Messwert Kältemenge', 'Messwert Volumen', 'Messwert Volumenstrom']
    labelKühler = ['Alarmmeldung Frostschutz', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Kühlbedarf', 'Stellbefehl', 'Störmeldung', 'Zählwert Kältemenge']
    labelUmluft = ['Messwert Temperatur', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Störmeldung']
    labelVentilator = ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Drehzahl', 'Rückmeldung Handschaltung', 'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung', 'Wartungsmeldung']
    labelWMZRlt = ['Messwert Leistung', 'Messwert Temperaturdifferenz', 'Messwert Wärmemenge']
    labelWrg = ['Alarmmeldung', 'Alarmmeldung Frostschutz', 'Messwert Temperatur', 'Messwert Temperatur Austritt Abluft', 'Messwert Temperatur Austritt Zuluft', 'Messwert Temperatur Eintritt Abluft', 'Messwert Temperatur Eintritt Zuluft', 'Messwert Vorlauftemperatur', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Frostschutz', 'Sollwert Stellsignal', 'Sollwert Stellsignal Max', 'Sollwert Stellsignal Min', 'Stellbefehl', 'Störmeldung']
    labelZuluftAllgemein = ['Alarmmeldung', 'Alarmmeldung Frostschutz', 'Messwert Druck', 'Messwert Enthalpie', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Volumenstrom', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Ventil', 'Schaltbefehl Anlage', 'Sollwert CO2 Konzentration', 'Sollwert CO2 Konzentration Max', 'Sollwert Druck', 'Sollwert Enthalpie', 'Sollwert Feuchte', 'Sollwert Feuchte Max', 'Sollwert Feuchte Min', 'Sollwert Frostschutz', 'Sollwert Grenzwert Soll Ist-Abweichung Temperatur', 'Sollwert Temperatur', 'Sollwert Temperatur Max', 'Sollwert Temperatur Min', 'Sollwert Volumenstrom', 'Sollwert Volumenstrom Max', 'Sollwert Volumenstrom Min', 'Sollwert Zeitverzögerung', 'Störmeldung', 'Warnmeldung Temperatur Niedrig', 'Warnmeldung-Feuchte', 'Warnmeldung-Temperatur-Hoch', 'Wartungsmeldung', 'Werkseinstellungen']
    labelZuluftklappe = ['Alarmmeldung', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Schaltbefehl', 'Stellbefehl', 'Störmeldung']
    labelZuluftventilator = ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlsausführkontrolle', 'Laufüberwachung', 'Messwert Differenzdruck', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Drehzahl', 'Rückmeldung Handschaltung', 'Rückmeldung Laufüberwachung', 'Rückmeldung Managementbedieneinrichtung', 'Rückmeldung Reperaturschalter', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung', 'Wartungsmeldung']

    # Kälte erzeugen
    labelKälteanlage = ['Anforderung', 'Messwert Energieverbrauch', 'Messwert Leistung', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Schaltbefehl', 'Störmeldung']
    labelKältekreisAllgemein = ['Grenzwert Außentemperatur', 'Messwert Außentemperatur', 'Messwert Druck']
    labelKältemaschine = ['Anforderung', 'Hysterese', 'Leistungszahl', 'Messwert Druck Verdampfer', 'Messwert Druck Verflüssiger', 'Messwert Kälteleistung', 'Messwert Stromaufnahme', 'Messwert Temperatur Kaltwassereintritt', 'Messwert Temperatur Kühlwasseraustritt', 'Messwert Temperatur Kühlwassereintritt', 'Messwert Verdampfer Austritt', 'Messwert Verdampfer Eintritt', 'Messwert Verflüssiger Austritt', 'Messwert Verflüssiger Eintritt', 'Messwert Verflüssiger Temperaturniveau', 'Messwert Volumenstrom', 'Rückmeldung Aktueller-Sollwert', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Kälteleistung', 'Rückmeldung Managementbedieneinrichtung', 'Schaltbefehl', 'Sollwert Stellsignal', 'Störmeldung']
    labelKmzKälteErzeugen = ['Messwert Kälteleistung', 'Messwert Kältemenge', 'Messwert Rücklauftemperatur', 'Messwert Vorlauftemperatur']
    labelKlappeKälteErzeugen = ['Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Schaltbefehl']
    labelPumpeKälteErzeugen = ['Anforderung', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Schaltbefehl', 'Störmeldung']
    labelReglerKälteErzeugen = ['D-Anteil', 'I-Anteil', 'P-Anteil', 'Sollwert', 'Sollwert Regler Max', 'Sollwert Regler Min', 'Stellbefehl', 'Totzeit']
    labelRkw = ['Grenzwert Druck', 'Messwert Drehzahl', 'Messwert Druck', 'Messwert Leistung', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Schaltbefehl', 'Sollwert Stellsignal', 'Störmeldung']
    labelVentilKälteErzeugen = ['Freigabe Sollwert', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Stellbefehl']
    labelVorlaufKälteErzeugen = ['Messwert Vorlauftemperatur', 'Sollwert Vorlauftemperatur']
    labelWmzKälteErzeugen = ['Messwert Wärmemenge', 'Störmeldung']
    labelRücklaufKälteErzeugen = ['Messwert Rücklauftemperatur', 'Sollwert Rücklauftemperatur']

    # Kälte verteilen
    labelFu = ['Frequenzumrichter']
    labelKältekreisAllgemeinKälteVerteilen = ['Messwert Druck', 'Sollwert Druck', 'Störmeldung']
    labelKältemaschinenAnschluss = ['Massenstrom', 'Messwert Rücklauftemperatur', 'Messwert Vorlauftemperatur', 'Sollwertabweichung', 'Störmeldung']
    labelKlappeKälteVerteilen = ['Klappe', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Schaltbefehl', 'Störmeldung']
    labelPumpeKälteVerteilen = ['Anforderung', 'Pumpe', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Betriebsstunden', 'Rückmeldung Handschaltung', 'Rückmeldung Managementbedieneinrichtung', 'Schaltbefehl', 'Stellbefehl', 'Störmeldung']
    labelRaumKälteVerteilen = ['Alarmmeldung', 'Messwert Raumtemperatur', 'Raum', 'Rückmeldung Managementbedieneinrichtung', 'Sollwert maximale Raumtemperatur', 'Sollwert minimale Raumtemperatur', 'Störmeldung']
    labelReglerKälteVerteilen = ['D-Anteil', 'I-Anteil', 'P-Anteil', 'Regelgröße', 'Sollwert', 'Sollwert Regler Max', 'Sollwert Regler Min']
    labelUmluftkühlgerät = ['Umluftkühlgerät']
    labelVentilKälteVerteilen = ['Rückmeldung Handschaltung', 'Sollwert Mischventil', 'Stellbefehl', 'Störmeldung']
    labelVorlaufKälteVerteilen = ['Grenzwert Vorlauftemperatur', 'Messwert Vorlauftemperatur', 'Sollwert Vorlauftemperatur', 'Vorlauf']
    labelWmzKälteVerteilen = ['Messwert Kälteleistung', 'Messwert Kältemenge', 'Messwert Rücklauftemperatur', 'Messwert Volumenstrom', 'Messwert Vorlauftemperatur', 'Schaltbefehl', 'Störmeldung']
    labelRücklaufKälteVerteilen = ['Messwert Rücklauftemperatur']


    # Alte Version
    """    
    labelBeziehen = ['Alarmmeldung', 'Anforderung', 'Messwert Außentemperatur', 'Betriebsstunden Pumpe', 'Grenzwert Vorlauftemperatur Sekundär', 'Sollwert Maximale Vorlauftemperatur', 'Sollwert Minimale Vorlauftemperatur', 'Offset Vorlauftemperatur',
        'Regler', 'Messwert Rücklauftemperatur Primär', 'Messwert Rücklauftemperatur Sekundär', 'Rückmeldung Handschaltung Ventil', 'Rückmeldung Handschaltung Klappe', 'Rückmeldung Betriebsart', 'Rückmeldung Ventil Rücklauf',
        'Sollwert Außentemperatur Maximal Tag', 'Sollwert Nachlaufzeit Pumpe', 'Schaltbefehl Anlage', 'Schaltbefehl Pumpe', 'Sollwert Vorlauftemperatur', 'Stellbefehl Ventil', 'Störmeldung', 'Messwert Vorlauftemperatur Sekundär',
        'Zähler', 'Messwert Vorlauftemperatur Primär', 'Grenzwert Rücklauftemperatur Sekundär', 'Rückmeldung Handschaltung Fernwärme', 'Rückmeldung Stellsignal']
    labelSpeichern = ['Externe Vorrangschaltung Aktiv', 'Rückmeldung Zeitplan', 'Sollwert Maximale Hysterese Speichertemperatur', 'Sollwert Speichertemperatur', 'Sollwert Speichertemperatur Unten', 'Messwert Speichertemperatur', 'Messwert Speichertemperatur Mitte',
        'Messwert Speichertemperatur Oben', 'Messwert Speichertemperatur Unten', 'Störmeldung', 'Rückmeldung Zeitplan']
    labelKessel = ['Anforderung', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Druck', 'Freigabe', 'Messwert Temperatur', 'Regler', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Klappe', 'Rückmeldung Stellsignal',
        'Rückmeldung Handschaltung', 'Rückmeldung Leistung', 'Rückmeldung Not Aus', 'Schaltbefehl Not Aus', 'Sollwert Temperatur', 'Sollwert Wartezeit', 'Sollwert Leistung', 'Schaltbefehl Anlage', 'Stellbefehl Anlage', 'Störmeldung', 'Überhöhung Kesselanlage',
        'Wartungsmeldung', 'Sollwert Einschaltverzögerung', 'Sollwert Abschaltung', 'Schaltbefehl Klappe']
    labelBhkw = ['Betriebsstunden', 'Laufzeit Nächste Wartung', 'Messwert Abgastemperatur', 'Messwert Gasverbrauch', 'Messwert Spannung', 'Messwert Strom', 'Messwert Temperatur Generator', 'Rückmeldung Ölnachspeisung Aktiv',
        'Rückmeldung Start', 'Rückmeldung Handschaltung', 'Rückmeldung Batterie', 'Schaltbefehl Anlage', 'Störmeldung', 'Warnmeldung', 'Wartungsmeldung', 'Rückmeldung Betrieb']
    labelWärmepumpe = ['Rückmeldung Handschaltung Brunnenpumpe', 'Rückmeldung Betriebsbereit', 'Rückmeldung Betriebsbereit', 'Rückmeldung Blockierschutz Umwälzpumpe', 'Rückmeldung Blockierschutz Brunnenpumpe', 'Rückmeldung Umschaltventil Zu',
        'Störmeldung', 'Zähler-Volumenstrom-Förderbrunnen']
    labelPelletkessel = ['Rückmeldung Schnecke Leer', 'Rückmeldung Betrieb', 'Messwert Außentemperatur', 'Messwert Primärluft', 'Restsauerstoff', 'Messwert Temperatur Einschubrohr']
    labelPumpe = ['Anzahl-Schaltungen', 'Betriebsstunden', 'Messwert Durchfluss', 'Messwert Energieverbrauch', 'Messwert Leistungsaufnahme', 'Messwert Stromaufnahme', 'Messwert Drehzahl', 'Reset Betriebsstunden', 'Rückmeldung Handschaltung Pumpe',
        'Rückmeldung Betrieb', 'Schaltbefehl', 'Schaltbefehl Blockierschutz', 'Sollwert Frostschutz', 'Sollwert Laufzeit Blockierschutz', 'Sollwert Nacht', 'Sollwert Nachlaufzeit', 'Sollwert Tag', 'Status Übersteuern Ein', 'Störmeldung', 'Wartungsintervall']
    labelVentil = ['Handschaltung', 'Laufzeit 3 Punkt Antrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Sollwert Stellsignal Min', 'Sollwert Stellsignal Max', 'Stellbefehl', 'Störmeldung', 'Stellbefehl Max', 'Stellbefehl Min',
        'Sollwert Mischventil', 'Laufzeit Ventil']
    labelRaum = ['Freigabe Heizung', 'Freigabe Raumkorrektur', 'Freigabe Stützbetrieb Nacht Ventil', 'Freigabe Stützbetrieb', 'Freigabe Stützbetrieb Tag Ventil', 'Freigabe Stellantrieb', 'Freigabe Zeitprogramm', 'Messwert Raumtemperatur',
        'Rückmeldung Normalbetrieb', 'Rückmeldung Ventil Handschaltung', 'Schaltbefehl Raumkorrektur', 'Sollwert Raumkorrektur', 'Sollwert Raumtemperatur Tag', 'Sollwert Raumtemperatur Nacht', 'Sollwert minimale Raumtemperatur',
        'Sollwertverschiebung', 'Sollwert Stützbetrieb Tag', 'Sollwert Stützbetrieb Nacht', 'Sollwert Aufheizbetrieb', 'Stellbefehl', 'Aktivierung Raumoptimierung', 'Rückmeldung Aufheizbetrieb', 'Rückmeldung Absenkbetrieb']
    labelVorlauf = ['Anhebung Vorlauftemperatur', 'Messwert Vorlauftemperatur', 'Sollwert Vorlauftemperatur', 'Sollwert Maximale Vorlauftemperatur', 'Sollwert Minimale Vorlauftemperatur', 'Sollwert Nachtabsenkung Vorlauftemperatur',
       'Störmeldung', 'Rückmeldung Sollwertabweichung Vorlauftemperatur', 'Sollwertkorrektur Vorlauftemperatur']
    labelRücklauf = ['Messwert Rücklauftemperatur', 'Sollwert Maximale Rücklauftemperatur', 'Sollwert Minimale Rücklauftemperatur', 'Sollwert Rücklauftemperatur', 'Rohrheizung']
    labelHeizkreisAllgemein = ['Alarmmeldung', 'Aktuelle Leistung', 'Grenzwert Frost', 'Heizkurve', 'Messwert Außentemperatur', 'Regler', 'Rückmeldung Nutzzeitverlängerung', 'Schaltbefehl Anlage', 'Schaltbefehl Nutzzeitverlängerung',
        'Schaltbefehl Nachtabsenkung', 'Sollwert Maximale Aufheizzeit', 'Sollwert Aufheizzeit', 'Sollwert Nachtabsenkung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Speicherfähigkeit', 'Sollwert Stützbetrieb Tag', 'Sollwert Überhöhung Hydraulische Weiche',
        'Stützbetrieb Nacht Erreicht', 'Warmwasserbereitung', 'Parallelverschiebung', 'Rückmeldung Tagbetrieb', 'Störmeldung', 'Wärmemengenzähler', 'Sollwert Minimale Außentemperatur', 'Sollwert Außentemperatur', 'Rückmeldung Betriebsart',
        'Rückmeldung Zeitplan', 'Rückmeldung Regelabweichung', 'Sollwert Abschalten Stützbetrieb', 'Schaltbefehl Start Stop Optimierung', 'Schaltbefehl Gleitendes Schalten', 'Schaltbefehl Zeitprogramm']
    labelAbluftAllgemein = ['Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Luftqualität', 'Messwert Volumenstrom', 'Rückmeldung Handschaltung', 'Rückmeldung Nutzzeitverlängerung',
        'Rückmeldung Ventil', 'Rückmeldung Zeitplan', 'Schaltbefehl Anlage', 'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Temperatur', 'Sollwert CO2 Konzentration', 'Sollwert Volumenstrom', 'Störmeldung',
        'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch', 'Warnmeldung Temperatur Niedrig', 'Wartungsmeldung']
    labelAbluftventilator = ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlausführungskontrolle', 'Betriebsstunden', 'Messwert Differenzdruck', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Rückmeldung Nutzzeitverlängerung',
        'Rückmeldung Handschaltung', 'Rückmeldung Reperaturschalter', 'Rückmeldung Betrieb', 'Rückmeldung Zeitplan', 'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert FU', 'Stellbefehl', 'Störmeldung']
    labelZuluftventilator = ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlausführungskontrolle', 'Betriebsstunden', 'Messwert Differenzdruck', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Rückmeldung Drehzahl',
        'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Handschaltung', 'Rückmeldung Reperaturschalter', 'Rückmeldung Stellsignal', 'Rückmeldung Betrieb', 'Rückmeldung Zeitplan', 'Rückmeldung Laufüberwachung',
        'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung', 'Wartungsmeldung']
    labelZuluftAllgemein = ['Alarmmeldung Frostschutz', 'Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Luftqualität', 'Messwert Volumenstrom', 'Rückmeldung Handschaltung',
        'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Ventil', 'Rückmeldung Zeitplan', 'Rückmeldung Grenzwert Soll Ist Abweichung Temperatur', 'Sollwert Grenzwert Soll Ist Abweichung Temperatur', 'Schaltbefehl Anlage',
        'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Feuchte Max', 'Sollwert Feuchte Min', 'Sollwert Frostschutz', 'Sollwert Temperatur', 'Sollwert Temperatur Min', 'Sollwert Temperatur Max', 'Sollwert CO2-Konzentration',
        'Sollwert CO2-Konzentration Max', 'Sollwert Volumenstrom', 'Sollwert Volumenstrom Max', 'Sollwert Volumenstrom Min', 'Störmeldung', 'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch',
        'Warnmeldung Temperatur Niedrig', 'Wartungsmeldung']
    labelKlappe = ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Störmeldung', 'Stellbefehl', 'Sollwert Stellsignal']
    labelBefeuchter = ['Rückmeldung Betrieb', 'Betriebsstunden', 'Sollwert Befeuchten', 'Stellbefehl', 'Störmeldung', 'Schaltbefehl']
    labelEntrauchung = ['Rückmeldung Betrieb', 'Wartungsmeldung', 'Störmeldung', 'Schaltbefehl']
    labelErhitzer = ['Alarmmeldung', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Durchfluss', 'Messwert Energieverbrauch', 'Messwert Leistungsaufnahme', 'Messwert Rücklauftemperatur', 'Messwert Stromaufnahme', 'Messwert Vorlauftemperatur', 'Messwert Drehzahl', 'Reset Betriebsstunden', 'Rückmeldung Handschaltung Pumpe', 'Rückmeldung Handschaltung Ventil', 'Rückmeldung Betrieb', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Schaltbefehl Blockierschutz', 'Schaltbefehl Frostschutz', 'Sollwert Frostschutz', 'Sollwert Laufzeit Blockierschutz', 'Sollwert Nacht', 'Sollwert Nachlaufzeit', 'Sollwert Dauerfreigabe', 'Sollwert Tag', 'Status Übersteuern-Ein', 'Stellbefehl Ventil', 'Störmeldung', 'Wartungsintervall', 'Wartungsmeldung', 'Grenzwert Rücklauftemperatur']
    labelFilter = ['Messwert Druck', 'Wartungsmeldun -Abluft', 'Wartungsmeldung Zuluft', 'Wartungsmeldung Fortluft', 'Wartungsmeldung Außenluft', 'Wartungsmeldung Filter', 'Störmeldung']
    labelGerätAllgemein = ['Alarmmeldung', 'Anforderung Tableau', 'Messwert Außentemperatur', 'Sollwert Kühlbedarf', 'Schaltbefehl Anlage', 'Übersteuert', 'Rückmeldung Anfahrbetrieb', 'Rückmeldung Batterie', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Quittierung', 'Rückmeldung Freie Nachtkühlung', 'Rückmeldung Ferienprogramm', 'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Restlaufzeit Nutzzeitverlängerung', 'Rückmeldung Spülen', 'Schaltbefehl Nachtkühlung', 'Schaltbefehl Optimierte Luftqualität', 'Schaltbefehl Tagesprogramm', 'Schaltbefehl Nutzzeitverlängerung', 'Sollwert Feuchte', 'Sollwert Spülzeit', 'Sollwert Freie-Nachtkühlung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Wärmebedarf', 'Sollwert Maximale Einschaltverzögerung', 'Störmeldung', 'Rückmeldung Anlage Fern', 'Schaltbefehl Anlage Fern']
    labelKühler = ['Alarm Frostschutz', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Rücklauftemperatur', 'Messwert Vorlauftemperatur', 'Rückmeldung Klappe Auf', 'Rückmeldung Betrieb', 'Rückmeldung Stellsignal', 'Sollwert Kühlbedarf', 'Stellbefehl Ventil', 'Zählwert Kühlwasser', 'Zählwert Kältemenge']
    labelRaumRlt = ['Alarmmeldung', 'Alarme Zurück Gestellt', 'Betriebsmeldung Präsenzmelder', 'Messwert Feuchte', 'Messwert CO2', 'Messwert Raumtemperatur', 'Rückmeldung Betrieb', 'Rückmeldung Ventil', 'Rückmeldung Klappe Auf', 'Rückmeldung Kommunikation', 'Sollwert Ausschaltverzögerung', 'Sollwert Einschaltverzögerung', 'Sollwert CO2', 'Sollwert CO2 Max', 'Sollwert Feuchte', 'Sollwert Raumtemperatur', 'Störmeldung', 'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch', 'Warnmeldung Temperatur Niedrig']
    labelUmluft = ['Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Schaltbefehl', 'Stellbefehl', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung']
    labelVsr = ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung']
    labelWrg = ['Alarmmeldung', 'Messwert Temperatur Austritt Zuluft', 'Messwert Temperatur Eintritt Zuluft', 'Messwert Temperatur Eintritt Abluft', 'Messwert Temperatur Austritt Abluft', 'Messwert Vorlauftemperatur', 'Pumpe', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Frostschutz', 'Sollwert Stellsignal', 'Sollwert Stellsignal Min', 'Sollwert Stellsignal Max', 'Stellbefehl', 'Stellbefehl WRG Bypass', 'Störmeldung']
    """
    # For Schleife für jeden Datenpunkt des BACnet Teilmodells
    # For Schleife, da Endpoints als CPU und nicht GPU ausgeführt sind
    # Wenn GPU dann auch Batches möglivh (4, 8, 12 etc.), bei CPUs ist einzeln schneller
    label_mapping_wv = {
        'LABEL_0': 'Wärme beziehen',
        'LABEL_1': 'Wärme erzeugen',
        'LABEL_2': 'Wärme speichern',
        'LABEL_3': 'Wärme verteilen'
    }
    label_mapping_lv = {
        'LABEL_0': 'Luft bereitstellen',
        'LABEL_1': 'Luft verteilen'
    }
    label_mapping_mv = {
        'LABEL_0': 'Medien bereitstellen',
        'LABEL_1': 'Medien entsorgen',
        'LABEL_2': 'Medien speichern',
        'LABEL_3': 'Medien verteilen'
    }
    label_mapping_kv = {
        'LABEL_0': 'Kälte erzeugen',
        'LABEL_1': 'Kälte speichern',
        'LABEL_2': 'Kälte verteilen'
    }
    label_mapping_we = {
        'LABEL_0': 'BHKW',
        'LABEL_1': 'Kessel',
        'LABEL_2': 'Pelletkessel',
        'LABEL_3': 'Wärmepumpe',
        'LABEL_4': 'Wärmeversorger allgemein'
    }
    label_mapping_wärme_verteilen = {
        'LABEL_0': 'Druckhaltestation',
        'LABEL_1': 'Heizkreis allgemein',
        'LABEL_2': 'Heizkurve',
        'LABEL_3': 'Kältemengenzähler',
        'LABEL_4': 'Pumpe',
        'LABEL_5': 'Raum',
        'LABEL_6': 'Regler',
        'LABEL_7': 'Rücklauf',
        'LABEL_8': 'Übertrager',
        'LABEL_9': 'Ventil',
        'LABEL_10': 'Vorlauf',
        'LABEL_11': 'Wärmengenzähler',
        'LABEL_12': 'Warmwasserbereitung'
    }
    label_mapping_lb = {
        'LABEL_0': 'Abluft allgemein',
        'LABEL_1': 'Abluftfilter',
        'LABEL_2': 'Abluftklappe',
        'LABEL_3': 'Abluftventilator',
        'LABEL_4': 'Außenluftfilter',
        'LABEL_5': 'Außenluftklappe',
        'LABEL_6': 'Befeuchter',
        'LABEL_7': 'Erhitzer',
        'LABEL_8': 'Filter',
        'LABEL_9': 'Fortluftklappe',
        'LABEL_10': 'Gerät allgemein',
        'LABEL_11': 'Kältemengenzähler',
        'LABEL_12': 'Klappen allgemein',
        'LABEL_13': 'Kühler',
        'LABEL_14': 'Regler',
        'LABEL_15': 'Umluft',
        'LABEL_16': 'Ventilator',
        'LABEL_17': 'Wärmemengenzähler',
        'LABEL_18': 'Wärmerückgewinnung',
        'LABEL_19': 'Zuluft allgemein',
        'LABEL_20': 'Zuluftfilter',
        'LABEL_21': 'Zuluftklappe',
        'LABEL_22': 'Zuluftventilator' 
    }
    label_mapping_luft_verteilen = {
        'LABEL_0': 'Auslass',
        'LABEL_1': 'Raum',
        'LABEL_2': 'Volumenstromregler Abluft',
        'LABEL_3': 'Volumenstromregler Raum',
        'LABEL_4': 'Volumenstromregler Zuluft'
    }
    label_mapping_ke = {
        'LABEL_0': 'Kälteanlage',
        'LABEL_1': 'Kältekreis allgemein',
        'LABEL_2': 'Kältemaschine',
        'LABEL_3': 'Kältemengenzähler',
        'LABEL_4': 'Klappe',
        'LABEL_5': 'Pumpe',
        'LABEL_6': 'Rückkühlwerk',
        'LABEL_7': 'Regler',
        'LABEL_8': 'Rücklauf',
        'LABEL_9': 'Ventil',
        'LABEL_10': 'Vorlauf',
        'LABEL_11': 'Wärmengenzähler'
    }
    label_mapping_kälte_verteilen = {
        'LABEL_0': 'Frequenzumrichter',
        'LABEL_1': 'Kältekreis allgemein',
        'LABEL_2': 'Kältemaschinenanschluss',
        'LABEL_3': 'Klappe',
        'LABEL_4': 'Pumpe',
        'LABEL_5': 'Raum',
        'LABEL_6': 'Regler',
        'LABEL_7': 'Rücklauf',
        'LABEL_8': 'Umluftkühlgerät',
        'LABEL_9': 'Ventil',
        'LABEL_10': 'Vorlauf',
        'LABEL_11': 'Wärmemengenzähler'
    }
    label_mapping_sichern = {
        'LABEL_0': 'Brandmeldeanlage',
        'LABEL_1': 'Brandschutzklappe',
        'LABEL_2': 'Einbruchmeldeanlage',
        'LABEL_3': 'Eintrauchung Ventilator',
        'LABEL_4': 'Feuerlöschanlage',
        'LABEL_5': 'Gaswarnanlage',
        'LABEL_6': 'Notruf',
        'LABEL_7': 'Rauchmeldeanlage'
    }

    # Alte Modelle für Medien, deswegen kein Mapping von Zahlen auf Strings
    label_mapping_mb = {
        "BereitstellungAllgemein": "Bereitstellung allgemein", 
        "Dosieranlage": 'Dosieranlage',
        "Entgasung": 'Entgasung',
        "Enthärtung": 'Enthärtung',
        "Entsalzung": 'Entsalzung',
        "Frischwassermodul": 'Frischwassermodul',
        "Kraftstoffreinigung": 'Kraftstoffreinigung',
        "Nachfüllstation": 'Nachfüllstation',
        "Präsenzmelder": 'Präsenzmelder',
        "Regler": 'Regler',
        "ThermischeDesinfektion": 'Thermische Desinfektion',
        "Wasseraufbereitung": 'Wasseraufbereitung'
    }
    label_mapping_medien_verteilen = {
        "Druckhaltestation": 'Druckhaltestation',
        "Hygienespülung": 'Hygienespülung',
        "Kraftstoffpumpe": 'Kraftstoffpumpe',
        "Rohrbegleitheizung": 'Rohrbegleitheizung',
        "Ventil": 'Ventil',
        "Wasserzähler": 'Wasserzähler',
        "ZirkulationAllgemein": 'Zirkulation allgemein',
        "Zirkulationspumpe": 'Zirkulationspumpe'
    }
    label_mapping_me = {
        "Drainage": 'Drainage',
        "Fettabscheider": 'Fettabscheider',
        "Hebeanlage": 'Hebeanlage',
        "NeutralisationKondensat": 'Neutralisation Kondensat',
        "Regenwasserpumpe": 'Regenwasserpumpe',
        "Schmutzwasserpumpe": 'Schmutzwasserpumpe',
        "WCAbwasser:": 'WC Abwasser'
    }
    
    submodel_df = label_grundfunktion(submodel_df)
    for index, row in submodel_df.iterrows():
        #print(row)

        if submodel_df.at[index, 'LabelGrundfunktion'] == 'Wärme versorgen':
            submodel_df = label_ebene_zwei(submodel_df, index, 'https://x0a6xxkk1wk61aky.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_wv)
            if submodel_df.at[index, 'LabelZweiteEbene'] == 'Wärme erzeugen':
                submodel_df = label_komponente(submodel_df, index, 'https://e4tgijtfjyicemkl.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_we)
                if submodel_df.at[index, 'LabelKomponente'] == 'BHKW':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelBhkw)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kessel':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKessel)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Pelletkessel':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelPelletkessel)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmepumpe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWärmepumpe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmeversorger allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWärmeversorgerAllgemein)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Wärme verteilen':
                submodel_df = label_komponente(submodel_df, index, 'https://v2o9y3sziy0nl9w8.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_wärme_verteilen)
                if submodel_df.at[index, 'LabelKomponente'] == 'Pumpe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelPumpe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Ventil':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVentil)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Raum':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRaum)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Vorlauf':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVorlauf)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Heizkreis allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelHeizkreisAllgemein)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Rücklauf':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRücklauf)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Druckhaltestation':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelDruckhaltestation)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Heizkurve':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelHeizkurve)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKMZ)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Regler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRegler)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Übertrager':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelÜbertrager)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWMZ)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Warmwasserbereitung':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWWB)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Wärme beziehen':
                submodel_df.at[index, 'LabelKomponente'] == 'Fernwärme'
                submodel_df.at[index, 'ScoreKomponente'] = 1
                if submodel_df.at[index, 'LabelKomponente'] == 'Fernwärme':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFernwärme)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Wärme speichern':
                submodel_df.at[index, 'LabelKomponente'] = 'Speicher'
                submodel_df.at[index, 'ScoreKomponente'] = 1
                if submodel_df.at[index, 'LabelKomponente'] == 'Speicher':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelSpeicher)
        elif submodel_df.at[index, 'LabelGrundfunktion'] == 'Luft versorgen':
            submodel_df = label_ebene_zwei(submodel_df, index, 'https://vzg0uwwuodns1yav.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_lv)
            if submodel_df.at[index, 'LabelZweiteEbene'] == 'Luft bereitstellen':
                submodel_df = label_komponente(submodel_df, index, 'https://idk9o946rmtr7acy.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_lb)
                if submodel_df.at[index, 'LabelKomponente'] == 'Abluft allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelAbluftAllgemein)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Zuluft allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelZuluftAllgemein)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Zuluftventilator':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelZuluftventilator)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Abluftventilator':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelAbluftventilator)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Fortluftklappe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFortluftklappe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Abluftklappe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelAbluftklappe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Zuluftklappe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelZuluftklappe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Außenluftklappe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelAußenluftklappe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Klappen allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKlappe)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Befeuchter':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelBefeuchter)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Erhitzer':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelErhitzer)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Abluftfilter':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFilter)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Zuluftfilter':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFilter)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Filter':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFilter)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Außenluftfilter':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFilter)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Gerät allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelGerätAllgemein)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kühler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKühler)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Umluft':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelUmluft)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmerückgewinnung':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWrg)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKMZRlt)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWMZRlt)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Ventilator':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVentilator)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Regler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelReglerRlt)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Luft verteilen':
                submodel_df = label_komponente(submodel_df, index, 'https://vo997j7x85a9xhiw.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_luft_verteilen)
                if submodel_df.at[index, 'LabelKomponente'] == 'Volumenstromregler Zuluft':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVsrAbluftZuluft)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Volumenstromregler Abluft':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVsrAbluftZuluft)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Volumenstromregler Raum':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVsrRaum)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Raum':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRaumRlt)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Auslass':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelAuslass)
        elif submodel_df.at[index, 'LabelGrundfunktion'] == 'Medien versorgen':
            submodel_df = label_ebene_zwei(submodel_df, index, 'https://ukmaffqudyrq5c67.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_mv)
            if submodel_df.at[index, 'LabelZweiteEbene'] == 'Medien bereitstellen':
                submodel_df = label_komponente(submodel_df, index, 'https://f22wlztf3s91ijyq.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_mb)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Medien verteilen':
                submodel_df = label_komponente(submodel_df, index, 'https://wk4i8t8fs3bet51b.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_medien_verteilen)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Medien entsorgen':
                submodel_df = label_komponente(submodel_df, index, 'https://fq4hhtntn4avpdbg.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_me)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Medien speichern':
                submodel_df.at[index, 'LabelKomponente'] = 'Speicher'
                submodel_df.at[index, 'ScoreKomponente'] = 1
        elif submodel_df.at[index, 'LabelGrundfunktion'] == 'Kälte versorgen':
            submodel_df = label_ebene_zwei(submodel_df, index, 'https://syabwso8g3aot0x0.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_kv)
            if submodel_df.at[index, 'LabelZweiteEbene'] == 'Kälte erzeugen':
                submodel_df = label_komponente(submodel_df, index, 'https://zrn28zc0qduxnird.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_ke)
                if submodel_df.at[index, 'LabelKomponente'] == 'Kälteanlage':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKälteanlage)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältekreis allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKältekreisAllgemein)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältemaschine':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKältemaschine)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKmzKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Klappe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKlappeKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Pumpe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelPumpeKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Rückkühlwerk':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRkw)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Regler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelReglerKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Rücklauf':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRücklaufKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Ventil':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVentilKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Vorlauf':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVorlaufKälteErzeugen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWmzKälteErzeugen)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Kälte verteilen':
                submodel_df = label_komponente(submodel_df, index, 'https://b0u8vvr4te63alb9.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_kälte_verteilen)
                if submodel_df.at[index, 'LabelKomponente'] == 'Frequenzumrichter':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelFu)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältekreis allgemein':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKältekreisAllgemeinKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Kältemaschinenanschluss':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKältemaschinenAnschluss)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Klappe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelKlappeKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Pumpe':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelPumpeKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Raum':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRaumKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Regler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelReglerKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Rücklauf':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelRücklaufKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Umluftkühlgerät':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelUmluftkühlgerät)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Ventil':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVentilKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Vorlauf':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelVorlaufKälteVerteilen)
                elif submodel_df.at[index, 'LabelKomponente'] == 'Wärmemengenzähler':
                    submodel_df = label_datapoint(submodel_df, index, hf_url_datenpunkt, labelWmzKälteVerteilen)
            elif submodel_df.at[index, 'LabelZweiteEbene'] == 'Kälte speichern':
                submodel_df.at[index, 'LabelKomponente'] = 'Speicher'
                submodel_df.at[index, 'ScoreKomponente'] = 1
        elif submodel_df.at[index, 'LabelGrundfunktion'] == 'Sichern':
            submodel_df.at[index, 'LabelZweiteEbene'] = 'Sichern'
            submodel_df.at[index, 'ScoreZweiteEbene'] = 1
            submodel_df = label_komponente(submodel_df, index, 'https://fplw2my0d3jol283.eu-west-1.aws.endpoints.huggingface.cloud', label_mapping_sichern)
    # Neu für Anlagenklassifizierung
            
    print('Alina Start')
            
    hf_url_anlage = 'https://drtm4zzl09iy5rrc.us-east-1.aws.endpoints.huggingface.cloud'
            
    df_verteilen, df_pumps, submodel_df = prepare_data(submodel_df)

    df_pumps = generiereAnlagen(df_pumps, 0.7, hf_url_anlage)

    label_list = labelliste(df_pumps)
    #!!! Wenn keine true Label vorab da sind dann:
    label_translate = translate_label(label_list)

    df_classified = classify(df_verteilen,label_list,8,label_translate, hf_url_anlage)

    submodel_df.update(df_classified)

    #restliche Wärme:
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Wärme erzeugen', 'LabelAnlage'] = 'Erzeuger 1'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Wärme speichern', 'LabelAnlage'] = 'Wärmespeicher 1'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Wärme beziehen', 'LabelAnlage'] = 'Fernwärme 1'
    #restliche Kälte:
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Kälte erzeugen', 'LabelAnlage'] = 'Erzeuger 2'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Kälte speichern', 'LabelAnlage'] = 'Kältespeicher 1'
    #restliche Lüftung:
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Luft bereitstellen', 'LabelAnlage'] = 'Lüftungsanlage 1'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Luft verteilen', 'LabelAnlage'] = 'Lüftungsstrang 1'
    #Medien:
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Medien bereitstellen', 'LabelAnlage'] = 'Bereitstellung 1'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Medien verteilen', 'LabelAnlage'] = 'Medien Verteilkreis 1'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Medien entsorgen', 'LabelAnlage'] = 'Entsorgung 1'
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Medien speichern', 'LabelAnlage'] = 'Medienspeicher 1'
    #Sichern:
    submodel_df.loc[submodel_df['LabelZweiteEbene'] == 'Sichern', 'LabelAnlage'] = 'Sichern 1'

    #Bis hierhin von Alina mit ANlagangenklassifizierung

    print('Alina Ende')

    submodel_df = submodel_df.fillna('NaN')
    
    #nlp_submodel, submodel_for_aas = create_nlp_submodel_collections(submodel_df)
    nlp_submodel = create_nlp_submodel_collections(submodel_df)
    #print(nlp_submodel)
    # Unix Timestamp für individuelle ID des Teilmodells
    unix_timestamp = int(time.time()* 1000)
    nlp_submodel_id = 'th-koeln.de/gart/submodel/NLPClassificationResult/'+ str(unix_timestamp)
    # ID muss sowohl dem Teilmodell, als auch der Referenz innerhalb der AAS auf das Teilmodell
    # hinzugefügt werden
    nlp_submodel['identification']['id'] = nlp_submodel_id
    #submodel_for_aas['keys'][0]['value'] = nlp_submodel_id
    # Hinzufügen NLP Teilmodell
    #predict_data["submodels"].append(nlp_submodel)
    #predict_data["assetAdministrationShells"][0]["submodels"].append(submodel_for_aas)
    #print(type(predict_data))

    # Umformen zu wohlformiertem JSON
    #json_aas = json.dumps(predict_data, indent=2)
    #print(type(json_aas))

    #return predict_data
    return nlp_submodel

def prepare_data(submodel_df): #submodel_df enthält alle Datenpunkte einer Automationsstation!

  #Neue Spalten für Anlagenklassifizierung:
  submodel_df['LabelAnlage']='nothing'
  submodel_df['ScoreAnlage']='nothing'

  # Filter df nach KaelteVerteilen & Wärmeverteilen:
  df_verteilen=submodel_df[(submodel_df['LabelZweiteEbene'] == 'Wärme verteilen') | (submodel_df['LabelZweiteEbene'] == 'Kälte verteilen')]
  
  # Filter nach Rückmeldung Betrieb -> Annahme das jede Pumpe über eine Rückmeldung Betrieb verfügt
  df_pumps=df_verteilen[(df_verteilen['LabelKomponente'] == 'Pumpe') & (df_verteilen['LabelDatenpunkt'] == 'Rückmeldung Betrieb')]

  return df_verteilen, df_pumps, submodel_df

def check_scores(scores, labels, threshold):
    doubles = [label for label, score in zip(labels, scores) if score > threshold]
    return ", ".join(doubles) if doubles else "No Double"

def generiereAnlagen(df_pumps,threshold, hf_url_anlage): #df=df_pumps

  
  # Eindeutige Premises im Datensatz
  unique_premises = df_pumps['ObjectName'].unique()

  correct_predictions = 0
  total_predictions = 0

  for premise in unique_premises:
      labels = [p for p in unique_premises if p != premise]
      labels = list(set(labels))  #Entferne Duplikate

      hypothese = 'This datapoint belongs to {}'

      headers = {
        'Authorization': 'Bearer BWKspKrXvGhLerysCyfYISapWopuGGPTDRxAowpKsiPugTuTqNLQrSPTJEvGkOsVQLIGyBEaNHymluAgZpRClVFJdQuRgvMGIpnWBPTAxnEIZGgthUdywhaqoGIZsewN',
        'Content-Type': 'application/json',
      }

      json_data = {
        'inputs': premise,
        'parameters': {
            'candidate_labels': labels,
            'hypothesis_template': hypothese
        }
      }
      response = requests.post(hf_url_anlage, headers=headers, json=json_data)
      encoded_response = json.loads(response.content.decode("utf-8"))
      top_3_labels = encoded_response['labels'][0:3]
      top_3_scores = encoded_response['scores'][0:3]


      #submodel_df.at[index, 'LabelDatenpunkt'] = label_name
      #submodel_df.at[index, 'ScoreDatenpunkt'] = label_score

      # Alina: prediction = pipe(premise, labels, hypothesis_template=template)

      # Alina: top_3_labels = prediction['labels'][0:3]
      # Alina: top_3_scores = prediction['scores'][0:3]

      #df_pumps.loc[df_pumps['ObjectName'] == premise, 'Ergebnis_Labels'] = ", ".join(top_3_labels)
      #df_pumps.loc[df_pumps['ObjectName'] == premise, 'Ergebnis_Scores'] = ", ".join(map(str, top_3_scores))
      
      df_pumps.loc[df_pumps['ObjectName'] == premise, 'Ergebnis_Labels'] = ", ".join(top_3_labels)
      df_pumps.loc[df_pumps['ObjectName'] == premise, 'Ergebnis_Scores'] = ", ".join(map(str, top_3_scores))

      double_labels = check_scores(top_3_scores, top_3_labels, threshold)

      df_pumps.loc[df_pumps['ObjectName'] == premise, 'Double'] = double_labels
     # print(type(double_labels),double_labels) #string

     # Alina: wenn label bekannt unter "Anlage_AKS":
       #anlage_aktueller_premise=df_pumps.loc[df_pumps['ObjectName'] == premise]['Anlage_AKS'].iloc[0]
       #anlage_index=df_pumps.loc[df_pumps['ObjectName'] == premise]['Anlage_AKS'].index[0]
       #anlage_aks_count = df_pumps['Anlage_AKS'].eq(anlage_aktueller_premise).sum()
       #print(anlage_aks_count)
       #checke ob double_labels mehr als einen string hat:
       #if ',' in double_labels:
       #   double_labels_list = double_labels.split(', ')
       #    anlage_vorhergesagter_doublepremise = df_pumps[df_pumps['ObjectName'].isin(double_labels_list)]['Anlage_AKS']
       #else:
       #    anlage_vorhergesagter_doublepremise = df_pumps[df_pumps['ObjectName'] == double_labels]['Anlage_AKS']


      #anlage_vorhergesagter_doublepremise = pumps_df.loc[pumps_df['premise'] == double_labels, 'Anlage_AKS'] #type pandas series
      #anlage_vorhergesagter_doublepremise = pumps_df[pumps_df['premise'].isin(double_labels)]['Anlage_AKS']
        # if not anlage_vorhergesagter_doublepremise.empty:
        #     try:
        #         anlage_vorhergesagter_doublepremise = anlage_vorhergesagter_doublepremise.drop(anlage_index)
        #     except KeyError:
        #         pass
        #     anlage_vorhergesagter_doublepremise_list = anlage_vorhergesagter_doublepremise.tolist()
        #     # print('länge liste',len(anlage_vorhergesagter_doublepremise_list))
        #     # print ('liste',anlage_vorhergesagter_doublepremise_list)
        # else:
        #     #print(anlage_vorhergesagter_doublepremise)
        #     print("Die Liste ist leer.")


        # if double_labels != "No Double" and not anlage_vorhergesagter_doublepremise.empty:
        #     #werte = anlage_vorhergesagter_doublepremise.tolist()
        #     ergebnis = all(e == anlage_aktueller_premise for e in anlage_vorhergesagter_doublepremise_list)  # Überprüfen, ob alle Einträge in werte gleich wertX sind
        #     df_pumps.loc[df_pumps['ObjectName'] == premise, 'vorhersage_korrekt'] = ergebnis
        # # print(ergebnis)

        # elif double_labels == "No Double" and anlage_aks_count == 1:
        #     df_pumps.loc[df_pumps['ObjectName'] == premise, 'vorhersage_korrekt'] = True

        # else:
        #     df_pumps.loc[df_pumps['ObjectName'] == premise, 'vorhersage_korrekt'] = False

  return df_pumps

# Define a function to check if two lists have the same elements (order doesn't matter)
def lists_equal(list1, list2):
    def clean_string(s):
        return ''.join(s.split())  # Remove all whitespace characters

    return set(map(clean_string, list1)) == set(map(clean_string, list2))

def labelliste(df_pumps): # Funktion um die Labelliste aus der Pumpenklassifizierung zu generieren (von jeder Pumpe einen unique BM-Datenpunkt!)
    # Create an empty list to store the label lists
    label_lists = []
    no_double_list = []

    print(df_pumps)

    for index, row in df_pumps.iterrows():
        if row['Double'] != "No Double":
            # Extract values from 'Double' and 'premise' columns
            doubles = row['Double'].split(',')  # Assuming values in 'Double' are comma-separated
            premise = row['ObjectName']

            # Create a new list and add values from 'Double' and 'premise'
            label_list = [premise] + doubles
            label_lists.append(label_list)
        else:
            premise = row['ObjectName']
            no_double_list.append(premise)

    # Initialize a list to keep track of unique label lists
    unique_label_lists = []

    # Compare label lists
    for label_list in label_lists:
        is_unique = True
        for unique_list in unique_label_lists:
            if lists_equal(label_list, unique_list):
                is_unique = False
                break
        if is_unique:
            unique_label_lists.append(label_list)

    # Keep only the first entry of each unique list
    first_entries = [unique_list[0] for unique_list in unique_label_lists]
    first_entries.extend(no_double_list)
    first_entries.append('None')
    label_list=first_entries

    print(label_list)

    return label_list


def translate_label(label_list): # um Pumpennamen in "Verteilkreis 1,2,3,..." zu mappen
  if 'None' not in label_list:
    label_list.append('None')

  df = pd.DataFrame(label_list, columns=['label'])

  # Füge die Übersetzungen hinzu
  df['translation'] = [f'Verteilkreis {i}' if label != 'None' else 'None' for i, label in enumerate(range(1, len(df) + 1), start=1)]
  df.loc[df['label'] == 'None', 'translation'] = 'None'

  return df

def classify(df_verteilen, label_list, batchsize, label_translate, hf_url_anlage):

    hypothese = 'This datapoint belongs to {}'

    # Assuming text_list is a list of texts you want to classify
    text_list = df_verteilen['ObjectName'].tolist()

    # Set the batch size
    batch_size = batchsize  # Adjust the batch size based on your system's memory capacity

    # Process texts in batches
    #predictions = []

    headers = {
        'Authorization': 'Bearer BWKspKrXvGhLerysCyfYISapWopuGGPTDRxAowpKsiPugTuTqNLQrSPTJEvGkOsVQLIGyBEaNHymluAgZpRClVFJdQuRgvMGIpnWBPTAxnEIZGgthUdywhaqoGIZsewN',
        'Content-Type': 'application/json',
    }

    """
    for i in range(0, len(text_list), batch_size):
        batch_texts = text_list[i:i + batch_size]
        batch_results = classifier(batch_texts, label_list, hypothesis_template = hypothesis_template)

        predictions.extend(batch_results)
    """
    label_names = []
    label_scores = []

    for i in range(0, len(text_list)):
        text = text_list[i]
        #print(text)
        json_data = {
            'inputs': text,
            'parameters': {
                'candidate_labels': label_list,
                'hypothesis_template': hypothese
            }
        }
        
        #batch_results = classifier(batch_texts, label_list, hypothesis_template = hypothesis_template)
        response = requests.post(hf_url_anlage, headers=headers, json=json_data)
        encoded_response = json.loads(response.content.decode("utf-8"))
    

        label_name = encoded_response['labels'][0]
        label_score = encoded_response['scores'][0]

        label_names.append(label_name)
        label_scores.append(label_score)

    # Extract relevant information from predictions and add to DataFrame
    #top_prediction = [result['labels'][0] if result['labels'] else None for result in predictions]
    #top_score = [result['scores'][0] if result['scores'] else None for result in predictions]

    #print(label_names)
    #print(label_scores)
    df_verteilen['LabelOrigin'] = label_names
    df_verteilen['ScoreAnlage'] = label_scores

    # Iterate through df1['label_origin']
    for index, row in df_verteilen.iterrows():
        label_origin_value = row['LabelOrigin']

        # Check if label_origin_value is in df2['label']
        if label_origin_value in label_translate['label'].values:
            # Get the corresponding translation value from df2
            translation_value = label_translate.loc[label_translate['label'] == label_origin_value, 'translation'].values[0]

            # Write the translation value to df1['LabelAnlage']
            df_verteilen.at[index, 'LabelAnlage'] = translation_value

    #df = df.drop(columns=['label', 'translation'])
            
    print(df_verteilen.iloc[0])

    return df_verteilen
