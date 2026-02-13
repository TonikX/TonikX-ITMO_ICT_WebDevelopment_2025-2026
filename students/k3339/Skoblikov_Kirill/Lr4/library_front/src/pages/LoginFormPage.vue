<template>
    <div class="login-page">
        <div class="form-container">
            <h1 class="title">Авторизация</h1>

            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>

            <div v-if="successMessage" class="success-message">
                {{ successMessage }}
            </div>

            <form class="login-form" @submit.prevent="handleSubmit">
                <InputField
                    id="username"
                    label="Юзернейм"
                    v-model="formData.username"
                    placeholder="Введите имя пользователя"
                    :required="true"
                    :disabled="loading"
                    :errors="errors.username"
                />

                <InputField
                    id="password"
                    label="Пароль"
                    type="password"
                    v-model="formData.password"
                    placeholder="Введите пароль"
                    :required="true"
                    :disabled="loading"
                    :errors="errors.password"
                />

                <reglog-button
                    type="submit"
                    class="submit-btn"
                    :disabled="loading"
                >
                    <span v-if="loading">Авторизация...</span>
                    <span v-else>Войти</span>
                </reglog-button>

                <RedirectLink>
                    Еще нет аккаунта?
                    <router-link to="/register">Зарегистрироваться</router-link>
                </RedirectLink>
            </form>
        </div>
    </div>
</template>

<script>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import authAPI from '@/api/api.js';
import ReglogButton from "@/components/UI/ReglogButton.vue";
import InputField from "@/components/InputField.vue";
import RedirectLink from "@/components/UI/RedirectLink.vue"

export default {
    name: 'LoginPage',
    components: {
        ReglogButton,
        InputField,
        RedirectLink
    },
    setup() {
        const router = useRouter();
        const loading = ref(false);
        const errorMessage = ref('');
        const successMessage = ref('');
        const errors = reactive({});

        const formData = reactive({
            username: '',
            password: '',
        });

        const resetErrors = () => {
            errorMessage.value = '';
            successMessage.value = '';
            Object.keys(errors).forEach(key => delete errors[key]);
        };

        const validateForm = () => {
            resetErrors();

            if (!formData.username.trim()) {
                errorMessage.value = 'Имя пользователя не может быть пустым';
                return false;
            }

            if (!formData.password.trim()) {
                errorMessage.value = 'Пароль не может быть пустым';
                return false;
            }

            return true;
        };

        const handleSubmit = async () => {
            if (!validateForm()) {
                return;
            }

            loading.value = true;
            resetErrors();

            try {
                const dataToSend = {
                    username: formData.username,
                    password: formData.password,
                };

                const response = await authAPI.login(dataToSend);
                const authToken = response.data.auth_token;
                if (authToken) {
                    localStorage.setItem('auth_token', authToken);
                }

                successMessage.value = 'Авторизация успешна!';

                Object.keys(formData).forEach(key => {
                    formData[key] = '';
                });

                setTimeout(() => {
                    router.push('/app/books');
                }, 1000);

            } catch (error) {
                if (error.response) {
                    if (error.response.data) {
                        const data = error.response.data;
                        if (data.non_field_errors) {
                            errorMessage.value = data.non_field_errors.join(', ');
                        } else {
                            Object.keys(data).forEach(key => {
                                errors[key] = Array.isArray(data[key]) ? data[key] : [data[key]];
                            });

                            if (data.detail) {
                                errorMessage.value = data.detail;
                            } else if (Object.keys(errors).length > 0) {
                                errorMessage.value = 'Неверное имя пользователя или пароль';
                            }
                        }
                    }
                } else {
                    errorMessage.value = 'Произошла ошибка. Попробуйте еще раз.';
                }

                console.error('Ошибка авторизации:', error);
            } finally {
                loading.value = false;
            }
        };

        return {
            formData,
            errors,
            loading,
            errorMessage,
            successMessage,
            handleSubmit
        };
    }
}
</script>

<style scoped>
.login-page {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #7a66ea 10%, #b84a65 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.form-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    padding: 40px;
    width: 100%;
    max-width: 450px;
    animation: slideUp 0.5s ease-out;
}

.title {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
    font-size: 2rem;
    font-weight: 700;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.error-message {
    background: #ffeaea;
    color: #d32f2f;
    padding: 12px 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-weight: 500;
}

.success-message {
    background: #e8f5e9;
    color: #2e7d32;
    padding: 12px 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-weight: 500;
}

.submit-btn {
    margin-top: 10px;
}

.submit-btn:deep(.btn) {
    cursor: pointer;
    transition: all 0.3s ease;
}

.submit-btn:deep(.btn):disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 480px) {
    .form-container {
        padding: 30px 25px;
    }

    .title {
        font-size: 1.8rem;
    }
}
</style>