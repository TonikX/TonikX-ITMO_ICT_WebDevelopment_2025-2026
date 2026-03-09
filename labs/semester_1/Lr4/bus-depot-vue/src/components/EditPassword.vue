<script>
export default {
    data() {
        return {
            oldPassword: '',
            newPassword: '',
            reNewPassword: '',
        }
    },
    methods: {
        handleCancel() {
            this.$emit('cancel');
        },

        async handleSave() {
            if (!this.oldPassword || !this.newPassword || !this.reNewPassword) {
                alert('Все поля должны быть заполнены!');
                return;
            }

            if (this.newPassword !== this.reNewPassword) {
                alert('Новый пароль и его подтверждение не совпадают!');
                return;
            }

            const token = localStorage.getItem('auth_token');
            const url = `http://127.0.0.1:8000/auth/users/set_password/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({
                    new_password: this.newPassword,
                    current_password: this.oldPassword
                })
            });

            if (response.ok) {
                this.$emit('success');
            } else {
                console.log(response.json())
                alert("Ошибка при смене пароля");
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
            Изменить пароль
        </v-card-title>
        
        <v-card-text>
            <v-text-field v-model="oldPassword" label="Старый пароль" type="password" />
            <v-text-field v-model="newPassword" label="Новый пароль" type="password" />
            <v-text-field v-model="reNewPassword" label="Повторить новый пароль" type="password" />
        </v-card-text>
        
        <v-card-actions>
            <v-btn @click="handleSave" color="primary">Сохранить</v-btn>
        </v-card-actions>
    </v-card>
</template>
