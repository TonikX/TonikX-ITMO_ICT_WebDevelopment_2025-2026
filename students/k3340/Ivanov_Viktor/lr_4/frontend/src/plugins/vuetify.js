import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#3F51B5',
          secondary: '#03A9F4',
          success: '#4CAF50',
          error: '#F44336',
          info: '#2196F3',
          warning: '#FFC107',
        },
      },
    },
  },
})

export default vuetify

