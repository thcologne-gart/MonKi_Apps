<template>
    <div>
        <v-row class="ma-1">
            <v-col>
                <v-select 
                :items="buildingsList" 
                v-model="choosedBuilding" 
                label= 'Zugehöriges Gebäude' 
                />
            </v-col>
        </v-row>
        <v-card-actions class="d-flex justify-center align-center">
            <v-btn class="mt-0" variant="outlined" color="warning" 
                @click= "generalStore.addGatewayToBuilding(gateway, choosedBuilding, buildingsIdsWithSelectName);
                buildingName = ''">Submit
            </v-btn>
        </v-card-actions>
        <v-container>
            <div v-if="generalStore.loadingBacnetAdding === true">
                <v-progress-linear
                indeterminate
                color="success"
                ></v-progress-linear>
            </div>
        </v-container>
    </div>
</template>

<script>
import { useGeneralStore } from "@/store/general"

export default{
    data () {
      return {
        choosedBuilding: ''
      }
    },    
    props: {
        buildingsList: Array, 
        gateway: Object,
        buildingsIdsWithSelectName:Object
    },
    computed: {
        generalStore () {
            return useGeneralStore()
        }
    }
}

</script>