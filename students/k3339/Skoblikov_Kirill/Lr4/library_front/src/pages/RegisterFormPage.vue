<template>
    <div class="register-page">
        <div class="form-container">
            <h1 class="title">Регистрация</h1>

            <div v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </div>

            <div v-if="successMessage" class="success-message">
                {{ successMessage }}
            </div>

            <form class="register-form" @submit.prevent="handleSubmit">
                <InputField
                    id="first_name"
                    label="Имя"
                    v-model="formData.first_name"
                    placeholder="Иван"
                    :disabled="loading"
                    :errors="errors.first_name"
                />

                <InputField
                    id="last_name"
                    label="Фамилия"
                    v-model="formData.last_name"
                    placeholder="Иванов"
                    :disabled="loading"
                    :errors="errors.last_name"
                />

                <InputField
                    id="patronymic"
                    label="Отчество"
                    v-model="formData.patronymic"
                    placeholder="Иванович"
                    :disabled="loading"
                    :errors="errors.patronymic"
                />

                <InputField
                    id="job_title"
                    label="Должность"
                    v-model="formData.position"
                    placeholder="Менеджер"
                    :disabled="loading"
                    :errors="errors.position"
                />

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
                    id="email"
                    label="Email"
                    type="email"
                    v-model="formData.email"
                    placeholder="example@mail.ru"
                    :required="true"
                    :disabled="loading"
                    :errors="errors.email"
                />

                <InputField
                    id="password"
                    label="Пароль"
                    type="password"
                    v-model="formData.password"
                    placeholder="Не менее 8 символов"
                    :required="true"
                    :disabled="loading"
                    :errors="errors.password"
                />

                <InputField
                    id="confirmPassword"
                    label="Подтвердите пароль"
                    type="password"
                    v-model="formData.confirmPassword"
                    placeholder="Повторите пароль"
                    :required="true"
                    :disabled="loading"
                />

                <reglog-button
                    type="submit"
                    class="submit-btn"
                    :disabled="loading"
                >
                    <span v-if="loading">Регистрация...</span>
                    <span v-else>Зарегистрироваться</span>
                </reglog-button>

                <RedirectLink>
                    Уже есть аккаунт?
                    <router-link to="/login">Войти</router-link>
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
    name: 'RegisterPage',
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
            first_name: '',
            last_name: '',
            patronymic: '',
            job_title: '',
            username: '',
            email: '',
            password: '',
            confirmPassword: ''
        });

        const resetErrors = () => {
            errorMessage.value = '';
            successMessage.value = '';
            Object.keys(errors).forEach(key => delete errors[key]);
        };

        const validateForm = () => {
            resetErrors();

            if (formData.password !== formData.confirmPassword) {
                errorMessage.value = 'Пароли не совпадают!';
                return false;
            }

            if (formData.password.length < 8) {
                errorMessage.value = 'Пароль должен содержать не менее 8 символов';
                return false;
            }

            if (!formData.username.trim()) {
                errorMessage.value = 'Имя пользователя обязательно';
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
                    email: formData.email,
                    first_name: formData.first_name,
                    last_name: formData.last_name,
                    patronymic: formData.patronymic,
                    job_title: formData.job_title
                };

                await authAPI.register(dataToSend);

                successMessage.value = 'Регистрация успешна!';

                Object.keys(formData).forEach(key => {
                    formData[key] = '';
                });

                setTimeout(() => {
                    router.push('/login');
                }, 2000);

            } catch (error) {
                if (error.response) {
                    if (error.response.data) {
                        const data = error.response.data;

                        Object.keys(data).forEach(key => {
                            errors[key] = Array.isArray(data[key]) ? data[key] : [data[key]];
                        });

                        if (data.detail) {
                            errorMessage.value = data.detail;
                        } else if (Object.keys(errors).length > 0) {
                            errorMessage.value = 'Пожалуйста, исправьте ошибки в форме';
                        }
                    }
                } else if (error.request) {
                    errorMessage.value = 'Ошибка сети. Проверьте подключение к интернету.';
                } else {
                    errorMessage.value = 'Произошла ошибка. Попробуйте еще раз.';
                }

                console.error('Ошибка регистрации:', error);
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
.register-page {
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

.register-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.form-group label {
    color: #555;
    font-weight: 600;
    font-size: 0.95rem;
}

.form-group input {
    padding: 12px 15px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.3s ease;
    background: #fff;
}

.form-group input:focus {
    outline: none;
    border-color: #7a66ea;
    box-shadow: 0 0 0 3px rgba(122, 102, 234, 0.1);
}

.form-group input:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
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

.field-error {
    color: #d32f2f;
    font-size: 0.85rem;
    margin-top: 3px;
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