<template>
    <div class="registration-page">
        <div class="registration-container">
            <div class="registration-card">
                <h1 class="title">Регистрация</h1>
                <p class="subtitle">Заполните поля ниже для создания аккаунта.</p>

                <a-form :model="formState" :rules="rules" @finish="onFinish" @finishFailed="onFinishFailed"
                    layout="vertical" class="registration-form">
                    <!-- Имя -->
                    <a-form-item name="name" class="form-item">
                        <a-input v-model:value="formState.name" placeholder="Имя" size="large" class="custom-input" />
                    </a-form-item>

                    <!-- E-mail -->
                    <a-form-item name="email" class="form-item">
                        <a-input v-model:value="formState.email" placeholder="E-mail" size="large"
                            class="custom-input" />
                    </a-form-item>

                    <!-- Введите пароль -->
                    <a-form-item name="password" class="form-item">
                        <a-input-password v-model:value="formState.password" placeholder="Введите пароль" size="large"
                            class="custom-input" />
                    </a-form-item>

                    <!-- Повторите пароль -->
                    <a-form-item name="confirmPassword" class="form-item">
                        <a-input-password v-model:value="formState.confirmPassword" placeholder="Повторите пароль"
                            size="large" class="custom-input" />
                    </a-form-item>

                    <!-- Согласен с политикой -->
                    <a-form-item name="agreement" class="form-item checkbox-item">
                        <a-checkbox v-model:checked="formState.agreement">
                            Согласен с политикой обработки данных.
                        </a-checkbox>
                    </a-form-item>

                    <!-- Submit Button -->
                    <a-form-item class="form-item">
                        <a-button :loading="loading" type="primary" html-type="submit" size="large" block
                            class="submit-button">
                            {{ loading ? "Loading..." : "Зарегистрироваться" }}
                        </a-button>
                    </a-form-item>

                    <!-- Login Link -->
                    <div class="login-link">
                        Уже есть аккаунт? <router-link to="login">Войти</router-link>
                    </div>
                </a-form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { message } from 'ant-design-vue';
import api from '@/utils/axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';

const userStore = useUserStore()
const router = useRouter()

const formState = reactive({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    agreement: false,
});

const loading = ref(false)

// Validatsiya qoidalari
const rules = {
    name: [
        {
            required: true,
            message: 'Пожалуйста, введите ваше имя',
            trigger: 'blur',
        },
        {
            min: 2,
            message: 'Имя должно содержать минимум 2 символа',
            trigger: 'blur',
        },
    ],
    email: [
        {
            required: true,
            message: 'Пожалуйста, введите email',
            trigger: 'blur',
        },
        {
            type: 'email',
            message: 'Пожалуйста, введите корректный email',
            trigger: 'blur',
        },
    ],
    password: [
        {
            required: true,
            message: 'Пожалуйста, введите пароль',
            trigger: 'blur',
        },
        {
            min: 8,
            message: 'Пароль должен содержать минимум 8 символов',
            trigger: 'blur',
        },
    ],
    confirmPassword: [
        {
            required: true,
            message: 'Пожалуйста, повторите пароль',
            trigger: 'blur',
        },
        {
            validator: (rule, value) => {
                if (value !== formState.password) {
                    return Promise.reject('Пароли не совпадают');
                }
                return Promise.resolve();
            },
            trigger: 'blur',
        },
    ],
    agreement: [
        {
            validator: (rule, value) => {
                if (!value) {
                    return Promise.reject('Вы должны согласиться с политикой обработки данных');
                }
                return Promise.resolve();
            },
            trigger: 'change',
        },
    ],
};

// Form submit handler (logikani siz qo'shasiz)
const onFinish = async (values) => {
    loading.value = true
    try {
        const { data } = await api.post("/auth/singup/", {
            username: values.name,
            email: values.email,
            password: values.password,
            confirm_password: values.confirmPassword
        })
        // console.log(data)
        const access_token = data.data.tokens.access_token
        const refresh_token = data.data.tokens.refresh_token

        localStorage.setItem("access_token", access_token)
        localStorage.setItem("refresh_token", refresh_token)
        localStorage.setItem("username", data.data.username)
        localStorage.setItem("useremail", data.data.email)
        userStore.add_user(data.data.username, data.data.email, access_token)
        message.success(data.message)
        formState.name = ""
        formState.email = ""
        formState.password = ""
        formState.confirmPassword = ""
        formState.agreement = ""
        router.push("/")
    } catch (error) {
        if (error.response) {
            const errors = error.response.data
            console.log(errors)
            if (errors.username) {
                message.error(errors.username[0])
            } else if (errors.email) {
                message.error(errors.email[0])
            } else if (errors.password) {
                message.error(errors.password[0])
            } else {
                message.error("An error occurred.")
            }
        } else {
            message.error("No connection to the server.")
            console.log(error)
        }
    } finally {
        loading.value = false
    }
};

const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};
</script>

<style scoped>
.registration-page {
    min-height: calc(100vh - 200px);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F5F5F5;
    padding: 40px 20px;
}

.registration-container {
    width: 100%;
    max-width: 550px;
    margin: 0 auto;
}

.registration-card {
    background: white;
    padding: 48px 40px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.title {
    font-size: 28px;
    font-weight: 700;
    color: #000000;
    text-align: center;
    margin-bottom: 8px;
}

.subtitle {
    font-size: 14px;
    color: #8C8C8C;
    text-align: center;
    margin-bottom: 32px;
}

.registration-form {
    width: 100%;
}

.form-item {
    margin-bottom: 16px !important;
}

.form-item:last-child {
    margin-bottom: 0;
}

.custom-input {
    border-radius: 4px;
    background: #F5F5F5;
    border: 1px solid #F5F5F5;
    font-size: 14px;
    color: #000000;
}

.custom-input:hover,
.custom-input:focus {
    background: #F5F5F5;
    border-color: #D9D9D9;
}

:deep(.ant-input-affix-wrapper) {
    background: #F5F5F5;
    border: 1px solid #F5F5F5;
    border-radius: 4px;
}

:deep(.ant-input-affix-wrapper:hover),
:deep(.ant-input-affix-wrapper:focus),
:deep(.ant-input-affix-wrapper-focused) {
    background: #F5F5F5;
    border-color: #D9D9D9;
}

:deep(.ant-input) {
    background: #F5F5F5;
    font-size: 14px;
    color: #000000;
}

:deep(.ant-input::placeholder) {
    color: #BFBFBF;
}

.checkbox-item {
    margin-bottom: 24px;
}

:deep(.ant-checkbox-wrapper) {
    font-size: 14px;
    color: #000000;
}

:deep(.ant-checkbox-checked .ant-checkbox-inner) {
    background-color: #2684E5;
    border-color: #2684E5;
}

.submit-button {
    height: 48px;
    font-size: 16px;
    font-weight: 500;
    border-radius: 4px;
    background: #2684E5;
    border: none;
    margin-top: 8px;
}

.submit-button:hover {
    background: #1a6bc4;
}

.login-link {
    text-align: center;
    font-size: 14px;
    color: #000000;
    margin-top: 24px;
}

.login-link a {
    color: #2684E5;
    text-decoration: none;
    font-weight: 500;
}

.login-link a:hover {
    text-decoration: underline;
}

/* Error messages styling */
:deep(.ant-form-item-explain-error) {
    font-size: 12px;
    margin-top: 4px;
}

/* Remove default margin from form items */
:deep(.ant-form-item) {
    margin-bottom: 0;
}
</style>