import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Пастельные цвета
const lightTheme = {
    dark: false,
    colors: {
        primary: '#2f6aff',
        secondary: '#00cc66',
        accent: '#FFB6C1',
        success: '#77DD77',
        error: '#FF6961',
        warning: '#FFD700',
        info: '#84B6F4',
        background: '#F9F9F9',
        surface: '#FFFFFF',
    }
}

export default createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'lightTheme',
        themes: {
            lightTheme,
        }
    },
    defaults: {
        VBtn: {
            color: 'primary',
            variant: 'flat',
            rounded: 'lg'
        },
        VCard: {
            rounded: 'lg',
            elevation: 2
        },
        VTextField: {
            variant: 'outlined',
            density: 'comfortable'
        }
    }
})