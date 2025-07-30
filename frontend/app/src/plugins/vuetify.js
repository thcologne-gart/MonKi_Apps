/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify} from 'vuetify'


const myCustomLightTheme = {
  dark:false,
  colors:{
    //background:'#fcefef',
    //background: '#FFFAF4',
    background: '#e8e8e8',
    surface:'#FFFFFF',
    primary:'#c42424', //th: orange
    //primary: '#FF4A1C',
    'primary-darken-1':'#bc3384',
    highlight:'#ff4a1c', // plyteq rot
    secondary:'#a3a0a0',
    'secondary-darken-1': '#9dacb2',
    error:'#e03024',
    info:'#b2ffa9', // plyteq hellgrüm
    //success:'#bc3384',
    success: '#3B5249', // plyteq dunkelgrün
    //warning:'#ff4a1c',
    warning: '#372772', // plyteq blau
    //monitoring: '#285757',
    monitoring: '#3B5249',
  },
}

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  
    theme: {
      defaultTheme: 'myCustomLightTheme',
      themes:{
        myCustomLightTheme,
      }
  
    },
})
