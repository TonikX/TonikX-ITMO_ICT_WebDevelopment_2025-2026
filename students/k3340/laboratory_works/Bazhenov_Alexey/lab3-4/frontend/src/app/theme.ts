import { createTheme } from '@mui/material/styles';
import { ruRU as coreRuRU } from '@mui/material/locale';
import { ruRU as dateRuRU } from '@mui/x-date-pickers/locales';

export const theme = createTheme(
  {
    palette: {
      mode: 'light',
      primary: {
        main: '#006d77',
      },
      secondary: {
        main: '#ffb703',
      },
      background: {
        default: '#f7f9fb',
        paper: '#ffffff',
      },
    },
    shape: {
      borderRadius: 12,
    },
  },
  coreRuRU,
  dateRuRU,
);

