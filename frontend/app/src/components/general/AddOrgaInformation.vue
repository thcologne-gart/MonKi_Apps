<template>
    <div>
      <!-- <v-card-title id="card-title">Unternehmensinformationen</v-card-title> -->
      <v-form>
        <v-container :style="{ width: '80%' }">
            <v-text-field
            id="organization-name"
            v-model="form.organizationName"
            label="Name der Organisation"
            required
            ></v-text-field>

            <v-select :items="countries" v-model="form.country" label= 'Sitz des Unternehmens (Land)' />

            <v-text-field
            id="city"
            v-model="form.city"
            label="Sitz des Unternehmens (Stadt)"
            required
            ></v-text-field>

            <v-text-field
            id="zipcode"
            v-model.number="form.zipcode"
            label="Sitz des Unternehmens (Postleitzahl)"
            required
            ></v-text-field>

            <v-text-field
            id="street"
            v-model="form.street"
            label="Straße und Hausnummer"
            required
            ></v-text-field>

            <!-- <v-text-field
            id="number-sites"
            v-model.number="form.numberOfSites"
            label="Anzahl der Standorte, die integriert werden"
            required
            type = number
            ></v-text-field> -->
            <v-btn 
            @click="generalStore.addOrganizationInformation(
              form.organizationName, 
              form.country, 
              form.city,
              form.zipcode,
              form.street
            )"
            class="ma-3" variant="outlined" color="warning">Submit</v-btn>
            <v-btn @click="onReset" class="max-3" type="reset" variant="outlined" color="warning">Reset</v-btn>
        </v-container>
      </v-form>
    </div>
</template>

<script>
import { useGeneralStore } from "@/store/general"

export default {
  data () {
    return {
      form: {
        organizationName: '',
        country: '',
        city: '',
        zipcode: null,
        numberOfSites: null,
        street: ''
      },
      countries: ['Deutschland', 'Österreich', 'Schweiz', 'Frankreich', 'Italien', 'England']
    }
  },
  computed: {
    generalStore () {
      return useGeneralStore()
    },
    organization () {
      const loadedOrganizationInformation = this.generalStore.loadedOrganizationInformation
      console.log(loadedOrganizationInformation)
      return loadedOrganizationInformation
    }
  },
  /*
  mounted () {
    this.showForm()
  },
  methods: {
    showForm () {
      // console.log(this.organization[0].value)
      const card = document.getElementById('cardOrganizationForm')
      console.log(card)
      //const alreadyFilled = this.organization[0].value
      // console.log('jiiii')
      //if (!alreadyFilled) {
        // console.log('nicht null')
      // } else {
        // card.classList.add('d-none')
      //}
    },
    // onCreateOrga (event) {
    onCreateOrga () {
      console.log(this.form.organizationName)
      //const card = document.getElementById('cardOrganizationForm')
      //card.classList.add('d-none')
      //console.log(typeof this.form.numberOfSites)
      // event.preventDefault()
      
      this.form.organizationName = ''
      // this.form.country = null
      this.form.city = ''
      this.form.zipcode = ''
      this.form.numberOfSites = ''
      this.form.street = ''
    },
   */
  methods: {
    onReset () {
      // event.preventDefault()
      // Reset our form values
      this.form.organizationName = ''
      // this.form.country = null
      this.form.city = ''
      this.form.zipcode = ''
      this.form.numberOfSites = ''
      this.form.street = ''
    }
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
#displayOrganizationInformation {
    margin-inline: 10%;
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
.row {
    border-bottom-style: solid;
    border-color: #F2F2F2;
}
</style>
