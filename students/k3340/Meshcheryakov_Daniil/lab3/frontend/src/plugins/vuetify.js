import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const ru = {
  dataIterator: {
    noResultsText: 'Результаты не найдены',
    loadingText: 'Загрузка...'
  },
  dataTable: {
    itemsPerPageText: 'Строк на странице:',
    ariaLabel: {
      sortDescending: 'Сортировка по убыванию',
      sortAscending: 'Сортировка по возрастанию',
      sortNone: 'Без сортировки',
      activateNone: 'Активировать для удаления сортировки',
      activateDescending: 'Активировать для сортировки по убыванию',
      activateAscending: 'Активировать для сортировки по возрастанию'
    },
    sortBy: 'Сортировать по'
  },
  dataFooter: {
    itemsPerPageText: 'Строк на странице:',
    itemsPerPageAll: 'Все',
    nextPage: 'Следующая страница',
    prevPage: 'Предыдущая страница',
    firstPage: 'Первая страница',
    lastPage: 'Последняя страница',
    pageText: '{0}-{1} из {2}'
  },
  datePicker: {
    itemsSelected: '{0} выбрано'
  },
  noDataText: 'Нет данных',
  carousel: {
    prev: 'Предыдущий',
    next: 'Следующий',
    ariaLabel: {
      delimiter: 'Слайд {0} из {1}'
    }
  },
  calendar: {
    moreEvents: 'Еще {0}'
  },
  fileInput: {
    counter: '{0} файлов',
    counterSize: '{0} файлов ({1} всего)'
  },
  timePicker: {
    am: 'AM',
    pm: 'PM'
  },
  pagination: {
    ariaLabel: {
      wrapper: 'Навигация по страницам',
      next: 'Следующая страница',
      previous: 'Предыдущая страница',
      page: 'Перейти на страницу {0}',
      currentPage: 'Текущая страница, страница {0}'
    }
  },
  rating: {
    ariaLabel: {
      item: 'Рейтинг {0} из {1}'
    }
  }
}

export default createVuetify({
  components,
  directives,
  locale: {
    locale: 'ru',
    fallback: 'ru',
    messages: { ru }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        },
      },
    },
  },
})

