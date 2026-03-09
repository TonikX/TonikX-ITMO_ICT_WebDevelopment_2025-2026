<template>
    <v-container class="d-flex flex-column align-center justify-center fill-height">
        <h1 class="mb-6">Автобусный парк</h1>

        <div class="d-flex flex-column" style="width: 300px;">
            <v-btn
                to="/login"
                block
                color="primary"
            >
                Войти
            </v-btn>

            <br>

            <v-btn
                to="/signup"
                block
                color="primary"
            >
                Регистрация
            </v-btn>
        </div>
    </v-container>
</template>
