<template>
    <div>
        <v-container v-if="parentAasIdShort == $route.params.buildingid">
            <v-row>
                <v-col v-for="grundfunktion in this.numberGrundfunktionen" :key="grundfunktion" cols = '6'>
                    <v-card max-width="70%" v-if="grundfunktion ==='WaermeVersorgen'" class="mx-auto my-8" elevation="0">
                        <v-card-title class="text-center">Wärme versorgen</v-card-title>
                        <v-divider class="mx-4" :thickness="3"></v-divider>
                        <div class="d-flex flex-column align-center">
                            <v-avatar size="112" rounded="0" class="ma-6">
                                <v-img class="mx-auto" max-width="78" href="#" contain :src="wärmePic[[Object.keys(wärmePic)[0]]]"></v-img>
                            </v-avatar>
                            <v-btn
                                class="max-3 mb-4" 
                                variant="outlined" 
                                color="warning"
                                @click="$router.push({name:'DigitalTwins_Site_Building_Grundfunktion', params:{siteid:siteId, buildingid: buildingId, bacnetid:this.digitalTwinStore.aasId, grundfunktion:grundfunktion}})"
                            >
                                Go to
                            </v-btn>
                        </div>
                    </v-card>
                    <v-card max-width="70%" v-else-if="grundfunktion ==='LuftVersorgen'" class="mx-auto my-8" elevation="0">
                        <v-card-title class="text-center">Luft versorgen</v-card-title>
                        <v-divider class="mx-4" :thickness="3"></v-divider>
                        <div class="d-flex flex-column align-center">
                            <v-avatar size="112" rounded="0" class="ma-6">
                                <v-img class="mx-auto" max-width="78" href="#" contain :src="luftPic[[Object.keys(luftPic)[0]]]"></v-img>
                            </v-avatar>
                            <v-btn
                                class="max-3 mb-4" 
                                variant="outlined" 
                                color="warning"
                                @click="$router.push({name:'DigitalTwins_Site_Building_Grundfunktion', params:{siteid:siteId, buildingid: buildingId, bacnetid:this.digitalTwinStore.aasId, grundfunktion:grundfunktion}})"
                            >
                                Go to
                            </v-btn>
                        </div>
                    </v-card>
                    <v-card max-width="70%" v-else-if="grundfunktion ==='KaelteVersorgen'" class="mx-auto my-8" elevation="0">
                        <v-card-title class="text-center">Kälte versorgen</v-card-title>
                        <v-divider class="mx-4" :thickness="3"></v-divider>
                        <div class="d-flex flex-column align-center">
                            <v-avatar size="112" rounded="0" class="ma-6">
                                <v-img class="mx-auto" max-width="78" href="#" contain :src="kältePic[[Object.keys(kältePic)[0]]]"></v-img>
                            </v-avatar>
                            <v-btn
                                class="max-3 mb-4" 
                                variant="outlined" 
                                color="warning"
                                @click="$router.push({name:'DigitalTwins_Site_Building_Grundfunktion', params:{siteid:siteId, buildingid: buildingId, bacnetid:this.digitalTwinStore.aasId, grundfunktion:grundfunktion}})"
                            >
                                Go to
                            </v-btn>
                        </div>
                    </v-card>
                    <v-card max-width="70%" v-else-if="grundfunktion ==='MedienVersorgen'" class="mx-auto my-8" elevation="0">
                        <v-card-title class="text-center">Medien versorgen</v-card-title>
                        <v-divider class="mx-4" :thickness="3"></v-divider>
                        <div class="d-flex flex-column align-center">
                            <v-avatar size="112" rounded="0" class="ma-6">
                                <v-img class="mx-auto" max-width="78" href="#" contain :src="medienPic[[Object.keys(medienPic)[0]]]"></v-img>
                            </v-avatar>
                            <v-btn
                                class="max-3 mb-4" 
                                variant="outlined" 
                                color="warning"
                                @click="$router.push({name:'DigitalTwins_Site_Building_Grundfunktion', params:{siteid:siteId, buildingid: buildingId,bacnetid:this.digitalTwinStore.aasId, grundfunktion:grundfunktion}})"
                            >
                                Go to
                            </v-btn>
                        </div>
                    </v-card>
                    <v-card max-width="70%" v-else-if="grundfunktion ==='Sichern'" class="mx-auto my-8" elevation="0">
                        <v-card-title class="text-center">Sichern</v-card-title>
                        <v-divider class="mx-4" :thickness="3"></v-divider>
                        <div class="d-flex flex-column align-center">
                            <v-avatar size="112" rounded="0" class="ma-6">
                                <v-img class="mx-auto" max-width="78" href="#" contain :src="sichernPic[[Object.keys(sichernPic)[0]]]"></v-img>
                            </v-avatar>
                            <v-btn
                                class="max-3 mb-4" 
                                variant="outlined" 
                                color="warning"
                                @click="$router.push({name:'DigitalTwins_Site_Building_Grundfunktion', params:{siteid:siteId, buildingid: buildingId,bacnetid:this.digitalTwinStore.aasId, grundfunktion:grundfunktion}})"
                            >
                                Go to
                            </v-btn>
                        </div>
                    </v-card>
                    <v-card max-width="70%" v-else-if="grundfunktion ==='StromVersorgen'" class="mx-auto my-8" elevation="0">
                        <v-card-title class="text-center">Strom versorgen</v-card-title>
                        <v-divider class="mx-4" :thickness="3"></v-divider>
                        <div class="d-flex flex-column align-center">
                            <v-avatar size="112" rounded="0" class="ma-6">
                                <v-img class="mx-auto" max-width="78" href="#" contain :src="stromPic[[Object.keys(stromPic)[0]]]"></v-img>
                            </v-avatar>
                            <v-btn
                                class="max-3 mb-4" 
                                variant="outlined" 
                                color="warning"
                                @click="$router.push({name:'DigitalTwins_Site_Building_Grundfunktion', params:{siteid:siteId, buildingid: buildingId,bacnetid:this.digitalTwinStore.aasId, grundfunktion:grundfunktion}})"
                            >
                                Go to
                            </v-btn>
                        </div>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
    <!--
    <div v-for="img in energyUseGroup" :key="img">
        <div>{{ Object.keys(img)[0] }}</div>
        <v-avatar max-size="44px" rounded="0" >
            <v-img class="mx-auto" max-width="60" href="#" contain :src="img[[Object.keys(img)[0]]]"></v-img>
        </v-avatar>
    </div>
    <div>{{ numberGrundfunktionen }}</div>
    <div>{{ wärmeVersorgen }}</div>
-->
</template>

<script>
import { useDigitalTwinsStore } from "@/store/digitaltwins"
import { useGeneralStore } from "@/store/general"

export default{
    data() {
        return {
            siteId: '',
            buildingId: '',
            parentIdShort: '',
            wärmePic: {'Wärme versorgen': Object.values(import.meta.glob('@/assets/Wärmeversorgen.svg', {as:'url', eager:true}))[0]},
            luftPic: {'Luft versorgen': Object.values(import.meta.glob('@/assets/Luftversorgen.svg', {as:'url', eager:true}))[0]},
            kältePic: {'Kälte versorgen': Object.values(import.meta.glob('@/assets/Kälteversorgen.svg', {as:'url', eager:true}))[0]},
            medienPic: {'Medien versorgen': Object.values(import.meta.glob('@/assets/Medienversorgen.svg', {as:'url', eager:true}))[0]},
            sichernPic: {'Sichern': Object.values(import.meta.glob('@/assets/Sichern.svg', {as:'url', eager:true}))[0]},
            stromPic: {'Strom versorgen': Object.values(import.meta.glob('@/assets/Stromversorgen.svg', {as:'url', eager:true}))[0]}
        };
    },
    mounted() {
        const site_id = this.$route.params.siteid
        this.siteId = site_id
        const building_id = this.$route.params.buildingid
        this.buildingId = building_id
        //this.getParentAasIdShort ()
    },
    /*
    methods: {
        async getParentAasIdShort () {
            const aasId = this.digitalTwinStore.aasId
            console.log(aasId)
            const parent = await this.generalStore.getBomParent(aasId)
            console.log(parent)
            const parentIdShort = await this.generalStore.getAasIdShortByIdentifier(parent[0])
            console.log(parentIdShort)
            this.parentIdShort = parentIdShort[0]
        },
    },
    */
    computed: {
        digitalTwinStore () {
        return useDigitalTwinsStore()
        },
        generalStore () {
            return useGeneralStore()
        },
        wärmeVersorgen () {
            const wärmeVersorgen = this.digitalTwinStore.wärmeVersorgen
            return wärmeVersorgen
        },
        luftVersorgen () {
            const luftVersorgen = this.digitalTwinStore.luftVersorgen
            return luftVersorgen
        },
        medienVersorgen () {
            const medienVersorgen = this.digitalTwinStore.medienVersorgen
            return medienVersorgen
        },
        kälteVersorgen () {
            const kälteVersorgen = this.digitalTwinStore.kälteVersorgen
            return kälteVersorgen
        },
        sichern () {
            const sichern = this.digitalTwinStore.sichern
            return sichern
        },
        stromVersorgen () {
            const stromVersorgen = this.digitalTwinStore.stromVersorgen
            return stromVersorgen
        },
        numberGrundfunktionen () {
            const allElements = this.digitalTwinStore.allNlpSubmodelElements
            const grundfunktionen = []
            for (const data in allElements) {
                let grundfunktionValue = allElements[data]['GrundfunktionValue']
                if (grundfunktionen.includes(grundfunktionValue)) {
                    continue
                } else {
                    grundfunktionen.push(grundfunktionValue)
                }
            }
            return grundfunktionen
        },
        parentAasIdShort () {
            const parentIdShort = this.digitalTwinStore.parentAasIdShort
            return parentIdShort
        }
    }
}
</script>