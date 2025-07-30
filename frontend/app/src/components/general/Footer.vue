<template>
    <v-footer
      id="footer"
      class="text-center d-flex justify-space-between" color="secondary-darken-1"
    >
    <div>   
    </div>

    <div>
      <div>
        <v-btn
          v-for="icon in icons"
          :key="icon"
          class="mx-4"
          :icon="icon"
          variant="text"
        ></v-btn>
      </div>
      <div class="pt-0">
      </div>
      <v-divider></v-divider>
      <div>
        {{ new Date().getFullYear() }} — <strong>TH Köln</strong>
        <p>Institut für Technische Gebäudeausrüstung</p>
      </div>
    </div>
      
      <div >
      <v-avatar size="150px" rounded="0">
              <v-img src="@/assets/logo_TH.png">
            </v-img>
          </v-avatar>

     </div>
    </v-footer>
  </template>
  
  <script>
  export default {
    data: () => ({
      icons: [
        'mdi-facebook',
        'mdi-twitter',
        'mdi-linkedin',
        'mdi-instagram',
      ],
    }),
  }
  </script>
  
  <style scoped>
  #footer {
    width: 100%;
    margin-top: 10%;
    padding-top: 0 ;
    padding-bottom: 0;
  }
  #footer-button {
    width: 10%;
  }
  .container {
    padding: 0;
  }
  </style>
  