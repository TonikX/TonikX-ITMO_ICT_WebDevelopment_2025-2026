import { axios } from './config'

export const getEggsByCharacteristics = (params = {}) =>
  axios.get('/reports/eggs-by-characteristics/', { params }).then(r => r.data)

export const getTopWorkshop = (breedName) =>
  axios.get(`/reports/top-workshop/${breedName}/`).then(r => r.data)

export const getEmployeeAvgEggs = () =>
  axios.get('/reports/employee-average-eggs/').then(r => r.data)

export const getBreedDistribution = () =>
  axios.get('/reports/breed-distribution/').then(r => r.data)

export const getBreedEfficiencyDiff = () =>
  axios.get('/reports/breed-efficiency-difference/').then(r => r.data)

export const getMonthlyReport = () =>
  axios.get('/reports/monthly/').then(r => r.data)