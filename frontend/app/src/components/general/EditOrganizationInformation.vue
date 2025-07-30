<template>
  <div>
    <v-dialog
        v-model="dialog"
        width="60%">
        <template v-slot:activator="{ props }">
            <!--<v-btn class="ma-3" @click="getData()">Get Data</v-btn>-->
            <v-container class="d-flex justify-center align-center">
              <v-btn
                class="ma-1"
                v-bind="props"
                rounded="xl"
                variant="text" color="rgba(255, 74, 28, 1.0)"
            >Edit information</v-btn>
            </v-container>
          </template>
              <v-card>
                <v-toolbar
                color="success"
                >
                <v-toolbar-title style="color: white;">Edit information</v-toolbar-title>
                </v-toolbar>
                <v-form id="text-field-edit-orga" class="mt-4">
                  <v-text-field
                  label="Name der Organisation"
                  placeholder="Edit Name"
                  v-model="editOrganizationName"
                  required
                  ></v-text-field>
                </v-form>

              <v-form id="text-field-edit-orga">
                  <v-text-field
                  label="Land"
                  placeholder="Edit Land"
                  v-model="editOrganizationCountry"
                  required
                  ></v-text-field>
              </v-form>

              <v-form id="text-field-edit-orga">
                  <v-text-field
                  label="Stadt"
                  placeholder="Edit Stadt"
                  v-model="editOrganizationCity"
                  required
                  ></v-text-field>
              </v-form>

              <v-form id="text-field-edit-orga">
                  <v-text-field
                  label="Postleitzahl"
                  placeholder="Edit Postleitzahl"
                  v-model="editOrganizationZip"
                  required
                  ></v-text-field>
              </v-form>

              <v-form id="text-field-edit-orga">
                  <v-text-field
                  label="Straße und Hausnummer"
                  placeholder="Edit Straße"
                  v-model="editOrganizationStreet"
                  required
                  ></v-text-field>
              </v-form>
                <div class="text-center">
                  <v-btn 
                  @click="generalStore.editOrganizationInformation(
                    editOrganizationName, 
                    editOrganizationCountry,
                    editOrganizationCity,
                    editOrganizationZip,
                    editOrganizationStreet
                  ), dialog = false"
                  rounded="xl"
                  variant="text" color="rgba(255, 74, 28, 1.0)"
                  class="ma-3">Submit</v-btn>
                <v-btn
                  rounded="xl"
                  variant="text" color="rgba(255, 74, 28, 1.0)"
                    @click="dialog = false"
                >
                    Close
                </v-btn>
                </div>
        </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { useGeneralStore } from "@/store/general"

export default {

    data () {
      return {
        dialog: false,
        editOrganizationName: this.orgaInformation['organizationName'],
        editOrganizationCountry: this.orgaInformation['country'],
        editOrganizationCity: this.orgaInformation['city'],
        editOrganizationZip: this.orgaInformation['zipcode'],
        editOrganizationStreet: this.orgaInformation['street'],
      }
    },
    props: {
        orgaInformation: Object
    },
    computed: {
        generalStore () {
          return useGeneralStore()
        }
    }
}
</script>

<style>
.two-line-title {
  max-height: 3em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
}
#text-field-edit-orga {
  width: 70%;
  align-self: center;
}
</style>