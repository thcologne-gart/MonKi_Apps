<template>
    <div>
        <div v-for="building in computedBuildings" :key="building['Name Gebäude']">
            <ShowBuildingInformation :building="building"/>
        </div>
        <AddBuilding :site="site"/>
    </div>
</template>

<script>
import AddBuilding from '@/components/general/AddBuilding.vue'
import ShowBuildingInformation from '@/components/general/ShowBuildingInformation.vue'
import { useGeneralStore } from "@/store/general"

export default {
  data: () => ({
    show: false
  }),
  components: { AddBuilding, ShowBuildingInformation }, 
  props: {
    site: Array
  },
  computed: {
    generalStore () {
      return useGeneralStore()
    },
    computedBuildings () {
        const buildings = []
        // const site = Object.values(this.site)[0]
        console.log(this.site['buildings'])
        for (let building in this.site['buildings']) {
          // console.log(site[building])
            let buildingInformationDict = {}
            console.log(this.site['buildings'])
            //let buildingInformation = this.site['buildings'][building]
            let buildingInformation = this.site['buildings'][building]
            console.log(buildingInformation)
            for (const i in buildingInformation) {
                let elementDict = buildingInformation[i]
                for (const element in elementDict) {
                  if (element === 'country') {
                    buildingInformationDict['Land'] = elementDict[element]
                  } else if (element === 'city') {
                      buildingInformationDict['Stadt'] =  elementDict[element]
                  } else if (element === 'street') {
                      buildingInformationDict['Straße'] = elementDict[element]
                  } else if (element === 'buildingName') {
                      buildingInformationDict['Name Gebäude'] = elementDict[element] 
                  }
                }
            }
            buildings.push(buildingInformationDict)
        }
        console.log(buildings)
        return buildings
    }
  }
}

</script>
