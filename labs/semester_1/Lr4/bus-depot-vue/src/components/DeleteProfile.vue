<script>
export default {
    data() {
        return {
            username: localStorage.getItem("username"),
            password: '',
        }
    },
    methods: {
        handleCancel() {
            this.$emit('cancel');
        },

        async deleteProfile() {
            if (!confirm(`Вы уверены, что хотите удалить профиль '${this.username}'?`)) {
                return;
            }
            const token = localStorage.getItem('auth_token');
            const response = await fetch('http://127.0.0.1:8000/auth/users/me/', {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    current_password: this.password
                })
            });
            if (response.ok) {
                alert(`Профиль '${this.username}' был успешно удалён`)
                localStorage.clear();
                this.$router.push('/auth')
            } else {
                alert("Ошибка при удалении профиля")
            }
        }
    },
}
</script>


<template>
    <v-card style="max-width: 800px;">
        <v-card-title>
            <v-btn @click="handleCancel" class="mb-4">
                <v-icon>mdi-arrow-left</v-icon>
                Отмена
            </v-btn>
            <br>
            Удаление профиля '{{ username }}'
        </v-card-title>
        
        <v-card-text>
            <v-text-field v-model="password" label="Введите пароль" type="password" />
        </v-card-text>
        
        <v-card-actions>
            <v-btn @click="deleteProfile" color="error">Удалить профиль</v-btn>
        </v-card-actions>
    </v-card>
</template>
