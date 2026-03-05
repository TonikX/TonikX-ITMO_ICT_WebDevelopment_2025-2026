import {defineStore} from 'pinia'
import {ref} from "vue";
import axios from "axios";

export const tokenStore = defineStore('tokenStore', () => {
    let token = ref(null)

    function setToken(newToken){
        token.value = newToken
        axios.defaults.headers.common.Authorization = 'Token ' + newToken
    }

    function deleteToken(){
        token.value = null
        axios.defaults.headers.common.Authorization = null
    }

    return {token, setToken, deleteToken}



}, {persist: true})