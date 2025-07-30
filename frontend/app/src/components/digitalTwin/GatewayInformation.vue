<template>
    <v-container>
        <v-row>
            <v-col cols="6" v-for="gateway in generalStore.loadedBacnetInformationNotAssigned" :key="gateway['AAS ID']">
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
                    <BuildingForGateway :buildingsList="buildingsList" :gateway="gateway" :buildingsIdsWithSelectName="buildingsIdsWithSelectName"/>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>


<script>
import { useGeneralStore } from "@/store/general"
import BuildingForGateway from "@/components/digitalTwin/BuildingForGateway.vue"

export default{
    data () {
      return {
        // choosedBuilding: '',
        // buildingsIdsWithSelectName: {},
        // buildingsList: []
      }
    },    
    components: {
        BuildingForGateway
    },
    /*
    mounted() {
        this.loadBuildingInformation()
    },
    methods: {
        async loadBuildingInformation() {
            let buildingsIdsWithSelectName = {}
            let buildingsList = []
            const semanticIdAasTypeBacnet = 'https://th-koeln.de/gart/BACnetDeviceAAS/1/0'    
            const aasBacnetIds = await this.generalStore.getAasByType(semanticIdAasTypeBacnet)
            await this.generalStore.loadBacnetInformation(aasBacnetIds)

            for (let site in this.generalStore.loadedSiteInformationWithBuildings) {
                let siteInformation = this.generalStore.loadedSiteInformationWithBuildings[site]
                let siteName = siteInformation['siteName']
                console.log(siteInformation['buildings'])
                for (let building in siteInformation['buildings'][0]) {
                    console.log(building)
                    let buildingInformation = siteInformation['buildings'][0][building]
                    console.log(buildingInformation)
                    let buildingName = buildingInformation['buildingName']
                    console.log(buildingName)
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
    */
    computed: {
        generalStore () {
            return useGeneralStore()
        },
        buildingsIdsWithSelectName () {
            const buildingsIds = this.generalStore.buildingsIdsWithSelectName
            return buildingsIds
        },
        buildingsList () {
            const buildingsList = this.generalStore.buildingsList
            return buildingsList
        }
        /*
        buildingsList () {
            //let buildingsIdsWithSelectName = {}
            let buildingsList = []
            for (let site in this.generalStore.loadedSiteInformationWithBuildings) {
                let siteInformation = this.generalStore.loadedSiteInformationWithBuildings[site]
                let siteName = siteInformation['siteName']
                console.log(siteInformation['buildings'])
                for (let building in siteInformation['buildings'][0]) {
                    console.log(building)
                    let buildingInformation = siteInformation['buildings'][0][building]
                    console.log(buildingInformation)
                    let buildingName = buildingInformation['buildingName']
                    console.log(buildingName)
                    let siteBuildingName = buildingName + ', ' + siteName
                    buildingsList.push(siteBuildingName)
                    //this.$set(this.myObject, 'newKey', 'New Value')
                    //buildingsIdsWithSelectName.$set(building, siteBuildingName)
                }

                //buildingsList.push(buildingName)
            }
            return buildingsList
        }
        */
    }
}

</script>