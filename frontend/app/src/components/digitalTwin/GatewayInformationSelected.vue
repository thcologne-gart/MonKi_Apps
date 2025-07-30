<template>
    <v-container>
        <v-row>
            <v-col cols ="6" v-for="gateway in generalStore.loadedGatewayInformation" :key="gateway['AAS ID']">
                <v-card v-if="gateway['ParentAasIdShort'][0] == buildingId"
                style="border-radius: 20px; background-color: whitesmoke"
                variant="outlined"
                max-width="70%" class="mx-auto my-8">
                    <v-toolbar color="success">
                        <v-toolbar-title class="text-center" style="color: white; font-size: 20px">
                            {{ gateway['AAS ID Short'][0] }}
                        </v-toolbar-title>
                    </v-toolbar>
                    <v-divider></v-divider>
                    <v-card-text class="px-6 pb-0">
                        <v-row align="center" no-gutters class="mb-4">
                        <v-col cols="3"
                        style="font-size: 16px;">
                            Status:
                        </v-col>
                        <v-col cols="6">
                            <v-chip v-if ="gateway['Gateway Information']['Status'] == 'connected'" variant="outlined" color="monitoring">
                                {{ gateway['Gateway Information']['Status'] }}
                            </v-chip>
                            <v-chip v-else-if ="gateway['Gateway Information']['Status'] == 'disconnected'" variant="outlined" color="highlight">
                                {{ gateway['Gateway Information']['Status'] }}
                            </v-chip>
                            <v-chip v-else-if ="gateway['Gateway Information']['Status'] == 'never connected'" variant="outlined" color="warning">
                                {{ gateway['Gateway Information']['Status'] }}
                            </v-chip>
                        </v-col>
                        </v-row>
                    </v-card-text>
                    <v-expansion-panels 
                    v-for="(bacnetDevice, key) in gateway['bacnetDevices']" :key="key"
                    style="background-color: whitesmoke">
                        <v-expansion-panel elevation="0" rounded="0">
                            <v-expansion-panel-title style="font-size: 16px;" >{{ bacnetDevice['AAS ID Short'][0] }}</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div v-for="(property, key) in bacnetDevice['Digital Nameplate']" :key="key">
                                    <v-row>
                                        <v-col cols="6">
                                            {{ key }}:
                                        </v-col>
                                        <v-col cols ="6">
                                            {{ property }}
                                        </v-col>
                                    </v-row>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                    <v-divider></v-divider>
                    <!--
                    <v-card-actions v-if="gateway['NlpDone'] == false" class="d-flex justify-center align-center">
                        <v-btn class="max-3 mb-4"  variant="outlined" color="warning" 
                            @click= "digitalTwinStore.startNlp(gateway['AAS ID'], gateway['AAS ID Short']);
                            buildingName = ''">Classify Datapoints
                        </v-btn>
                    </v-card-actions>
                    <v-expansion-panels v-else-if ="gateway['NlpDone'] == true">
                        <v-expansion-panel @click="this.digitalTwinStore.getBasyxNlpSubmodel(gateway['AAS ID'], gateway['AAS ID Short'])" elevation="0" rounded="0">
                            <v-expansion-panel-title style="font-size: 18px;" >NLP Results</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <NlpResults />
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                -->
                </v-card>
            </v-col>
        </v-row>

        <v-row v-for="gateway in generalStore.loadedBacnetInformationAssigned" :key="gateway['AAS ID']">
            <v-col v-if="gateway['ParentAasIdShort'][0] == buildingId">
                <v-card max-width="70%" class="mx-auto my-8" elevation="1" rounded="0">
                    <v-toolbar color="success">
                        <v-toolbar-title class="text-center" style="color: white; font-size: 20px">
                            {{ gateway['AAS ID Short'][0] }}
                        </v-toolbar-title>
                    </v-toolbar>
                    <v-divider></v-divider>
                    <v-expansion-panels>
                        <v-expansion-panel elevation="0" rounded="0">
                            <v-expansion-panel-title style="font-size: 18px;" >Digital Nameplate</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div v-for="(property, key) in gateway['Digital Nameplate']" :key="key">
                                    <v-row>
                                        <v-col cols="6">
                                            {{ key }}:
                                        </v-col>
                                        <v-col cols ="6">
                                            {{ property }}
                                        </v-col>
                                    </v-row>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                    <v-divider></v-divider>
                    <v-card-actions v-if="gateway['NlpDone'] == false" class="d-flex justify-center align-center">
                        <v-btn class="max-3 mb-4"  variant="outlined" color="warning" 
                            @click= "digitalTwinStore.startNlp(gateway['AAS ID'], gateway['AAS ID Short']);
                            buildingName = ''">Classify Datapoints
                        </v-btn>
                    </v-card-actions>
                    <v-expansion-panels v-else-if ="gateway['NlpDone'] == true">
                        <v-expansion-panel @click="this.digitalTwinStore.getBasyxNlpSubmodel(gateway['AAS ID'], gateway['AAS ID Short'])" elevation="0" rounded="0">
                            <v-expansion-panel-title style="font-size: 18px;" >NLP Results</v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <NlpResults />
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import { useGeneralStore } from "@/store/general"
import { useDigitalTwinsStore } from "@/store/digitaltwins"
import NlpResults from "@/components/Nlp/NlpResults.vue"

export default{
    data () {
      return {
        datapointsClassified: false
      }
    },    
    mounted() {
        this.loadBuildingInformation()
    },
    props: {
        buildingId: String
    },
    components: {
        NlpResults
    },
    methods: {
        loadBuildingInformation() {
            this.digitalTwinStore.getSubmodel()
            let buildingsIdsWithSelectName = {}
            let buildingsList = []
            for (let site in this.generalStore.loadedSiteInformationWithBuildings) {
                let siteInformation = this.generalStore.loadedSiteInformationWithBuildings[site]
                let siteName = siteInformation['siteName']
                for (let building in siteInformation['buildings'][0]) {
                    let buildingInformation = siteInformation['buildings'][0][building]
                    let buildingName = buildingInformation['buildingName']
                    let siteBuildingName = buildingName + ', ' + siteName
                    buildingsList.push(siteBuildingName)
                    //this.$set(this.myObject, 'newKey', 'New Value')
                    buildingsIdsWithSelectName[building] = siteBuildingName
                }

                //buildingsList.push(buildingName)
            }
            this.buildingsList = buildingsList
            this.buildingsIdsWithSelectName = buildingsIdsWithSelectName
        }
    },
    computed: {
        generalStore () {
            return useGeneralStore()
        },
        digitalTwinStore () {
            return useDigitalTwinsStore()
        }
    }
}

</script>

<style scoped>
.transparent-background .v-expansion-panel {
  background-color: transparent !important;
}
</style>