<template>
    <v-card class="mx-auto my-16"
        max-width="65%"
        variant="outlined"
        style="border-radius: 20px; background-color: whitesmoke;">
        <v-toolbar
        style="background-color: whitesmoke;"
            >
            <v-toolbar-title style="color: #3B5249;"
            class="d-flex justify-center align-center">
                <span>{{ currentTitle }}</span>
            </v-toolbar-title>
        </v-toolbar>
        <v-divider :thickness="4"></v-divider>
        <v-window v-model="step"
        style="background-color: whitesmoke;">
        <v-window-item
            v-for="n in length"
            :key="`card-${n}`"
            :value="n"
        >
            <div v-if="n == 1 && !generalStore.loadedOrganizationInformation.length">
                <AddOrgaInformation />
            </div>
            <div v-else-if="n == 1 && generalStore.loadedOrganizationInformation.length != 0">
                <ShowOrgaInformation />
            </div>
            <div v-else-if="n == 2">
                <AddSites />
            </div>
            <div v-else-if="n == 3">
                <Buildings />
            </div>
        </v-window-item>
        </v-window>

        <v-card-actions class="justify-space-between">
        <v-btn
            rounded="xl"
            style="background-color: whitesmoke;"
            variant="plain" 
            color="highlight"
            icon="mdi-chevron-left"
            @click="prev"
        ></v-btn>
        <v-item-group
            v-model="step"
            class="text-center"
            mandatory
        >
            <v-item
            v-for="n in length"
            :key="`btn-${n}`"
            v-slot="{ isSelected, toggle }"
            :value="n"
            >
            <v-btn
                :variant="isSelected ? 'outlined' : 'text'"
                icon="mdi-record"
                color="highlight"
                @click="toggle"
            ></v-btn>
            </v-item>
        </v-item-group>
        <v-btn
            variant="plain"
            color="highlight"
            icon="mdi-chevron-right"
            @click="next"
        ></v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>

import AddOrgaInformation from '@/components/general/AddOrgaInformation.vue'
import ShowOrgaInformation from '@/components/general/ShowOrgaInformation.vue'
import AddSites from '@/components/general/AddSites.vue'
import Buildings from '@/components/general/Buildings.vue'
// import EditOrganizationInformation from '@/components/general/EditOrganizationInformation.vue'

import { useGeneralStore } from "@/store/general"

export default {
    data () {
        return {
            length: 3,
            step: 0,
        }
    },
    // components: { AddOrgaInformation, EditOrganizationInformation, AddSites, AddBuildings },
    components: { AddOrgaInformation, ShowOrgaInformation, AddSites, Buildings },
    computed: {
        currentTitle () {
            switch (this.step) {
            //case 1: return 'Registrierung Unternehmen'
            case 1: return 'Registrierung Unternehmen'
            case 2: return 'Registrierung Liegenschaften'
            default: return 'Registrierung Gebäude'
            }
        },
        generalStore () {
            return useGeneralStore()
        },
        /*
        organization () {
            const loadedOrganizationInformation = this.generalStore.loadedOrganizationInformation
            console.log(loadedOrganizationInformation)
            return loadedOrganizationInformation
        },
        sites () {
            const loadedSiteInformation = this.generalStore.loadedOrganizationInformation
            console.log(loadedSiteInformation)
            return loadedSiteInformation
        }
        */
    },
    methods: {
      next () {
        this.step = this.step + 1 > this.length
          ? 1
          : this.step + 1
      },
      prev () {
        this.step = this.step - 1 <= 0
          ? this.length
          : this.step - 1
        console.log(this.step)
      }
    }
}

</script>