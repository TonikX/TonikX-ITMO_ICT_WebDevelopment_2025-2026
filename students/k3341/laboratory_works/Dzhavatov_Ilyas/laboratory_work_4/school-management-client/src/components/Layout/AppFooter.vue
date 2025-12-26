<template>
  <v-footer app padless>
    <v-card flat tile width="100%" color="grey-lighten-4">
      <v-divider />

      <v-card-text class="py-2">
        <v-row align="center" justify="space-between">
          <v-col cols="12" md="6">
            <div class="d-flex align-center">
              <v-icon color="primary" class="mr-2">mdi-school</v-icon>
              <span class="text-caption">
                © {{ currentYear }} Школьная система управления. Все права защищены.
              </span>
            </div>
          </v-col>

          <v-col cols="12" md="6" class="text-md-right">
            <div class="d-flex justify-end gap-4">
              <v-btn
                v-for="link in links"
                :key="link.title"
                :to="link.to"
                :href="link.href"
                target="_blank"
                variant="text"
                size="small"
                class="text-caption"
              >
                <v-icon left size="small">{{ link.icon }}</v-icon>
                {{ link.title }}
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>
export default {
  name: 'AppFooter',
  data() {
    return {
      currentYear: new Date().getFullYear(),
      links: [
        {
          title: 'Документация',
          icon: 'mdi-help-circle',
          href: '/docs'
        },
        {
          title: 'Поддержка',
          icon: 'mdi-lifebuoy',
          to: { name: 'Support' }
        },
        {
          title: 'О проекте',
          icon: 'mdi-information',
          to: { name: 'About' }
        }
      ]
    }
  }
}
</script>