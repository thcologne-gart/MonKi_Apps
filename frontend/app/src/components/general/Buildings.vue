<template>
  <!--<div v-for="site in generalStore.loadedSiteInformation" :key="site">-->
  <div v-for="site, key in generalStore.loadedSiteInformationWithBuildings" :key="key">
    <SiteBuildings :site="site" />
    <v-divider :thickness="2"></v-divider>
  </div>
</template>

<script>
import SiteBuildings from '@/components/general/SiteBuildings.vue'
import { useGeneralStore } from "@/store/general"

export default {
  data () {
    return {
      form: {
        country: '',
        numberSite: '',
        city: '',
        zipcode: null,
        numberBuildings: null
      },
      countries: ['Deutschland', 'Österreich', 'Schweiz', 'Frankreich', 'Italien', 'England']
    }
  },
  components: { SiteBuildings },
  computed: {
    generalStore () {
      return useGeneralStore()
    },
    /*
    siteInformation () {
      const callBuildingsForEachSite = this.generalStore.getBuildingsForEachSite()
      const siteInformation = this.generalStore.loadedSiteInformationWithBuildings
      console.log(siteInformation)
      return siteInformation
    }, 
    */
  }
}
</script>
<style scoped>
.card {
    margin-inline: 20%;
    margin-bottom: 30px;
    margin-top: 20px;
}
.form-group {
    text-align: left;
    margin-bottom: 20px;
    margin-right: 10%;
    margin-left: 10%;
}
.btn {
    margin-left: 20px;
    margin-right: 20px;
}
#header {
    color: #0a322b;
    font-size: 1em
}
#body {
    font-size: 18px;
    padding-top: 5px;
    padding-bottom: 5px
}
</style>
