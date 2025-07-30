<template>
    <div>
        <!--
        <h1>Digital Twins - General</h1>
        <p> Wähle einen Standort aus, den du sehen möchtest</p>
        <div v-for="site in sites" :key="site.id" >
        <router-link :to="{name:'DigitalTwins_Site', params:{siteid:site.name}}">
            <h2>{{ site.name }}</h2>
        </router-link>  
        </div>
    -->
        <v-container>
            <!--<h2 style="color: #3B5249;">Digital Twins - Übersicht</h2>-->
            <!--
            <v-btn
            @click="generalStore.addBacnetDevice()">Create Bacnet
            </v-btn>
        -->
            <v-row>
                <v-col cols="6" v-for="site in generalStore.loadedSiteInformationWithBuildings" :key="Object.keys(site)[0]">
                    <DigitalTwinOverview :site="site"/>
                </v-col>
            </v-row>
            <!--<GatewayInformation />-->
        </v-container>
    </div>
</template> 

<script>
import { useGeneralStore } from "@/store/general"
import DigitalTwinOverview from "@/components/digitalTwin/DigitalTwinOverview.vue"
//import GatewayInformation from "@/components/digitalTwin/GatewayInformation.vue"

export default{
    setup(){
        // das hier dann aus deinem store laden:
        const sites=[ {name:"Köln",id:"1"},{name:"Hamburg",id:"2"} ]
    return{sites}},
    components: {
        DigitalTwinOverview, 
        //GatewayInformation
    },
    computed: {
        generalStore () {
            return useGeneralStore()
        }
    }
}

</script>