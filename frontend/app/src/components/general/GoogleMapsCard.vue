<template>
  <div>
    <v-container>
        <div class="google-map-card">
          <div id="map"></div>
        </div>
    </v-container>
  </div>
</template>

<script>
import { Loader } from '@googlemaps/js-api-loader';
import { useGeneralStore } from "@/store/general"

export default {
  data () {
      return {
        siteId: '',
        siteCoordinates: []
      }
  },
  mounted () {
    this.initMap()
  },
  created() {
        const site_id = this.$route.params.siteid
        this.siteId = site_id
    },
    computed: {
        generalStore () {
        return useGeneralStore()
        }
    },
    methods: {
        initMap() {
            /* eslint-disable no-undef */
            for (let site in this.generalStore.loadedSiteInformation) {
              if (this.siteId === this.generalStore.loadedSiteInformation[site]['siteName']) {
                const lat = parseFloat(this.generalStore.loadedSiteInformation[site]['lat'])
                const lng = parseFloat(this.generalStore.loadedSiteInformation[site]['lng'])
                this.siteCoordinates.push({ 
                  'lat': lat,
                  'lng': lng
                })
                //this.siteCoordinates['lat'] = this.generalStore.loadedSiteInformation[site]['lat']
                //this.siteCoordinates['lng'] = this.generalStore.loadedSiteInformation[site]['lng']
              }
            }
            /*
            for (let element in this.generalStore.loadedSiteInformationWithBuildings) {
              //console.log(Object.values(this.generalStore.loadedSiteInformationWithBuildings)[element])
              let site = Object.values(this.generalStore.loadedSiteInformationWithBuildings)[element]
              let siteName = Object.keys(site)
              console.log(siteName[0])
              if (this.siteId === siteName[0]) {
                let buildings = Object.values(site)
                console.log(buildings)
                for (let building in buildings[0]) {
                  console.log(buildings[0][building])
                  this.siteCoordinates.push({ 
                    'lat': buildings[0][building]['buildingInformation']['lat'],
                    'lng': buildings[0][building]['buildingInformation']['lng']
                  })
                }
              }
            }
            */
            console.log(this.siteCoordinates)
            //const uluru = { lat: -25.344, lng: 131.031 };

            const loader = new Loader({
                apiKey: 'AIzaSyDrSZaSw1y8mnFuNa_ZYHTd-0kFxd4eCnQ',
                version: 'weekly',
                libraries: ['places']
            });
            console.log(loader)
            let map

            loader.load().then(() => {
                map = new google.maps.Map(document.getElementById("map"), {
                    zoom: 10,
                    center: this.siteCoordinates[0]
                });
                console.log(map)
                const marker = new google.maps.Marker({
                    position: this.siteCoordinates[0],
                    map: map
                });
                console.log(marker)
            });
        }
    }
};
</script>

<style scoped>
.google-map-card {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 400px;
}

#map {
  width: 80%;
  height:100%;
}
</style>
