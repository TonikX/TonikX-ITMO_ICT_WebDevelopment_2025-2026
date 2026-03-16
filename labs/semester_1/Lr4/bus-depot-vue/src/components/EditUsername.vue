<script>
export default {
    props: {
        currentUsername: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            password: '',
            newUsername: this.currentUsername,
        }
    },
    methods: {
        handleCancel() {
            this.$emit('cancel');
        },
        async handleSave() {
            if (!this.password) {
                alert('Введите пароль');
                return;
            }
            
            if (!this.newUsername) {
                alert('Введите новый логин');
                return;
            }
            
            if (this.newUsername === this.currentUsername) {
                alert('Новый логин должен отличаться от текущего');
                return;
            }

            try {
                const token = localStorage.getItem('auth_token');
                const response = await fetch('http://127.0.0.1:8000/auth/users/set_username/', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        current_password: this.password,
                        new_username: this.newUsername
                    })
                });

                if (response.ok) {
                    localStorage.setItem('username', this.newUsername);
                    this.$emit('username-updated', this.newUsername);
                } else {
                    alert('Ошибка при изменении логина');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Ошибка при подключении к серверу');
            }
        },
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
            Изменить логин '{{ currentUsername }}'
        </v-card-title>
        
        <v-card-text>
            <v-text-field v-model="password" label="Пароль" type="password" />
            <v-text-field v-model="newUsername" label="Новый логин" />
        </v-card-text>
        
        <v-card-actions>
            <v-btn @click="handleSave" color="primary">Сохранить</v-btn>
        </v-card-actions>
    </v-card>
</template>
