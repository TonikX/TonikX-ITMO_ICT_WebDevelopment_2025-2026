<script>
import Header from '@/components/Header.vue';
import EditUsername from '@/components/EditUsername.vue';
import EditPassword from '@/components/EditPassword.vue';
import DeleteProfile from '@/components/DeleteProfile.vue';

export default {
    components: {
        Header,
        EditUsername,
        EditPassword,
        DeleteProfile,
    },
    data() {
        return {
            username: localStorage.getItem("username"),
            operation: null,
        }
    },
    methods: {
        handleUsernameUpdated(newUsername) {
            this.username = newUsername;
            this.operation = null;
            this.$refs.header.updateUsername();
        },
        handlePasswordUpdated() {
            this.operation = null;
            alert('Пароль успешно изменён');
        },
        handleCancelOperation() {
            this.operation = null;
        },
    },
}
</script>


<template>
    <v-container style="max-width: 800px;">
        <Header ref="header"></Header>
        
        <h1 class="text-h4 mb-6">Профиль пользователя</h1>

        <EditUsername
            v-if="operation === 'edit_username'"
            :current-username="username"
            @username-updated="handleUsernameUpdated"
            @cancel="handleCancelOperation"
        />

        <EditPassword 
            v-else-if="operation === 'edit_password'"
            @cancel="handleCancelOperation"
            @success="handlePasswordUpdated"
        />

        <DeleteProfile
            v-else-if="operation === 'delete_profile'"
            @cancel="handleCancelOperation"
        />

        <div v-else>
            <v-card class="mb-4">
                <v-card-title>Логин</v-card-title>
                <v-card-text>{{ username }}</v-card-text>
                <v-card-actions>
                    <v-btn @click="operation = 'edit_username'" color="primary">Изменить</v-btn>
                </v-card-actions>
            </v-card>

            <v-card class="mb-4">
                <v-card-title>Пароль</v-card-title>
                <v-card-actions>
                    <v-btn @click="operation = 'edit_password'" color="primary">Изменить</v-btn>
                </v-card-actions>
            </v-card>

            <v-card>
                <v-card-title>Профиль</v-card-title>
                <v-card-actions>
                    <v-btn @click="operation = 'delete_profile'" color="error">Удалить профиль</v-btn>
                </v-card-actions>
            </v-card>
        </div>
    </v-container>
</template>
