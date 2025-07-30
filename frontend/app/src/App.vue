<template>
  <v-app>
    <Authenticator>
      <template v-slot:header>
        <div style="padding: var(--amplify-space-large); text-align: center">
          <img
            src="@/assets/logo_TH.png"
          />
        </div>
      </template>
    </Authenticator>
      <template v-if="auth.authStatus === 'authenticated'">
        <NavBar />
        <NavigationDrawer />
        <v-main>
          <Breadcrumbs />
          <router-view />
          <Footer />
        </v-main>
      </template>   
  </v-app>

</template>

<script setup>
  import NavBar from '@/components/general/NavBar.vue'
  import Footer from '@/components/general/Footer.vue'
  import NavigationDrawer from '@/components/general/NavigationDrawer.vue'
  import Breadcrumbs from '@/components/general/Breadcrumbs.vue'

  //import { onMounted } from "vue"
  import { watchEffect } from "vue"
  import { useGeneralStore } from "@/store/general"
  import { Authenticator } from '@aws-amplify/ui-vue';
  import { useAuthenticator } from '@aws-amplify/ui-vue'
  import '@aws-amplify/ui-vue/styles.css';

  import { I18n } from 'aws-amplify';
  import { translations } from '@aws-amplify/ui-vue';
  I18n.putVocabularies(translations);
  I18n.setLanguage('de');

  I18n.putVocabularies({
    de: {
      'Enter your Username': 'Geben Sie Ihren Benutzernamen an',
      'Enter your Password': "Geben Sie ihr Passwort an",
      'Please confirm your Password': 'Bitte bestätigen Sie ihr Passwort',
      'Enter your Email': 'Geben Sie Ihre E-Mail Adresse an',
      'Reset Password': 'Passwort zurücksetzen',
      'Password must have at least 8 characters': 'Ihr Passwort muss mindestens 8 Zeichen haben',
      'Your passwords must match': 'Die Passwörter müssen übereinstimmen'
    }
  })
  const auth = useAuthenticator();
  const store = useGeneralStore()

  watchEffect(() => {
    // Check if auth.user is available and contains the necessary properties.
    if (auth.user && auth.user.signInUserSession) {
      const userId = auth.user.signInUserSession.idToken.payload.sub
      //console.log(userId)
      store.fetchGeneralInfos(userId)
    }
  });
  /*
  onMounted( () => {
    //const authentification = useAuthenticator()
    console.log(auth)
    const userId = auth.user.signInUserSession.idToken.payload.sub
    store.fetchGeneralInfos(userId)
  })
  */
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Montserrat");
#app {
  font-family: "Montserrat";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
[data-amplify-authenticator] {
  --amplify-components-tabs-item-active-border-color: var(
    --amplify-colors-brand-secondary-100
  );
  --amplify-components-tabs-item-active-color: var(
    --amplify-colors-brand-secondary-100
  );
  --amplify-components-button-primary-background-color: var(
    --amplify-colors-brand-secondary-80
  );
  --amplify-components-button-primary-hover-background-color: var(
    --amplify-colors-brand-secondary-90
  );
  --amplify-components-button-primary-focus-background-color: var(
    --amplify-colors-brand-secondary-90
  );
  --amplify-components-button-primary-active-background-color: var(
    --amplify-colors-brand-secondary-100
  );
  --amplify-components-button-link-color: var(
    --amplify-colors-brand-secondary-80
  );
  --amplify-components-button-link-hover-color: var(
    --amplify-colors-brand-secondary-90
  );
  --amplify-components-button-link-focus-color: var(
    --amplify-colors-brand-secondary-90
  );
  --amplify-components-button-link-active-color: var(
    --amplify-colors-brand-secondary-100
  );
  --amplify-components-button-link-active-background-color: transparent;
  --amplify-components-button-link-focus-background-color: transparent;
  --amplify-components-button-link-hover-background-color: transparent;
}
.card-background {
  background-color: whitesmoke;
}
</style>

