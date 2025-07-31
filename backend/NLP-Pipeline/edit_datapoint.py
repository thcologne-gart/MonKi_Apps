import json
import pandas as pd
import requests
import time

# Aufruf NLP Pipeline zum Labeln der zweiten Ebene -> Text Classification
def label_ebene_zwei(nlpInput, hf_url):

    headers = {
        'Authorization': '<TOKEN>',
        'Content-Type': 'application/json',
    }

    json_data = {
        'inputs': nlpInput,
        'parameters': {
            'top_k': None,
        },
    }
    response = requests.post(hf_url, headers=headers, json=json_data)

    encoded_response = json.loads(response.content.decode("utf-8"))
    label_name = encoded_response[0]['label']
    label_score = encoded_response[0]['score']
    resultEbeneZwei = {
        'labelZweiteEbene': label_name,
        'scoreZweiteEbene': label_score
    }

    return resultEbeneZwei
 
# Labeln Komponente -> Text Classification
def label_komponente(nlpInput, hf_url):

    headers = {
        'Authorization': '<TOKEN>',
        'Content-Type': 'application/json',
    }

    json_data = {
        'inputs': nlpInput,
        'parameters': {
            'top_k': None,
        },
    }
    response = requests.post(hf_url, headers=headers, json=json_data)

    encoded_response = json.loads(response.content.decode("utf-8"))
    label_name = encoded_response[0]['label']
    label_score = encoded_response[0]['score']
    resultEbeneKomponente = {
        'labelKomponente': label_name,
        'scoreKomponente': label_score
    }
    return resultEbeneKomponente

# Labeln Datenpunkt Ebene -> Zero Shot mit NLI
def label_datapoint(nlpInput, hf_url, candidate_labels):
    # Candidate Labels sind die weiter unten spezifiierten möglichen Label des Datenpunkts
    # für eine Komponente. Diese werden mit der Hypothese verknüpft. Dann NLI mit dem Datenpunkt (Name / Description)

    hypothese = 'Der Datenpunkt beschreibt: {}.'

    headers = {
        'Authorization': '<TOKEN>',
        'Content-Type': 'application/json',
    }

    json_data = {
        'inputs': nlpInput,
        'parameters': {
            'candidate_labels': candidate_labels,
            'hypothesis_template': hypothese
        }
    }
    response = requests.post(hf_url, headers=headers, json=json_data)
    encoded_response = json.loads(response.content.decode("utf-8"))
    label_name = encoded_response['labels'][0]
    label_score = encoded_response['scores'][0]
    resultDatenpunkt = {
        'labelDatenpunkt': label_name,
        'scoreDatenpunkt': label_score
    }
    return resultDatenpunkt

def edit_from_datenpunkt(datapoint_information):
    resultDatenpunkt = {
        'labelDatenpunkt': datapoint_information['labelDatenpunkt'],
        'scoreDatenpunkt': 1.0
    }

    result = [resultDatenpunkt]

    return result

def edit_from_komponente(datapoint_information, label_dict, hf_url_datenpunkt):
    print(datapoint_information)

    correctedLabel = datapoint_information['labelKomponente']
    nlpInput = datapoint_information['nlpInput']

    if correctedLabel == 'BHKW':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBhkw'])
    elif correctedLabel == 'Kessel':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKessel'])
    elif correctedLabel == 'Pelletkessel':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelPelletkessel'])
    elif correctedLabel == 'Waermepumpe':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelWärmepumpe'])
    elif correctedLabel == 'Pumpe':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelPumpe'])
    elif correctedLabel == 'Ventil':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVentil'])
    elif correctedLabel == 'Raum' and datapoint_information['labelZweiteEbene'] == 'Verteilen':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRaum'])
    elif correctedLabel == 'Vorlauf':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVorlauf'])
    elif correctedLabel == 'HeizkreisAllgemein':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelHeizkreisAllgemein'])
    elif correctedLabel == 'Ruecklauf':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRücklauf'])
    elif correctedLabel == 'Fernwaerme':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBeziehen'])
    elif correctedLabel == 'Speicher':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelSpeichern'])
    elif correctedLabel == 'AbluftAllgemein':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelAbluftAllgemein'])
    elif correctedLabel == 'ZuluftAllgemein':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelZuluftAllgemein'])
    elif correctedLabel == 'Zuluftventilator':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelZuluftventilator'])
    elif correctedLabel == 'Abluftventilator':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelAbluftventilator'])
    elif correctedLabel == 'Fortluftklappe':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
    elif correctedLabel == 'Abluftklappe':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
    elif correctedLabel == 'Zuluftklappe':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
    elif correctedLabel == 'Außenluftklappe':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
    elif correctedLabel == 'KlappenAllgemein':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
    elif correctedLabel == 'Befeuchter':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBefeuchter'])
    elif correctedLabel == 'Erhitzer':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelErhitzer'])
    elif correctedLabel == 'Abluftfilter':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
    elif correctedLabel == 'Zuluftfilter':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
    elif correctedLabel == 'Filter':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
    elif correctedLabel == 'Außenluftfilter':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
    elif correctedLabel == 'GeraetAllgemein':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelGerätAllgemein'])
    elif correctedLabel == 'Kühler':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKühler'])
    elif correctedLabel == 'Umluft':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelUmluft'])
    elif correctedLabel == 'Wärmerückgewinnung':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelWrg'])
    elif correctedLabel == 'VolumenstromreglerZuluft':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
    elif correctedLabel == 'VolumenstromreglerAbluft':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
    elif correctedLabel == 'VolumenstromreglerRaum':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
    elif correctedLabel == 'Raum' and datapoint_information['labelZweiteEbene'] == 'LuftVerteilen':
        resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRaumRlt']) 
    else: 
        resultDatenpunkt = {
            'labelDatenpunkt': 'Not defined',
            'scoreDatenpunkt': 0
        }

    result = [resultDatenpunkt]   
    return result

def edit_from_zweite_ebene(datapoint_information, label_dict, hf_url_datenpunkt):
    print(datapoint_information)

    correctedLabel = datapoint_information['labelZweiteEbene']
    nlpInput = datapoint_information['nlpInput']

    if correctedLabel == 'Erzeugen':
        resultKomponente = label_komponente(nlpInput, 'https://j5g3v827fcj2o7vz.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultKomponente['labelKomponente'] == 'BHKW':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBhkw'])
        elif resultKomponente['labelKomponente'] == 'Kessel':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKessel'])
        elif resultKomponente['labelKomponente'] == 'Pelletkessel':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelPelletkessel'])
        elif resultKomponente['labelKomponente'] == 'Waermepumpe':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelWärmepumpe'])
        else: 
            resultDatenpunkt = {
                'labelDatenpunkt': 'Not defined',
                'scoreDatenpunkt': 0
            }
    elif correctedLabel == 'Verteilen':
        resultKomponente = label_komponente(nlpInput, 'https://licaov4szmilwd8r.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultKomponente['labelKomponente'] == 'Pumpe':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelPumpe'])
        elif resultKomponente['labelKomponente'] == 'Ventil':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVentil'])
        elif resultKomponente['labelKomponente'] == 'Raum':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRaum'])
        elif resultKomponente['labelKomponente'] == 'Vorlauf':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVorlauf'])
        elif resultKomponente['labelKomponente'] == 'HeizkreisAllgemein':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelHeizkreisAllgemein'])
        elif resultKomponente['labelKomponente'] == 'Ruecklauf':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRücklauf'])
        else: 
            resultDatenpunkt = {
                'labelDatenpunkt': 'Not defined',
                'scoreDatenpunkt': 0
            }
    elif correctedLabel == 'Beziehen':
        resultKomponente = {
            'labelKomponente': 'Fernwärme',
            'scoreKomponente': 1.0
        }
        if resultKomponente['labelKomponente'] == 'Fernwärme':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBeziehen'])
    elif correctedLabel == 'Speichern':
        resultKomponente = {
            'labelKomponente': 'Speicher',
            'scoreKomponente': 1.0
        }
        if resultKomponente['labelKomponente'] == 'Speicher':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelSpeichern'])
    if correctedLabel == 'LuftBereitstellen':
        resultKomponente = label_komponente(nlpInput, 'https://tu0l4azn4h2zs51l.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultKomponente['labelKomponente'] == 'AbluftAllgemein':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelAbluftAllgemein'])
        elif resultKomponente['labelKomponente'] == 'ZuluftAllgemein':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelZuluftAllgemein'])
        elif resultKomponente['labelKomponente'] == 'Zuluftventilator':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelZuluftventilator'])
        elif resultKomponente['labelKomponente'] == 'Abluftventilator':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelAbluftventilator'])
        elif resultKomponente['labelKomponente'] == 'Fortluftklappe':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
        elif resultKomponente['labelKomponente'] == 'Abluftklappe':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
        elif resultKomponente['labelKomponente'] == 'Zuluftklappe':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
        elif resultKomponente['labelKomponente'] == 'Außenluftklappe':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
        elif resultKomponente['labelKomponente'] == 'KlappenAllgemein':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
        elif resultKomponente['labelKomponente'] == 'Befeuchter':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBefeuchter'])
        elif resultKomponente['labelKomponente'] == 'Erhitzer':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelErhitzer'])
        elif resultKomponente['labelKomponente'] == 'Abluftfilter':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
        elif resultKomponente['labelKomponente'] == 'Zuluftfilter':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
        elif resultKomponente['labelKomponente'] == 'Filter':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
        elif resultKomponente['labelKomponente'] == 'Außenluftfilter':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
        elif resultKomponente['labelKomponente'] == 'GerätAllgemein':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelGerätAllgemein'])
        elif resultKomponente['labelKomponente'] == 'Kühler':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKühler'])
        elif resultKomponente['labelKomponente'] == 'Umluft':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelUmluft'])
        elif resultKomponente['labelKomponente'] == 'Wärmerückgewinnung':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelWrg'])
        else: 
            resultDatenpunkt = {
                'labelDatenpunkt': 'Not defined',
                'scoreDatenpunkt': 0
            }
    elif correctedLabel == 'LuftVerteilen':
        resultKomponente = label_komponente(nlpInput, 'https://be0xyulh7jm7r427.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultKomponente['labelKomponente'] == 'VolumenstromreglerZuluft':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
        elif resultKomponente['labelKomponente'] == 'VolumenstromreglerAbluft':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
        elif resultKomponente['labelKomponente'] == 'VolumenstromreglerRaum':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
        elif resultKomponente['labelKomponente'] == 'Raum':
            resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRaumRlt'])
        else: 
            resultDatenpunkt = {
                'labelDatenpunkt': 'Not defined',
                'scoreDatenpunkt': 0
            }
    if correctedLabel == 'MedienBereitstellen':
       resultKomponente = label_komponente(nlpInput, 'https://kjvyy1gatbnrpd9j.eu-west-1.aws.endpoints.huggingface.cloud')
    elif correctedLabel == 'MedienVerteilen':
        resultKomponente = label_komponente(nlpInput, 'https://zz8r4yb9ne3oq830.eu-west-1.aws.endpoints.huggingface.cloud')
    elif correctedLabel == 'MedienEntsorgen':
        resultKomponente = label_komponente(nlpInput, 'https://hzo8bgl46cn0ajp2.eu-west-1.aws.endpoints.huggingface.cloud')
    elif correctedLabel == 'MedienSpeichern':
        resultKomponente = {
            'labelKomponente': 'Speicher',
            'scoreKomponente': 1.0
        }
    
    result = [resultKomponente, resultDatenpunkt]   
    return result

def edit_from_grundfunktion(datapoint_information, label_dict, hf_url_datenpunkt):

    correctedLabel = datapoint_information['correctedLabel']
    nlpInput = datapoint_information['nlpInput']
    
    if correctedLabel == 'WaermeVersorgen':
        resultZweiteEbene = label_ebene_zwei(nlpInput, 'https://b1q5jfx5fvw0xjkc.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultZweiteEbene['labelZweiteEbene'] == 'Erzeugen':
            resultKomponente = label_komponente(nlpInput, 'https://j5g3v827fcj2o7vz.eu-west-1.aws.endpoints.huggingface.cloud')
            if resultKomponente['labelKomponente'] == 'BHKW':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBhkw'])
            elif resultKomponente['labelKomponente'] == 'Kessel':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKessel'])
            elif resultKomponente['labelKomponente'] == 'Pelletkessel':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelPelletkessel'])
            elif resultKomponente['labelKomponente'] == 'Waermepumpe':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelWärmepumpe'])
            else: 
                resultDatenpunkt = {
                    'labelDatenpunkt': 'Not defined',
                    'scoreDatenpunkt': 0
                }

        elif resultZweiteEbene['labelZweiteEbene'] == 'Verteilen':
            resultKomponente = label_komponente(nlpInput, 'https://licaov4szmilwd8r.eu-west-1.aws.endpoints.huggingface.cloud')
            if resultKomponente['labelKomponente'] == 'Pumpe':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelPumpe'])
            elif resultKomponente['labelKomponente'] == 'Ventil':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVentil'])
            elif resultKomponente['labelKomponente'] == 'Raum':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRaum'])
            elif resultKomponente['labelKomponente'] == 'Vorlauf':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVorlauf'])
            elif resultKomponente['labelKomponente'] == 'HeizkreisAllgemein':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelHeizkreisAllgemein'])
            elif resultKomponente['labelKomponente'] == 'Ruecklauf':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRücklauf'])
            else: 
                resultDatenpunkt = {
                    'labelDatenpunkt': 'Not defined',
                    'scoreDatenpunkt': 0
                }

        elif resultZweiteEbene['labelZweiteEbene'] == 'Beziehen':
            resultKomponente = {
                'labelKomponente': 'Fernwärme',
                'scoreKomponente': 1.0
            }
            if resultKomponente['labelKomponente'] == 'Fernwärme':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBeziehen'])
        elif resultZweiteEbene['labelZweiteEbene'] == 'Speichern':
            resultKomponente = {
                'labelKomponente': 'Speicher',
                'scoreKomponente': 1.0
            }
            if resultKomponente['labelKomponente'] == 'Speicher':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelSpeichern'])
    elif correctedLabel == 'LuftVersorgen':
        resultZweiteEbene = label_ebene_zwei(nlpInput, 'https://akwxfoifsn1d3dyo.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultZweiteEbene['labelZweiteEbene'] == 'LuftBereitstellen':
            resultKomponente = label_komponente(nlpInput, 'https://tu0l4azn4h2zs51l.eu-west-1.aws.endpoints.huggingface.cloud')
            if resultKomponente['labelKomponente'] == 'AbluftAllgemein':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelAbluftAllgemein'])
            elif resultKomponente['labelKomponente'] == 'ZuluftAllgemein':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelZuluftAllgemein'])
            elif resultKomponente['labelKomponente'] == 'Zuluftventilator':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelZuluftventilator'])
            elif resultKomponente['labelKomponente'] == 'Abluftventilator':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelAbluftventilator'])
            elif resultKomponente['labelKomponente'] == 'Fortluftklappe':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
            elif resultKomponente['labelKomponente'] == 'Abluftklappe':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
            elif resultKomponente['labelKomponente'] == 'Zuluftklappe':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
            elif resultKomponente['labelKomponente'] == 'Außenluftklappe':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
            elif resultKomponente['labelKomponente'] == 'KlappenAllgemein':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKlappe'])
            elif resultKomponente['labelKomponente'] == 'Befeuchter':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelBefeuchter'])
            elif resultKomponente['labelKomponente'] == 'Erhitzer':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelErhitzer'])
            elif resultKomponente['labelKomponente'] == 'Abluftfilter':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
            elif resultKomponente['labelKomponente'] == 'Zuluftfilter':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
            elif resultKomponente['labelKomponente'] == 'Filter':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
            elif resultKomponente['labelKomponente'] == 'Außenluftfilter':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelFilter'])
            elif resultKomponente['labelKomponente'] == 'GerätAllgemein':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelGerätAllgemein'])
            elif resultKomponente['labelKomponente'] == 'Kühler':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelKühler'])
            elif resultKomponente['labelKomponente'] == 'Umluft':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelUmluft'])
            elif resultKomponente['labelKomponente'] == 'Wärmerückgewinnung':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelWrg'])
            else: 
                resultDatenpunkt = {
                    'labelDatenpunkt': 'Not defined',
                    'scoreDatenpunkt': 0
                }
        elif resultZweiteEbene['labelZweiteEbene'] == 'LuftVerteilen':
            resultKomponente = label_komponente(nlpInput, 'https://be0xyulh7jm7r427.eu-west-1.aws.endpoints.huggingface.cloud')
            if resultKomponente['labelKomponente'] == 'VolumenstromreglerZuluft':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
            elif resultKomponente['labelKomponente'] == 'VolumenstromreglerAbluft':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
            elif resultKomponente['labelKomponente'] == 'VolumenstromreglerRaum':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelVsr'])
            elif resultKomponente['labelKomponente'] == 'Raum':
                resultDatenpunkt = label_datapoint(nlpInput, hf_url_datenpunkt, label_dict['labelRaumRlt'])
            else: 
                resultDatenpunkt = {
                    'labelDatenpunkt': 'Not defined',
                    'scoreDatenpunkt': 0
                }
    elif correctedLabel == 'MedienVersorgen':
        resultZweiteEbene = label_ebene_zwei(nlpInput, 'https://vp0di0rrseqw9bxg.eu-west-1.aws.endpoints.huggingface.cloud')
        if resultZweiteEbene['labelZweiteEbene'] == 'MedienBereitstellen':
            resultKomponente = label_komponente(nlpInput, 'https://kjvyy1gatbnrpd9j.eu-west-1.aws.endpoints.huggingface.cloud')
        elif resultZweiteEbene['labelZweiteEbene'] == 'MedienVerteilen':
            resultKomponente = label_komponente(nlpInput, 'https://zz8r4yb9ne3oq830.eu-west-1.aws.endpoints.huggingface.cloud')
        elif resultZweiteEbene['labelZweiteEbene'] == 'MedienEntsorgen':
            resultKomponente = label_komponente(nlpInput, 'https://hzo8bgl46cn0ajp2.eu-west-1.aws.endpoints.huggingface.cloud')
        elif resultZweiteEbene['labelZweiteEbene'] == 'MedienSpeichern':
            resultKomponente = {
                'labelKomponente': 'Fernwärme',
                'scoreKomponente': 1.0
            }
    elif correctedLabel == 'KaelteVersorgen':
        resultZweiteEbene = label_ebene_zwei(nlpInput, 'https://optn7egbs73a3q52.eu-west-1.aws.endpoints.huggingface.cloud')
    elif correctedLabel == 'Sichern':
        resultZweiteEbene = label_ebene_zwei(nlpInput, 'https://ipzqkwuzdt81cw7u.eu-west-1.aws.endpoints.huggingface.cloud')
    print(resultKomponente)
    print(resultZweiteEbene)
    result = [resultZweiteEbene, resultKomponente, resultDatenpunkt]
  
    return result

def start_correction(datapoint_information):
    # Mögliche Label aller Komponente
    # -> erweitern wenn zu ende gelabelt
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
    
    label_dict = {'labelBeziehen': labelBeziehen, 'labelSpeichern': labelSpeichern, 'labelKessel': labelKessel,
                  'labelBhkw': labelBhkw, 'labelWärmepumpe': labelWärmepumpe, 'labelPelletkessel': labelPelletkessel,
                  'labelPumpe': labelPumpe, 'labelVentil': labelVentil, 'labelRaum': labelRaum, 'labelVorlauf': labelVorlauf,
                  'labelRücklauf': labelRücklauf,'labelHeizkreisAllgemein': labelHeizkreisAllgemein,
                  'labelAbluftAllgemein': labelAbluftAllgemein, 'labelAbluftventilator': labelAbluftventilator,
                  'labelZuluftventilator': labelZuluftventilator, 'labelZuluftAllgemein': labelZuluftAllgemein,
                'labelKlappe': labelKlappe, 'labelBefeuchter': labelBefeuchter, 'labelErhitzer': labelErhitzer,
                'labelFilter': labelFilter, 'labelGerätAllgemein': labelGerätAllgemein, 'labelKühler': labelKühler,
                'labelRaumRlt': labelRaumRlt, 'labelUmluft': labelUmluft, 'labelVsr': labelVsr,
                'labelWrg': labelWrg}
    
    hf_url_datenpunkt = 'https://r492wi538iopvp00.us-east-1.aws.endpoints.huggingface.cloud'   
    
    if datapoint_information['startPrediction'] == 'Grundfunktion':
        result = edit_from_grundfunktion(datapoint_information, label_dict, hf_url_datenpunkt)
        basyx_response = edit_aas_basyx(datapoint_information, result)
    elif datapoint_information['startPrediction'] == 'ZweiteEbene':
        result = edit_from_zweite_ebene(datapoint_information, label_dict, hf_url_datenpunkt)
        basyx_response = edit_aas_basyx(datapoint_information, result)
    elif datapoint_information['startPrediction'] == 'Komponente':
        result = edit_from_komponente(datapoint_information, label_dict, hf_url_datenpunkt)
        basyx_response = edit_aas_basyx(datapoint_information, result)
    elif datapoint_information['startPrediction'] == 'Datenpunkt':
        result = edit_from_datenpunkt(datapoint_information)
        basyx_response = edit_aas_basyx_no_nlp(datapoint_information, result)

    print(result)
    return result

def edit_aas_basyx_no_nlp(datapoint_information, result):
    print(datapoint_information)
    aasId = datapoint_information['aasId']
    smcIdShort = datapoint_information['idShort']
    aas_server = "http://3.83.126.51:4001/aasServer/shells/" + aasId + '/aas/submodels/NLPClassificationResult/submodel/submodelElements/' + smcIdShort

    response = requests.get(aas_server)
    data = json.loads(response.content)

    datapointLabeName = result[0]['labelDatenpunkt']
    datapointLabelScore = result[0]['scoreDatenpunkt']

    data['value'][3]['value'][0]['value'][0]['value'] = datapointLabeName
    data['value'][3]['value'][0]['value'][1]['value'] = datapointLabelScore   

    #print(result)
    print(data)
    headers = {"Content-Type": "application/json"}

    smc_string = json.dumps(data)
    response_smc = requests.put(aas_server, data = smc_string, headers = headers)

    print(response_smc)


def edit_aas_basyx(datapoint_information, result):
    print(datapoint_information)
    aasId = datapoint_information['aasId']
    smcIdShort = datapoint_information['idShort']
    aas_server = "http://3.83.126.51:4001/aasServer/shells/" + aasId + '/aas/submodels/NLPClassificationResult/submodel/submodelElements/' + smcIdShort

    response = requests.get(aas_server)
    data = json.loads(response.content)
    if len(result) == 1:
        komponenteName = datapoint_information['labelKomponente'] 
        komponenteScore = 1.0
        datapointLabeName = result[0]['labelDatenpunkt']
        datapointLabelScore = result[0]['scoreDatenpunkt']

        data['value'][3]['value'][0]['value'][0]['value'] = datapointLabeName
        data['value'][3]['value'][0]['value'][1]['value'] = datapointLabelScore

        data['value'][2]['value'][0]['value'][0]['value'] = komponenteName
        data['value'][2]['value'][0]['value'][1]['value'] = komponenteScore
    
    elif len(result) == 2:
        zweiteEbeneName = datapoint_information['labelZweiteEbene'] 
        zweiteEbeneScore = 1.0

        komponenteLabelName = result[0]['labelKomponente']
        komponenteLabelScore = result[0]['scoreKomponente']

        datapointLabeName = result[1]['labelDatenpunkt']
        datapointLabelScore = result[1]['scoreDatenpunkt']

        data['value'][3]['value'][0]['value'][0]['value'] = datapointLabeName
        data['value'][3]['value'][0]['value'][1]['value'] = datapointLabelScore

        data['value'][2]['value'][0]['value'][0]['value'] = komponenteLabelName
        data['value'][2]['value'][0]['value'][1]['value'] = komponenteLabelScore

        data['value'][1]['value'][0]['value'][0]['value'] = zweiteEbeneName
        data['value'][1]['value'][0]['value'][1]['value'] = zweiteEbeneScore

    elif len(result) == 3:

        grundfunktionName = datapoint_information['correctedLabel'] 
        grundfunktionScore = 1.0

        zweiteEbeneLabelName = result[0]['labelZweiteEbene']
        zweiteEbeneLabelScore = result[0]['scoreZweiteEbene']

        komponenteLabelName = result[1]['labelKomponente']
        komponenteLabelScore = result[1]['scoreKomponente']

        datapointLabeName = result[2]['labelDatenpunkt']
        datapointLabelScore = result[2]['scoreDatenpunkt']

        data['value'][3]['value'][0]['value'][0]['value'] = datapointLabeName
        data['value'][3]['value'][0]['value'][1]['value'] = datapointLabelScore

        data['value'][2]['value'][0]['value'][0]['value'] = komponenteLabelName
        data['value'][2]['value'][0]['value'][1]['value'] = komponenteLabelScore

        data['value'][1]['value'][0]['value'][0]['value'] = zweiteEbeneLabelName
        data['value'][1]['value'][0]['value'][1]['value'] = zweiteEbeneLabelScore

        data['value'][0]['value'][0]['value'][0]['value'] = grundfunktionName
        data['value'][0]['value'][0]['value'][1]['value'] = grundfunktionScore

    #print(result)
    print(data)
    headers = {"Content-Type": "application/json"}

    smc_string = json.dumps(data)
    response_smc = requests.put(aas_server, data = smc_string, headers = headers)

    print(response_smc)
"""

def read_sec(aas_file):
    with open(aas_file, 'r') as file:
        edit_data = json.load(file)
    all_elements = edit_data['value']
    element_id_short= edit_data['idShort']
    for element in all_elements:
        if element['idShort'] == 'PredictionGrundfunktion':
            label_grundfunktion = element['value'][0]['value'][0]['value']
            score_grundfunktion = element['value'][0]['value'][1]['value']
            user_grundfunktion = element['value'][0]['value'][2]['value']
        elif element['idShort'] == 'PredictionFunktionEbeneZwei':
            label_zweite_ebene = element['value'][0]['value'][0]['value']
            score_zwete_ebene = element['value'][0]['value'][1]['value']
            user_zweite_ebene = element['value'][0]['value'][2]['value']
        elif element['idShort'] == 'PredictionKomponente':
            label_komponente = element['value'][0]['value'][0]['value']
            score_komponente = element['value'][0]['value'][1]['value']
            user_komponente = element['value'][0]['value'][2]['value']
        elif element['idShort'] == 'PredictionDatapoint':
            label_datenpunkt = element['value'][0]['value'][0]['value']
            score_datenpunkt = element['value'][0]['value'][1]['value']
            user_datenpunkt = element['value'][0]['value'][2]['value']
        elif element['idShort'] == 'NLPInput':
            nlp_text = element['value']
    collection_df = pd.DataFrame({"idShort": element_id_short,
                            "LabelGrundfunktion": label_grundfunktion,
                            "ScoreGrundfunktion": score_grundfunktion,
                            "LabelUserGrundfunktion": user_grundfunktion,
                            "LabelZweiteEbene": label_zweite_ebene,
                            "ScoreZweiteEbene": score_zwete_ebene,
                            "LabelUserZweiteEbene": user_zweite_ebene,
                            "LabelKomponente": label_komponente,
                            "ScoreKomponente": score_komponente,
                            "LabelUserKomponente": user_komponente,
                            "LabelDatenpunkt": label_datenpunkt,
                            "ScoreDatenpunkt": score_datenpunkt,
                            "LabelUserDatenpunkt": user_datenpunkt,
                            "NLPText": nlp_text
                            }, index = [0])
    #print(collection_df.iloc[0]['LabelUserZweiteEbene'])
    # URL für Inference Endpoint Datenpunkt
    hf_url_datenpunkt = 'https://knpvpbn3qfklkw02.eu-west-1.aws.endpoints.huggingface.cloud'

    # Mögliche Label aller Komponente
    # -> erweitern wenn zu ende gelabelt
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
    
    label_dict = {'labelBeziehen': labelBeziehen, 'labelSpeichern': labelSpeichern, 'labelKessel': labelKessel,
                  'labelBhkw': labelBhkw, 'labelWärmepumpe': labelWärmepumpe, 'labelPelletkessel': labelPelletkessel,
                  'labelPumpe': labelPumpe, 'labelVentil': labelVentil, 'labelRaum': labelRaum, 'labelVorlauf': labelVorlauf,
                  'labelRücklauf': labelRücklauf,'labelHeizkreisAllgemein': labelHeizkreisAllgemein,
                  'labelAbluftAllgemein': labelAbluftAllgemein, 'labelAbluftventilator': labelAbluftventilator,
                  'labelZuluftventilator': labelZuluftventilator, 'labelZuluftAllgemein': labelZuluftAllgemein,
                'labelKlappe': labelKlappe, 'labelBefeuchter': labelBefeuchter, 'labelErhitzer': labelErhitzer,
                'labelFilter': labelFilter, 'labelGerätAllgemein': labelGerätAllgemein, 'labelKühler': labelKühler,
                'labelRaumRlt': labelRaumRlt, 'labelUmluft': labelUmluft, 'labelVsr': labelVsr,
                'labelWrg': labelWrg}
    

    if collection_df.iloc[0]['LabelUserGrundfunktion'] != '':
        collection_df = edit_from_grundfunktion(collection_df, hf_url_datenpunkt, label_dict)
    elif collection_df.iloc[0]['LabelUserZweiteEbene'] != '':
        collection_df = edit_from_zweite_ebene(collection_df, hf_url_datenpunkt, label_dict)
    elif collection_df.iloc[0]['LabelUserKomponente'] != '':
        collection_df = edit_from_komponente(collection_df, hf_url_datenpunkt, label_dict)
    elif collection_df.iloc[0]['LabelUserDatenpunkt'] != '':
        print('-----------------------')
        print(collection_df.iloc[0]['LabelDatenpunkt'])
        collection_df.loc[0, 'LabelDatenpunkt'] = collection_df.iloc[0]['LabelUserDatenpunkt']
        collection_df.loc[0, 'ScoreDatenpunkt'] = 1
        print(collection_df.iloc[0]['LabelDatenpunkt'])

    for element in all_elements:
        if element['idShort'] == 'PredictionGrundfunktion':
            element['value'][0]['value'][0]['value'] = collection_df.iloc[0]['LabelGrundfunktion']
            element['value'][0]['value'][1]['value'] = collection_df.iloc[0]['ScoreGrundfunktion']
        elif element['idShort'] == 'PredictionFunktionEbeneZwei':
            element['value'][0]['value'][0]['value'] = collection_df.iloc[0]['LabelZweiteEbene']
            element['value'][0]['value'][1]['value'] = collection_df.iloc[0]['ScoreZweiteEbene']
        elif element['idShort'] == 'PredictionKomponente':
            element['value'][0]['value'][0]['value'] = collection_df.iloc[0]['LabelKomponente']
            element['value'][0]['value'][1]['value'] = collection_df.iloc[0]['ScoreKomponente']
        elif element['idShort'] == 'PredictionDatapoint':
            element['value'][0]['value'][0]['value'] = collection_df.iloc[0]['LabelDatenpunkt']
            element['value'][0]['value'][1]['value'] = collection_df.iloc[0]['ScoreDatenpunkt']
    
    edit_data['value'] = all_elements

    # Umformen zu wohlformiertem JSON
    edited_json = json.dumps(edit_data, indent=2)

    with open('edited_datapoint.json', 'w') as file:
        #json.dump(all_classified_datapoint_collections, file)
        #json.dump(json_aas, file)
        file.write(edited_json)
    return edited_json

if __name__ == "__main__":
    file = "edit_example.json"
    data = read_sec(file)

"""
