<template>
    <div>
        <v-container>
            <v-card 
            style="border-radius: 20px; background-color: whitesmoke" 
            variant="outlined"
            class="mx-10 card-background">
                <v-card-title style="font-size: 18px">
                    <v-row>
                        <v-col cols="2">
                        </v-col>
                        <v-col cols="7" class="title-center"> {{ site['siteName'] }}</v-col>
                        <v-col cols="3">
                            <v-btn class="mt-0" variant="flat" color="rgba(255, 74, 28, 0.7)" 
                            size="small"
                                icon="mdi-map-marker-radius"
                                @click="$router.push({name:'DigitalTwins_Site', params:{siteid:site['siteName']}})">
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-card-title>
                <v-divider 
                class="border-opacity-75 mx-4 mb-2" :thickness="2" color="success"></v-divider>
                <v-card-subtitle class="title-center">Gebäude</v-card-subtitle>
                <v-card-title v-for="aasId in site['buildings']" :key="aasId" style="font-size: 18px">
                    <v-row v-for="(building, key) in aasId" :key="key">
                        <v-col cols="2"></v-col>
                        <v-col cols="7" class="title-center">
                            {{ building["buildingName"] }}
                        </v-col>
                        <v-col cols="3">
                                <v-btn variant="flat" color="rgba(255, 74, 28, 0.7)" size="small"
                                icon="mdi-home" class="mt-0"
                                @click="$router.push({name:'DigitalTwins_Site_Building', params:{buildingid:building['buildingName'], siteid:site['siteName'], buildingaasid:key}})">
                                </v-btn>
                        </v-col>
                    </v-row>
                </v-card-title>
            </v-card>
        </v-container>
    </div>
</template>

<script>
import { useDigitalTwinsStore } from "@/store/digitaltwins"

export default{
    data () {
        return {
            file: null,
        }
    },
    props: {
        site: Object
    },
    computed: {
        digitalTwinStore () {
        return useDigitalTwinsStore()
        }
    },
    methods: {
        getBuildingId (building) {
            const buildingId = building['buildingName']
            return buildingId
        }
    }
}
</script>

<style scoped>
.title-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>