<!-- eslint-disable vue/no-mutating-props -->
<!-- eslint-disable vue/no-mutating-props -->
<template>
  <div>
    <v-dialog
        v-model="dialog"
        width="60%">
        <template v-slot:activator="{ props }">
            <!--<v-btn class="ma-3" @click="getData()">Get Data</v-btn>-->
            <v-container class="d-flex justify-center align-center">
              <v-btn
                v-bind="props"
                variant="outlined"
                color = "warning"
                size="small"
            >Edit Datenpunkt</v-btn>
            </v-container>
          </template>
              <v-card>
                <v-toolbar
                color="success"
                >
                <v-toolbar-title style="color: white;">Edit Datenpunkt</v-toolbar-title>
                </v-toolbar>
                <v-container>
                    <v-row>
                        <v-col
                        cols="4"
                        >
                            <v-list lines="two">
                                <v-list-item>
                                    <v-list-item-subtitle>Object Name</v-list-item-subtitle>
                                    <v-list-item-title>{{ datenpunkt['ObjectName'] }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-col>
                        <v-col
                        cols="8"
                        >
                            <v-list lines="two">
                                <v-list-item>
                                    <v-list-item-subtitle>Description</v-list-item-subtitle>
                                    <v-list-item-title>{{ datenpunkt['Description'] }}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-col>
                    </v-row>
                    <v-divider :thickness="3"></v-divider>
                    <v-row class="ma-1">
                        <v-col cols="8">
                            <v-select 
                            :items="grundfunktionen" 
                            v-model="predictedGrundfunktion" 
                            label= 'Grundfunktion' 
                            @update:model-value="changeGrundfunktion"
                            />
                        </v-col>
                        <v-col cols="4" class="d-flex justify-center align-center">
                            <v-btn
                            class="ma-1"
                            v-bind="props"
                            variant="outlined"
                            color = "warning"
                            @click="editZweiteEbene()">
                            New Prediction
                            </v-btn>
                        </v-col>
                    </v-row>
                    <v-row class="ma-1">
                        <v-col cols="8">
                            <div v-for="(value, key) in zweiteEbeneDict" :key="key">
                                <v-select
                                v-if="predictedGrundfunktion == key"
                                :items="value" 
                                v-model="predictedZweiteEbene" 
                                label= 'Zweite Grundfunktion' 
                                @update:model-value="changeZweiteEbene"
                                />
                                <v-select
                                v-else-if="predictedGrundfunktion == ''"
                                :items="zweiteGrundfunktionNochNichtMöglich" 
                                v-model="predictedZweiteEbene" 
                                label= 'Zweite Grundfunktion' 
                                @update:model-value="changeZweiteEbene"
                                />
                            </div>
                        </v-col>
                        <v-col cols="4" class="d-flex justify-center align-center">
                            <v-btn
                            class="ma-1"
                            v-bind="props"
                            variant="outlined"
                            color = "warning"
                            @click ="editKomponente()">
                            New Prediction
                            </v-btn>
                        </v-col>
                    </v-row>
                    <v-row class="ma-1">
                        <v-col cols="8">
                            <div v-for="(value, key) in komponentenEbeneDict" :key="key">
                                <v-select
                                v-if="predictedZweiteEbene == key"
                                :items="value" 
                                v-model="predictedKomponente" 
                                label= 'Komponente' 
                                @update:model-value="changeKomponente"
                                />
                            </div>
                            <v-select
                            v-if="predictedZweiteEbene == ''"
                            :items="komponenteNochNichtMöglich" 
                            v-model="predictedKomponente" 
                            label= 'Komponente' 
                            @update:model-value="changeKomponente"
                            />
                        </v-col>
                        <v-col cols="4" class="d-flex justify-center align-center">
                            <v-btn
                            class="ma-1"
                            v-bind="props"
                            variant="outlined"
                            color = "warning"
                            @click ="editDatenpunkt()">
                            New Prediction
                            </v-btn>
                        </v-col>
                    </v-row>
                    <v-row class="ma-1">
                        <v-col cols="8">
                            <div v-for="(value, key) in datenpunktEbeneDict" :key="key">
                                <v-select
                                v-if="predictedKomponente == key"
                                :items="value" 
                                v-model="predictedDatenpunkt" 
                                label= 'Datenpunkt' 
                                @update:model-value="changeDatenpunkt"
                                />
                            </div>
                            <v-select
                            v-if="predictedKomponente == ''"
                            :items="datenpunktNochNichtMöglichNochNichtMöglich" 
                            v-model="predictedDatenpunkt" 
                            label= 'Datenpunkt' 
                            @update:model-value="changeDatenpunkt"
                            />
                        </v-col>
                        <v-col cols="4" class="d-flex justify-center align-center">
                            <v-btn
                            class="ma-1"
                            v-bind="props"
                            variant="outlined"
                            color = "warning"
                            @click ="updataDatenpunktBasyx()">
                            Submit
                            </v-btn>
                        </v-col>
                    </v-row>
                    <div class="d-flex flex-column align-center">
                        <v-card-actions>
                            <v-btn
                                variant="outlined"
                                color = "warning"
                                @click="dialog = false"
                            >
                                Close
                            </v-btn>
                        </v-card-actions>
                    </div>
                    <v-container>
                        <div v-if="digitalTwinStore.showProgressEditDatenpunkt === true">
                            <v-progress-linear
                            indeterminate
                            color="success"
                            ></v-progress-linear>
                        </div>
                    </v-container>
                </v-container>
        </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { useDigitalTwinsStore } from "@/store/digitaltwins"

export default {

    data () {
      return {
        dialog: false,
        predictedGrundfunktion: '',
        predictedZweiteEbene: '',
        predictedKomponente: '',
        predictedDatenpunkt: '',
        predictedGrundfunktionScore: 0,
        predictedZweiteEbeneScore: 0,
        predictedKomponenteScore: 0,
        predictedDatenpunktScore: 0,
        grundfunktionen: ['Wärme versorgen', 'Luft versorgen', 'Kälte versorgen', 'Medien versorgen', 'Strom versorgen', 'Sichern'],
        zweiteEbeneDict: {
            'Wärme versorgen': ['Wärme erzeugen', 'Wärme verteilen', 'Wärme beziehen', 'Wärme speichern'],
            'WaermeVersorgen': ['Wärme erzeugen', 'Wärme verteilen', 'Wärme beziehen', 'Wärme speichern'],
            'Luft versorgen': ['Luft bereitstellen', 'Luft verteilen'],
            'LuftVersorgen': ['Luft bereitstellen', 'Luft verteilen']
        },
        komponentenEbeneDict: {
            'Wärme verteilen': ['Heizkreis allgemein', 'Vorlauf', 'Rücklauf', 'Pumpe', 'Ventil', 'Wärmemengenzähler'],
            'Verteilen': ['Heizkreis allgemein', 'Vorlauf', 'Rücklauf', 'Pumpe', 'Ventil', 'Wärmemengenzähler'],
            'Wärme erzeugen': ['BHKW', 'Kessel', 'Pelletkessel', 'Wärmepumpe', 'Wärmeversorger allgemein'],
            'Erzeugen': ['BHKW', 'Kessel', 'Pelletkessel', 'Wärmepumpe', 'Wärmeversorger allgemein'],
            'Wärme beziehen': ['Fernwärme'],
            'Beziehen': ['Fernwärme'],
            'Wärme speichern': ['Speicher'],
            'Speichern': ['Speicher'],
            'Luft bereitstellen': ['Abluft allgemein', 'Abluftfilter','Abluftklappe', 'Ablufventilator', 'Außenluftfilter', 
            'Außenluftklappe','Befeuchter', 'Erhitzer', 'Filter', 'Fortluftklappe', 'Gerät allgemein', 'Kühler', 'Ventilator', 'Wärmerückgewinnung', 'Zuluft allgemein',
            'Zuluftventilator', 'Zuluftfilter', 'Zuluftklappe'],
            'LuftBereitstellen': ['Abluft allgemein', 'Abluftfilter','Abluftklappe', 'Ablufventilator', 'Außenluftfilter', 
            'Außenluftklappe','Befeuchter', 'Erhitzer', 'Filter', 'Fortluftklappe', 'Gerät allgemein', 'Kühler', 'Ventilator', 'Wärmerückgewinnung', 'Zuluft allgemein',
            'Zuluftventilator', 'Zuluftfilter', 'Zuluftklappe'],
            'Luft verteilen': ['Auslass', 'Raum', 'Volumenstromregler Abluft', 'Volumenstromregler Raum', 'Volumenstromregler Zuluft'],
            'LuftVerteilen': ['Auslass', 'Raum', 'Volumenstromregler Abluft', 'Volumenstromregler Raum', 'Volumenstromregler Zuluft'],
        },
        zweiteGrundfunktionNochNichtMöglich: [],
        komponenteNochNichtMöglich: [],
        datenpunktNochNichtMöglich: [],
        datenpunktEbeneDict: {
            'Fernwärme': ['Alarmmeldung', 'Anforderung', 'Messwert Außentemperatur', 'Betriebsstunden Pumpe', 'Grenzwert Vorlauftemperatur Sekundär', 'Sollwert Maximale Vorlauftemperatur', 'Sollwert Minimale Vorlauftemperatur', 'Offset Vorlauftemperatur',
            'Regler', 'Messwert Rücklauftemperatur Primär', 'Messwert Rücklauftemperatur Sekundär', 'Rückmeldung Handschaltung Ventil', 'Rückmeldung Handschaltung Klappe', 'Rückmeldung Betriebsart', 'Rückmeldung Ventil Rücklauf',
            'Sollwert Außentemperatur Maximal Tag', 'Sollwert Nachlaufzeit Pumpe', 'Schaltbefehl Anlage', 'Schaltbefehl Pumpe', 'Sollwert Vorlauftemperatur', 'Stellbefehl Ventil', 'Störmeldung', 'Messwert Vorlauftemperatur Sekundär',
            'Zähler', 'Messwert Vorlauftemperatur Primär', 'Grenzwert Rücklauftemperatur Sekundär', 'Rückmeldung Handschaltung Fernwärme', 'Rückmeldung Stellsignal'],
            
            'Fernwaerme': ['Alarmmeldung', 'Anforderung', 'Messwert Außentemperatur', 'Betriebsstunden Pumpe', 'Grenzwert Vorlauftemperatur Sekundär', 'Sollwert Maximale Vorlauftemperatur', 'Sollwert Minimale Vorlauftemperatur', 'Offset Vorlauftemperatur',
            'Regler', 'Messwert Rücklauftemperatur Primär', 'Messwert Rücklauftemperatur Sekundär', 'Rückmeldung Handschaltung Ventil', 'Rückmeldung Handschaltung Klappe', 'Rückmeldung Betriebsart', 'Rückmeldung Ventil Rücklauf',
            'Sollwert Außentemperatur Maximal Tag', 'Sollwert Nachlaufzeit Pumpe', 'Schaltbefehl Anlage', 'Schaltbefehl Pumpe', 'Sollwert Vorlauftemperatur', 'Stellbefehl Ventil', 'Störmeldung', 'Messwert Vorlauftemperatur Sekundär',
            'Zähler', 'Messwert Vorlauftemperatur Primär', 'Grenzwert Rücklauftemperatur Sekundär', 'Rückmeldung Handschaltung Fernwärme', 'Rückmeldung Stellsignal'],
            
            'Speicher': ['Externe Vorrangschaltung Aktiv', 'Rückmeldung Zeitplan', 'Sollwert Maximale Hysterese Speichertemperatur', 'Sollwert Speichertemperatur', 'Sollwert Speichertemperatur Unten', 'Messwert Speichertemperatur', 'Messwert Speichertemperatur Mitte',
                'Messwert Speichertemperatur Oben', 'Messwert Speichertemperatur Unten', 'Störmeldung', 'Rückmeldung Zeitplan'],
            
            'Kessel': ['Anforderung', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Druck', 'Freigabe', 'Messwert Temperatur', 'Regler', 'Reset Betriebsstunden', 'Rückmeldung Betrieb', 'Rückmeldung Klappe', 'Rückmeldung Stellsignal',
                'Rückmeldung Handschaltung', 'Rückmeldung Leistung', 'Rückmeldung Not Aus', 'Schaltbefehl Not Aus', 'Sollwert Temperatur', 'Sollwert Wartezeit', 'Sollwert Leistung', 'Schaltbefehl Anlage', 'Stellbefehl Anlage', 'Störmeldung', 'Überhöhung Kesselanlage',
                'Wartungsmeldung', 'Sollwert Einschaltverzögerung', 'Sollwert Abschaltung', 'Schaltbefehl Klappe'],
            
            'BHKW': ['Betriebsstunden', 'Laufzeit Nächste Wartung', 'Messwert Abgastemperatur', 'Messwert Gasverbrauch', 'Messwert Spannung', 'Messwert Strom', 'Messwert Temperatur Generator', 'Rückmeldung Ölnachspeisung Aktiv',
                'Rückmeldung Start', 'Rückmeldung Handschaltung', 'Rückmeldung Batterie', 'Schaltbefehl Anlage', 'Störmeldung', 'Warnmeldung', 'Wartungsmeldung', 'Rückmeldung Betrieb'],
            
            'Wärmepumpe': ['Rückmeldung Handschaltung Brunnenpumpe', 'Rückmeldung Betriebsbereit', 'Rückmeldung Betriebsbereit', 'Rückmeldung Blockierschutz Umwälzpumpe', 'Rückmeldung Blockierschutz Brunnenpumpe', 'Rückmeldung Umschaltventil Zu',
                'Störmeldung', 'Zähler-Volumenstrom-Förderbrunnen'],
            
            'Waermepumpe': ['Rückmeldung Handschaltung Brunnenpumpe', 'Rückmeldung Betriebsbereit', 'Rückmeldung Betriebsbereit', 'Rückmeldung Blockierschutz Umwälzpumpe', 'Rückmeldung Blockierschutz Brunnenpumpe', 'Rückmeldung Umschaltventil Zu',
                'Störmeldung', 'Zähler-Volumenstrom-Förderbrunnen'],
            
            'Pelletkessel': ['Rückmeldung Schnecke Leer', 'Rückmeldung Betrieb', 'Messwert Außentemperatur', 'Messwert Primärluft', 'Restsauerstoff', 'Messwert Temperatur Einschubrohr'],
            
            'Pumpe': ['Anzahl-Schaltungen', 'Betriebsstunden', 'Messwert Durchfluss', 'Messwert Energieverbrauch', 'Messwert Leistungsaufnahme', 'Messwert Stromaufnahme', 'Messwert Drehzahl', 'Reset Betriebsstunden', 'Rückmeldung Handschaltung Pumpe',
                'Rückmeldung Betrieb', 'Schaltbefehl', 'Schaltbefehl Blockierschutz', 'Sollwert Frostschutz', 'Sollwert Laufzeit Blockierschutz', 'Sollwert Nacht', 'Sollwert Nachlaufzeit', 'Sollwert Tag', 'Status Übersteuern Ein', 'Störmeldung', 'Wartungsintervall'],
            
            'Ventil': ['Handschaltung', 'Laufzeit 3 Punkt Antrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Sollwert Stellsignal Min', 'Sollwert Stellsignal Max', 'Stellbefehl', 'Störmeldung', 'Stellbefehl Max', 'Stellbefehl Min',
                'Sollwert Mischventil', 'Laufzeit Ventil'],

            'Raum': ['Freigabe Heizung', 'Freigabe Raumkorrektur', 'Freigabe Stützbetrieb Nacht Ventil', 'Freigabe Stützbetrieb', 'Freigabe Stützbetrieb Tag Ventil', 'Freigabe Stellantrieb', 'Freigabe Zeitprogramm', 'Messwert Raumtemperatur',
                'Rückmeldung Normalbetrieb', 'Rückmeldung Ventil Handschaltung', 'Schaltbefehl Raumkorrektur', 'Sollwert Raumkorrektur', 'Sollwert Raumtemperatur Tag', 'Sollwert Raumtemperatur Nacht', 'Sollwert minimale Raumtemperatur',
                'Sollwertverschiebung', 'Sollwert Stützbetrieb Tag', 'Sollwert Stützbetrieb Nacht', 'Sollwert Aufheizbetrieb', 'Stellbefehl', 'Aktivierung Raumoptimierung', 'Rückmeldung Aufheizbetrieb', 'Rückmeldung Absenkbetrieb'],
            
            'Vorlauf': ['Anhebung Vorlauftemperatur', 'Messwert Vorlauftemperatur', 'Sollwert Vorlauftemperatur', 'Sollwert Maximale Vorlauftemperatur', 'Sollwert Minimale Vorlauftemperatur', 'Sollwert Nachtabsenkung Vorlauftemperatur',
            'Störmeldung', 'Rückmeldung Sollwertabweichung Vorlauftemperatur', 'Sollwertkorrektur Vorlauftemperatur'],
            
            'Rücklauf': ['Messwert Rücklauftemperatur', 'Sollwert Maximale Rücklauftemperatur', 'Sollwert Minimale Rücklauftemperatur', 'Sollwert Rücklauftemperatur', 'Rohrheizung'],
            
            'Ruecklauf': ['Messwert Rücklauftemperatur', 'Sollwert Maximale Rücklauftemperatur', 'Sollwert Minimale Rücklauftemperatur', 'Sollwert Rücklauftemperatur', 'Rohrheizung'],
            
            'Heizkreis allgemein': ['Alarmmeldung', 'Aktuelle Leistung', 'Grenzwert Frost', 'Heizkurve', 'Messwert Außentemperatur', 'Regler', 'Rückmeldung Nutzzeitverlängerung', 'Schaltbefehl Anlage', 'Schaltbefehl Nutzzeitverlängerung',
                'Schaltbefehl Nachtabsenkung', 'Sollwert Maximale Aufheizzeit', 'Sollwert Aufheizzeit', 'Sollwert Nachtabsenkung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Speicherfähigkeit', 'Sollwert Stützbetrieb Tag', 'Sollwert Überhöhung Hydraulische Weiche',
                'Stützbetrieb Nacht Erreicht', 'Warmwasserbereitung', 'Parallelverschiebung', 'Rückmeldung Tagbetrieb', 'Störmeldung', 'Wärmemengenzähler', 'Sollwert Minimale Außentemperatur', 'Sollwert Außentemperatur', 'Rückmeldung Betriebsart',
                'Rückmeldung Zeitplan', 'Rückmeldung Regelabweichung', 'Sollwert Abschalten Stützbetrieb', 'Schaltbefehl Start Stop Optimierung', 'Schaltbefehl Gleitendes Schalten', 'Schaltbefehl Zeitprogramm'],
            'HeizkreisAllgemein': ['Alarmmeldung', 'Aktuelle Leistung', 'Grenzwert Frost', 'Heizkurve', 'Messwert Außentemperatur', 'Regler', 'Rückmeldung Nutzzeitverlängerung', 'Schaltbefehl Anlage', 'Schaltbefehl Nutzzeitverlängerung',
                'Schaltbefehl Nachtabsenkung', 'Sollwert Maximale Aufheizzeit', 'Sollwert Aufheizzeit', 'Sollwert Nachtabsenkung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Speicherfähigkeit', 'Sollwert Stützbetrieb Tag', 'Sollwert Überhöhung Hydraulische Weiche',
                'Stützbetrieb Nacht Erreicht', 'Warmwasserbereitung', 'Parallelverschiebung', 'Rückmeldung Tagbetrieb', 'Störmeldung', 'Wärmemengenzähler', 'Sollwert Minimale Außentemperatur', 'Sollwert Außentemperatur', 'Rückmeldung Betriebsart',
                'Rückmeldung Zeitplan', 'Rückmeldung Regelabweichung', 'Sollwert Abschalten Stützbetrieb', 'Schaltbefehl Start Stop Optimierung', 'Schaltbefehl Gleitendes Schalten', 'Schaltbefehl Zeitprogramm'],

            'AbluftAllgemein': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Luftqualität', 'Messwert Volumenstrom', 'Rückmeldung Handschaltung', 'Rückmeldung Nutzzeitverlängerung',
                'Rückmeldung Ventil', 'Rückmeldung Zeitplan', 'Schaltbefehl Anlage', 'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Temperatur', 'Sollwert CO2 Konzentration', 'Sollwert Volumenstrom', 'Störmeldung',
                'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch', 'Warnmeldung Temperatur Niedrig', 'Wartungsmeldung'],
            'Abluft allgemein': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Luftqualität', 'Messwert Volumenstrom', 'Rückmeldung Handschaltung', 'Rückmeldung Nutzzeitverlängerung',
                'Rückmeldung Ventil', 'Rückmeldung Zeitplan', 'Schaltbefehl Anlage', 'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Temperatur', 'Sollwert CO2 Konzentration', 'Sollwert Volumenstrom', 'Störmeldung',
                'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch', 'Warnmeldung Temperatur Niedrig', 'Wartungsmeldung'],
            
            'Abluftventilator': ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlausführungskontrolle', 'Betriebsstunden', 'Messwert Differenzdruck', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Rückmeldung Nutzzeitverlängerung',
                'Rückmeldung Handschaltung', 'Rückmeldung Reperaturschalter', 'Rückmeldung Betrieb', 'Rückmeldung Zeitplan', 'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert FU', 'Stellbefehl', 'Störmeldung'],
            
            'Zuluftventilator': ['Alarmmeldung', 'Anzahl Schaltungen', 'Befehlausführungskontrolle', 'Betriebsstunden', 'Messwert Differenzdruck', 'Messwert Volumenstrom', 'Reset Betriebsstunden', 'Rückmeldung Drehzahl',
                'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Handschaltung', 'Rückmeldung Reperaturschalter', 'Rückmeldung Stellsignal', 'Rückmeldung Betrieb', 'Rückmeldung Zeitplan', 'Rückmeldung Laufüberwachung',
                'Schaltbefehl', 'Sollwert Laufzeit', 'Sollwert Stellsignal', 'Stellbefehl', 'Störmeldung', 'Wartungsmeldung'],
            
            'ZuluftAllgemein': ['Alarmmeldung Frostschutz', 'Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Luftqualität', 'Messwert Volumenstrom', 'Rückmeldung Handschaltung',
                'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Ventil', 'Rückmeldung Zeitplan', 'Rückmeldung Grenzwert Soll Ist Abweichung Temperatur', 'Sollwert Grenzwert Soll Ist Abweichung Temperatur', 'Schaltbefehl Anlage',
                'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Feuchte Max', 'Sollwert Feuchte Min', 'Sollwert Frostschutz', 'Sollwert Temperatur', 'Sollwert Temperatur Min', 'Sollwert Temperatur Max', 'Sollwert CO2-Konzentration',
                'Sollwert CO2-Konzentration Max', 'Sollwert Volumenstrom', 'Sollwert Volumenstrom Max', 'Sollwert Volumenstrom Min', 'Störmeldung', 'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch',
                'Warnmeldung Temperatur Niedrig', 'Wartungsmeldung'],
            'Zuluft allgemein': ['Alarmmeldung Frostschutz', 'Alarmmeldung', 'Befehlsausführkontrolle', 'Messwert Druck', 'Messwert Feuchte', 'Messwert Temperatur', 'Messwert Luftqualität', 'Messwert Volumenstrom', 'Rückmeldung Handschaltung',
                'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Ventil', 'Rückmeldung Zeitplan', 'Rückmeldung Grenzwert Soll Ist Abweichung Temperatur', 'Sollwert Grenzwert Soll Ist Abweichung Temperatur', 'Schaltbefehl Anlage',
                'Sollwert Druck', 'Sollwert Feuchte', 'Sollwert Feuchte Max', 'Sollwert Feuchte Min', 'Sollwert Frostschutz', 'Sollwert Temperatur', 'Sollwert Temperatur Min', 'Sollwert Temperatur Max', 'Sollwert CO2-Konzentration',
                'Sollwert CO2-Konzentration Max', 'Sollwert Volumenstrom', 'Sollwert Volumenstrom Max', 'Sollwert Volumenstrom Min', 'Störmeldung', 'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch',
                'Warnmeldung Temperatur Niedrig', 'Wartungsmeldung'],

            'Klappe': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Störmeldung', 'Stellbefehl', 'Sollwert Stellsignal'],
            'Außenluftklappe': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Störmeldung', 'Stellbefehl', 'Sollwert Stellsignal'],
            'Abluftklappe': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Störmeldung', 'Stellbefehl', 'Sollwert Stellsignal'],
            'Fortluftklappe': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Störmeldung', 'Stellbefehl', 'Sollwert Stellsignal'],
            'Zuluftklappe': ['Alarmmeldung', 'Befehlsausführkontrolle', 'Rückmeldung Betrieb', 'Rückmeldung Klappe Auf', 'Rückmeldung Klappe Zu', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Störmeldung', 'Stellbefehl', 'Sollwert Stellsignal'],

            'Befeuchter': ['Rückmeldung Betrieb', 'Betriebsstunden', 'Sollwert Befeuchten', 'Stellbefehl', 'Störmeldung', 'Schaltbefehl'],

            'Erhitzer': ['Alarmmeldung', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Durchfluss', 'Messwert Energieverbrauch', 'Messwert Leistungsaufnahme', 'Messwert Rücklauftemperatur', 'Messwert Stromaufnahme', 'Messwert Vorlauftemperatur', 'Messwert Drehzahl', 'Reset Betriebsstunden', 'Rückmeldung Handschaltung Pumpe', 'Rückmeldung Handschaltung Ventil', 'Rückmeldung Betrieb', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Schaltbefehl Blockierschutz', 'Schaltbefehl Frostschutz', 'Sollwert Frostschutz', 'Sollwert Laufzeit Blockierschutz', 'Sollwert Nacht', 'Sollwert Nachlaufzeit', 'Sollwert Dauerfreigabe', 'Sollwert Tag', 'Status Übersteuern-Ein', 'Stellbefehl Ventil', 'Störmeldung', 'Wartungsintervall', 'Wartungsmeldung', 'Grenzwert Rücklauftemperatur'],
            
            'Filter': ['Messwert Druck', 'Wartungsmeldun -Abluft', 'Wartungsmeldung Zuluft', 'Wartungsmeldung Fortluft', 'Wartungsmeldung Außenluft', 'Wartungsmeldung Filter', 'Störmeldung'],
            'Abluftfilter': ['Messwert Druck', 'Wartungsmeldun -Abluft', 'Wartungsmeldung Zuluft', 'Wartungsmeldung Fortluft', 'Wartungsmeldung Außenluft', 'Wartungsmeldung Filter', 'Störmeldung'],
            'Außenluftfilter': ['Messwert Druck', 'Wartungsmeldun -Abluft', 'Wartungsmeldung Zuluft', 'Wartungsmeldung Fortluft', 'Wartungsmeldung Außenluft', 'Wartungsmeldung Filter', 'Störmeldung'],
            'Zuluftfilter': ['Messwert Druck', 'Wartungsmeldun -Abluft', 'Wartungsmeldung Zuluft', 'Wartungsmeldung Fortluft', 'Wartungsmeldung Außenluft', 'Wartungsmeldung Filter', 'Störmeldung'],

            'Kühler': ['Alarm Frostschutz', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Rücklauftemperatur', 'Messwert Vorlauftemperatur', 'Rückmeldung Klappe Auf', 'Rückmeldung Betrieb', 'Rückmeldung Stellsignal', 'Sollwert Kühlbedarf', 'Stellbefehl Ventil', 'Zählwert Kühlwasser', 'Zählwert Kältemenge'],
            'Kuehler': ['Alarm Frostschutz', 'Anzahl Schaltungen', 'Betriebsstunden', 'Messwert Rücklauftemperatur', 'Messwert Vorlauftemperatur', 'Rückmeldung Klappe Auf', 'Rückmeldung Betrieb', 'Rückmeldung Stellsignal', 'Sollwert Kühlbedarf', 'Stellbefehl Ventil', 'Zählwert Kühlwasser', 'Zählwert Kältemenge'],

            'Raum RLT':['Alarmmeldung', 'Alarme Zurück Gestellt', 'Betriebsmeldung Präsenzmelder', 'Messwert Feuchte', 'Messwert CO2', 'Messwert Raumtemperatur', 'Rückmeldung Betrieb', 'Rückmeldung Ventil', 'Rückmeldung Klappe Auf', 'Rückmeldung Kommunikation', 'Sollwert Ausschaltverzögerung', 'Sollwert Einschaltverzögerung', 'Sollwert CO2', 'Sollwert CO2 Max', 'Sollwert Feuchte', 'Sollwert Raumtemperatur', 'Störmeldung', 'Warnmeldung CO2 Hoch', 'Warnmeldung Feuchte', 'Warnmeldung Temperatur Hoch', 'Warnmeldung Temperatur Niedrig'],

            'VolumenstromreglerAbluft': ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung'],
            'Volumenstromregler Abluft': ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung'],
            'VolumenstromreglerZuluft': ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung'],
            'Volumenstromregler Zuluft': ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung'],
            'VolumenstromreglerRaum': ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung'],
            'Volumenstromregler Raum': ['Schaltbefehl', 'Rückmeldung Stellsignal', 'Stellbefehl', 'Rückmeldung Handschaltung'],

            'Gerät allgemein': ['Alarmmeldung', 'Anforderung Tableau', 'Messwert Außentemperatur', 'Sollwert Kühlbedarf', 'Schaltbefehl Anlage', 'Übersteuert', 'Rückmeldung Anfahrbetrieb', 'Rückmeldung Batterie', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Quittierung', 'Rückmeldung Freie Nachtkühlung', 'Rückmeldung Ferienprogramm', 'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Restlaufzeit Nutzzeitverlängerung', 'Rückmeldung Spülen', 'Schaltbefehl Nachtkühlung', 'Schaltbefehl Optimierte Luftqualität', 'Schaltbefehl Tagesprogramm', 'Schaltbefehl Nutzzeitverlängerung', 'Sollwert Feuchte', 'Sollwert Spülzeit', 'Sollwert Freie-Nachtkühlung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Wärmebedarf', 'Sollwert Maximale Einschaltverzögerung', 'Störmeldung', 'Rückmeldung Anlage Fern', 'Schaltbefehl Anlage Fern'],
            'GeraetAllgemein': ['Alarmmeldung', 'Anforderung Tableau', 'Messwert Außentemperatur', 'Sollwert Kühlbedarf', 'Schaltbefehl Anlage', 'Übersteuert', 'Rückmeldung Anfahrbetrieb', 'Rückmeldung Batterie', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Quittierung', 'Rückmeldung Freie Nachtkühlung', 'Rückmeldung Ferienprogramm', 'Rückmeldung Nutzzeitverlängerung', 'Rückmeldung Restlaufzeit Nutzzeitverlängerung', 'Rückmeldung Spülen', 'Schaltbefehl Nachtkühlung', 'Schaltbefehl Optimierte Luftqualität', 'Schaltbefehl Tagesprogramm', 'Schaltbefehl Nutzzeitverlängerung', 'Sollwert Feuchte', 'Sollwert Spülzeit', 'Sollwert Freie-Nachtkühlung', 'Sollwert Nutzzeitverlängerung', 'Sollwert Wärmebedarf', 'Sollwert Maximale Einschaltverzögerung', 'Störmeldung', 'Rückmeldung Anlage Fern', 'Schaltbefehl Anlage Fern'],

            'Waermerueckgewinnung': ['Alarmmeldung', 'Messwert Temperatur Austritt Zuluft', 'Messwert Temperatur Eintritt Zuluft', 'Messwert Temperatur Eintritt Abluft', 'Messwert Temperatur Austritt Abluft', 'Messwert Vorlauftemperatur', 'Pumpe', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Frostschutz', 'Sollwert Stellsignal', 'Sollwert Stellsignal Min', 'Sollwert Stellsignal Max', 'Stellbefehl', 'Stellbefehl WRG Bypass', 'Störmeldung'],
            'Wärmerückgewinnung': ['Alarmmeldung', 'Messwert Temperatur Austritt Zuluft', 'Messwert Temperatur Eintritt Zuluft', 'Messwert Temperatur Eintritt Abluft', 'Messwert Temperatur Austritt Abluft', 'Messwert Vorlauftemperatur', 'Pumpe', 'Rückmeldung Betrieb', 'Rückmeldung Handschaltung', 'Rückmeldung Stellsignal', 'Schaltbefehl', 'Sollwert Frostschutz', 'Sollwert Stellsignal', 'Sollwert Stellsignal Min', 'Sollwert Stellsignal Max', 'Stellbefehl', 'Stellbefehl WRG Bypass', 'Störmeldung'],
        },
      }
    },
    props: {
        datenpunkt: Object
    },
    
    created() {

        if (this.datenpunkt['GrundfunktionValue'] == 'WaermeVersorgen') {
            this.predictedGrundfunktion = 'Wärme versorgen'
        } else if (this.datenpunkt['GrundfunktionValue'] == 'LuftVersorgen') {
            this.predictedGrundfunktion = 'Luft versorgen'
        } else {
            this.predictedGrundfunktion = this.datenpunkt['GrundfunktionValue']
        }
        
        if (this.datenpunkt['ZweiteEbeneValue'] == 'Verteilen') {
            this.predictedZweiteEbene = 'Wärme verteilen'
        } else if (this.datenpunkt['ZweiteEbeneValue'] == 'Erzeugen') {
            this.predictedZweiteEbene = 'Wärme erzeugen'
        } else if (this.datenpunkt['ZweiteEbeneValue'] == 'Beziehen') {
            this.predictedZweiteEbene = 'Wärme beziehen'
        } else if (this.datenpunkt['ZweiteEbeneValue'] == 'Speichern') {
            this.predictedZweiteEbene = 'Wärme speichern'
        } else if (this.datenpunkt['ZweiteEbeneValue'] == 'LuftVerteilen') {
            this.predictedZweiteEbene = 'Luft verteilen'
        } else if (this.datenpunkt['ZweiteEbeneValue'] == 'LuftBereitstellen') {
            this.predictedZweiteEbene = 'Luft bereitstellen'
        } else {
            this.predictedZweiteEbene = this.datenpunkt['ZweiteEbeneValue']
        }
        
        if (this.datenpunkt['KomponentenEbeneValue'] == 'Fernwaerme') {
            this.predictedKomponente = 'Fernwärme'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'Waermepumpe') {
            this.predictedKomponente = 'Wärmepumpe'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'Ruecklauf') {
            this.predictedKomponente = 'Rücklauf'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'HeizkreisAllgemein') {
            this.predictedKomponente = 'Heizkreis allgemein'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'AbluftAllgemein') {
            this.predictedKomponente = 'Abluft allgemein'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'ZuluftAllgemein') {
            this.predictedKomponente = 'Zuluft allgemein'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'Kuehler') {
            this.predictedKomponente = 'Kühler'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'VolumenstromreglerAbluft') {
            this.predictedKomponente = 'Volumenstromregler Abluft'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'VolumenstromreglerZuluft') {
            this.predictedKomponente = 'Volumenstromregler Zuluft'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'VolumenstromreglerRaum') {
            this.predictedKomponente = 'Volumenstromregler Raum'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'Waermerueckgewinnung') {
            this.predictedKomponente = 'Wärmeräckgewinnung'
        } else if (this.datenpunkt['KomponentenEbeneValue'] == 'GeraetAllgemein') {
            this.predictedKomponente = 'Gerät allgemein'
        } else {
            this.predictedKomponente = this.datenpunkt['KomponentenEbeneValue']
        }

        //this.predictedGrundfunktion = this.datenpunkt['GrundfunktionValue']
        //this.predictedZweiteEbene = this.datenpunkt['ZweiteEbeneValue']
        // this.predictedKomponente = this.datenpunkt['KomponentenEbeneValue']
        this.predictedDatenpunkt = this.datenpunkt['DatenpunktEbeneValue']
        this.predictedGrundfunktionScore = this.datenpunkt['GrundfunktionScore']
        this.predictedZweiteEbeneScore = this.datenpunkt['ZweiteEbeneScore']
        this.predictedKomponenteScore = this.datenpunkt['KomponentenEbeneScore']
        this.predictedDatenpunktScore = this.datenpunkt['DatenpunktEbeneScore']
    },
    methods: {
        changeGrundfunktion () {
            this.predictedGrundfunktionScore = 1.0
            this.predictedZweiteEbeneScore = 0
            this.predictedZweiteEbene = ''
            this.predictedKomponente = ''
            this.predictedKomponenteScore = 0
            this.predictedDatenpunkt = ''
            this.predictedDatenpunktScore = 0
        },
        changeZweiteEbene () {
            this.predictedZweiteEbeneScore = 1
            this.predictedKomponente = ''
            this.predictedKomponenteScore = 0
            this.predictedDatenpunkt = ''
            this.predictedDatenpunktScore = 0
        },
        changeKomponente () {
            this.predictedKomponenteScore = 1.0
            this.predictedDatenpunkt = ''
            this.predictedDatenpunktScore = 0
        },
        changeDatenpunkt () {
            this.predictedDatenpunktScore = 1.0
        },
        async editZweiteEbene () {
            const result = await this.digitalTwinStore.editDatenpunktGrundfunktion(this.datenpunkt, this.predictedGrundfunktion)
            console.log(result)
            this.$emit('editNlp')
        },
        async editKomponente () {
            const result = await this.digitalTwinStore.editDatenpunktZweiteEbene(this.datenpunkt, this.predictedGrundfunktion, this.predictedZweiteEbene)
            console.log(result)
            this.$emit('editNlp')
        },
        async editDatenpunkt () {
            const result = await this.digitalTwinStore.editDatenpunktKomponente(this.datenpunkt, this.predictedGrundfunktion, this.predictedZweiteEbene, this.predictedKomponente)
            console.log(result)
            this.$emit('editNlp')
        },
        async updataDatenpunktBasyx () {
            const result = await this.digitalTwinStore.editDatenpunkt(this.datenpunkt, this.predictedGrundfunktion, this.predictedZweiteEbene, this.predictedKomponente, this.predictedDatenpunkt)
            console.log(result)
            this.$emit('editNlp')
        }
    },    
    computed: {
        digitalTwinStore () {
        return useDigitalTwinsStore()
        }
    }
}
</script>

<style>
.two-line-title {
  max-height: 3em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
}
#text-field-edit-orga {
  width: 70%;
  align-self: center;
}
</style>