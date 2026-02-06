<template>
    <div class="container">
        <div v-if="!getUserLoading">
            <h1>Profile</h1>

            <!-- Rasm Upload Qismi -->
            <div class="user-image-section">
                <div class="avatar-container">
                    <div class="avatar-wrapper">
                        <img :src="photo || userStore.avatarUrl || defaultAvatar" alt="User Avatar" class="avatar-image">
                        <div class="avatar-overlay">
                            <label for="file-input" class="upload-label">
                                <CameraOutlined :style="{ fontSize: '24px', color: '#fff' }" />
                            </label>
                            <input 
                                id="file-input" 
                                type="file" 
                                accept="image/jpeg,image/png,image/heic,image/heif" 
                                @change="onFileChange"
                                style="display: none;"
                            >
                        </div>
                    </div>
                    <div class="avatar-actions" v-if="image">
                        <a-button type="primary" @click="handleChangeImage" :loading="uploadLoading">
                            <SaveOutlined /> Сохранить
                        </a-button>
                        <a-button @click="cancelUpload">
                            <CloseOutlined /> Отмена
                        </a-button>
                    </div>
                    <div class="avatar-actions" v-if="photo && !image">
                        <a-button danger @click="showDeleteConfirm">
                            <DeleteOutlined /> Удалить фото
                        </a-button>
                    </div>
                </div>
            </div>

            <!-- Email Form -->
            <a-form :model="EmailForm" :rules="emailRules" @finish="handleEmailRetriew" @finishFailed="onFinishFailed"
                layout="vertical">
                <a-form-item name='email' class="form-item" label="Email">
                    <a-input v-model:value="EmailForm.email" class="custom-input" placeholder="E-mail" size="large"
                        autocomplete="email" />
                </a-form-item>

                <a-form-item class="form-item">
                    <a-button :loading="emailLoading" type="primary" html-type="submit" size="large"
                        class="submit-button">
                        Изменить
                    </a-button>
                </a-form-item>
            </a-form>

            <!-- User Info Form -->
            <a-form :model="UserInfoState" :rules="UserInfoRules" @finish="handleUpdateUser"
                @finishFailed="onFinishFailed" layout="vertical">
                <div class="user_info">
                    <a-form-item name="username" class="form-item" label="Username">
                        <a-input v-model:value="UserInfoState.username" class="custom-input" placeholder="Username"
                            size="large" autocomplete="username" />
                    </a-form-item>
                    <a-form-item name="first_name" class="form-item" label="First Name">
                        <a-input v-model:value="UserInfoState.first_name" class="custom-input" placeholder="First Name"
                            size="large" autocomplete="given-name" />
                    </a-form-item>
                    <a-form-item name="last_name" class="form-item" label="Last Name">
                        <a-input v-model:value="UserInfoState.last_name" class="custom-input" placeholder="Last Name"
                            size="large" autocomplete="family-name" />
                    </a-form-item>
                </div>
                <a-form-item class="form-item">
                    <a-button :loading="loading" type="primary" html-type="submit" size="large">
                        Изменить
                    </a-button>
                </a-form-item>
            </a-form>

            <!-- Password Form -->
            <a-form :model="passwordState" :rules="passwordRules" @finish="handlePasswordChange"
                @finishFailed="onFinishFailed" layout="vertical">
                <div class="user_info">
                    <a-form-item name="old_password" label="Старый пароль" class="form-item">
                        <a-input-password v-model:value="passwordState.old_password" placeholder="Старый пароль"
                            class="custom-input" size="large" autocomplete="current-password" />
                    </a-form-item>
                    <a-form-item name="new_password" label="Новый пароль" class="form-item">
                        <a-input-password v-model:value="passwordState.new_password" placeholder="Новый пароль"
                            class="custom-input" size="large" autocomplete="new-password" />
                    </a-form-item>
                    <a-form-item name="confirm_password" label="Подтвердите пароль" class="form-item">
                        <a-input-password v-model:value="passwordState.confirm_password"
                            placeholder="Подтвердите пароль" class="custom-input" size="large"
                            autocomplete="new-password" />
                    </a-form-item>
                </div>
                <a-form-item class="form-item">
                    <a-button :loading="passwordLoading" type="primary" html-type="submit" size="large">
                        Изменить пароль
                    </a-button>
                </a-form-item>
            </a-form>
        </div>

        <div v-if="getUserLoading" class="user_loading">
            <a-spin size="large" />
        </div>
    </div>
</template>

<script setup>
import api from '@/utils/axios';
import { message, Modal } from 'ant-design-vue';
import { onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';
import { CameraOutlined, SaveOutlined, CloseOutlined, DeleteOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { createVNode } from 'vue';

const userStore = useUserStore();
const loading = ref(false);
const getUserLoading = ref(false);
const emailLoading = ref(false);
const passwordLoading = ref(false);
const uploadLoading = ref(false);
const router = useRouter();
const userID = ref(null);
const photo = ref(null);
const image = ref(null);

// Default avatar base64 SVG
const defaultAvatar = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgZmlsbD0iI2YwZjBmMCIvPjxjaXJjbGUgY3g9IjYwIiBjeT0iNDUiIHI9IjIwIiBmaWxsPSIjY2NjIi8+PHBhdGggZD0iTTMwIDkwIFE2MCA3MCA5MCA5MCIgZmlsbD0iI2NjYyIvPjwvc3ZnPg==';

const EmailForm = reactive({
    email: userStore.email
});

const UserInfoState = reactive({
    username: "",
    first_name: "",
    last_name: "",
});

const passwordState = reactive({
    old_password: "",
    new_password: "",
    confirm_password: ""
});

const emailRules = {
    email: [
        {
            required: true,
            message: "Пожалуйста, введите email",
            trigger: 'blur'
        },
        {
            type: 'email',
            message: "Пожалуйста, введите корректный email",
            trigger: 'blur'
        }
    ]
};

const UserInfoRules = {
    username: [
        {
            required: true,
            message: "Заполните поле",
            trigger: 'blur'
        },
        {
            min: 6,
            message: "Минимум 6 символов",
            trigger: 'blur'
        },
        {
            max: 32,
            message: "Максимум 32 символа",
            trigger: 'blur'
        }
    ],
    first_name: [
        {
            required: true,
            message: "Заполните поле",
            trigger: 'blur'
        },
        {
            min: 2,
            message: "Минимум 2 символа",
            trigger: 'blur'
        },
        {
            max: 32,
            message: "Максимум 32 символа",
            trigger: 'blur'
        }
    ],
    last_name: [
        {
            required: true,
            message: "Заполните поле",
            trigger: 'blur'
        },
        {
            min: 2,
            message: "Минимум 2 символа",
            trigger: 'blur'
        },
        {
            max: 32,
            message: "Максимум 32 символа",
            trigger: 'blur'
        }
    ]
};

const passwordRules = {
    old_password: [
        {
            required: true,
            message: "Введите старый пароль",
            trigger: 'blur'
        }
    ],
    new_password: [
        {
            required: true,
            message: "Введите новый пароль",
            trigger: 'blur'
        },
        {
            min: 8,
            message: "Минимум 8 символов",
            trigger: 'blur'
        },
        {
            pattern: /^(?=.*[a-z])(?=.*\d)/,
            message: "Пароль должен содержать заглавные и строчные буквы, и цифры",
            trigger: 'blur'
        }
    ],
    confirm_password: [
        {
            required: true,
            message: "Подтвердите пароль",
            trigger: 'blur'
        },
        {
            validator: (rule, value) => {
                if (value !== passwordState.new_password) {
                    return Promise.reject('Пароли не совпадают');
                }
                return Promise.resolve();
            },
            trigger: 'blur'
        }
    ]
};

// O'chirish confirmation modali
const showDeleteConfirm = () => {
    Modal.confirm({
        title: 'Вы уверены?',
        icon: createVNode(ExclamationCircleOutlined),
        content: 'Вы действительно хотите удалить фото профиля?',
        okText: 'Да, удалить',
        okType: 'danger',
        cancelText: 'Отмена',
        onOk() {
            handleDeleteImage();
        },
    });
};

// Rasmni o'chirish
const handleDeleteImage = async () => {
    try {
        const { data } = await api.delete(`/auth/user/image/delete/${userID.value}`);
        if (data.success) {
            message.success(data.message);
            photo.value = null;
            userStore.updateAvatar(null);
        } else {
            message.error(data.message);
        }
    } catch (error) {
        console.log(error.response || error);
        message.error('Ошибка при удалении фото');
    }
};

const MAX_SIZE = 2 * 1024 * 1024;

// File tanlanganda
const onFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const img = new Image();
    const objectUrl = URL.createObjectURL(file);
    img.src = objectUrl;

    img.onload = () => {
        if (img.width < 200 || img.height < 200) {
            message.error("Размер изображения должен быть не менее 200x200");
            e.target.value = null;
            URL.revokeObjectURL(objectUrl);
            return;
        }

        if (img.height > 2000 || img.width > 2000) {
            message.error("Размер изображения не должен превышать 2000x2000");
            e.target.value = null;
            URL.revokeObjectURL(objectUrl);
            return;
        }

        if (file.size > MAX_SIZE) {
            message.error("Размер файла не должен превышать 2 MB");
            e.target.value = null;
            URL.revokeObjectURL(objectUrl);
            return;
        }

        image.value = file;
        // Preview ko'rsatish uchun
        const reader = new FileReader();
        reader.onload = (event) => {
            photo.value = event.target.result;
        };
        reader.readAsDataURL(file);
        
        URL.revokeObjectURL(objectUrl);
    };

    img.onerror = () => {
        message.error("Ошибка загрузки изображения");
        e.target.value = null;
        URL.revokeObjectURL(objectUrl);
    };
};

// Uploadni bekor qilish
const cancelUpload = () => {
    image.value = null;
    getUserInfo(); // Original rasmni qaytarish
    message.info('Загрузка отменена');
};

// Rasmni saqlash
const handleChangeImage = async () => {
    if (!image.value) {
        message.warning('Сначала выберите фото');
        return;
    }

    uploadLoading.value = true;
    try {
        const formData = new FormData();
        formData.append("photo", image.value);

        const { data } = await api.put("/auth/user/update/", formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });

        photo.value = data.photo;
        userStore.updateAvatar(data.photo);
        image.value = null;
        message.success(data.message || 'Фото успешно обновлено');
        getUserInfo()
    } catch (error) {
        console.log(error.response || error);
        message.error('Ошибка при загрузке фото');
    } finally {
        uploadLoading.value = false;
    }
};

// User ma'lumotlarini yangilash
const handleUpdateUser = async (values) => {
    loading.value = true;
    try {
        const { data } = await api.put("/auth/user/update/", {
            username: values.username,
            last_name: values.last_name,
            first_name: values.first_name
        });
        message.success(data.message || 'Данные обновлены');
    } catch (error) {
        console.log(error.response || error);
        message.error('Ошибка при обновлении данных');
    } finally {
        loading.value = false;
    }
};

// Email o'zgartirish
const handleEmailRetriew = async (values) => {
    try {
        emailLoading.value = true;
        const { data } = await api.post("auth/email/", {
            old_email: userStore.email,
            email: values.email
        });
        message.success(data.message);
        router.push("email_verify");
        userStore.add_email_edit_token(data.data.token.email_edit_token);
        userStore.add_new_email(values.email);
    } catch (error) {
        if (error.response) {
            const errors = error.response.data;
            if (errors.old_email) {
                message.error(errors.old_email[0]);
            } else if (errors.email) {
                message.error(errors.email[0]);
            } else if (errors.detail) {
                message.error(errors.detail);
            } else {
                message.error("An error occurred.");
            }
        } else {
            message.error("No connection to the server.");
        }
    } finally {
        emailLoading.value = false;
    }
};

// Parolni o'zgartirish
const handlePasswordChange = async (values) => {
    passwordLoading.value = true;
    try {
        const { data } = await api.put('/auth/password/update/', {
            password: values.old_password,
            new_password: values.new_password,
            confirm_password: values.confirm_password
        });

        message.success(data.message);
        passwordState.old_password = "";
        passwordState.new_password = "";
        passwordState.confirm_password = "";
    } catch (error) {
        if (error.response) {
            const errors = error.response.data;
            if (errors.password) {
                message.error(errors.password);
            }
        } else {
            console.log(error);
        }
    } finally {
        passwordLoading.value = false;
    }
};

const onFinishFailed = (errorInfo) => {
    console.log("Failed : ", errorInfo);
};

// Foydalanuvchi ma'lumotlarini olish
const getUserInfo = async () => {
    getUserLoading.value = true;
    try {
        const { data } = await api.get('/auth/user/');
        UserInfoState.username = data.username;
        UserInfoState.first_name = data.first_name;
        UserInfoState.last_name = data.last_name;
        userID.value = data.id;
        
        if (data.photo) {
            photo.value = data.photo;
            userStore.updateAvatar(data.photo);
        }
    } catch (error) {
        console.log(error.response || error);
    } finally {
        getUserLoading.value = false;
    }
};

onMounted(() => {
    getUserInfo();
});
</script>

<style scoped>
.user_loading {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
}

.user-image-section {
    display: flex;
    justify-content: center;
    margin: 30px 0;
}

.avatar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.avatar-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid #f0f0f0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.avatar-wrapper:hover {
    border-color: #1890ff;
    box-shadow: 0 6px 16px rgba(24, 144, 255, 0.2);
}

.avatar-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-overlay {
    position: absolute;
    bottom: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.6);
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 50% 0 0 0;
}

.avatar-overlay:hover {
    background: rgba(0, 0, 0, 0.8);
    width: 45px;
    height: 45px;
}

.upload-label {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.avatar-actions {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.avatar-actions button {
    display: flex;
    align-items: center;
    gap: 5px;
}

.user_info {
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.user_info div {
    width: 100%;
}

@media (max-width: 768px) {
    .user_info {
        flex-direction: column;
    }

    .avatar-wrapper {
        width: 100px;
        height: 100px;
    }

    .avatar-actions {
        flex-direction: column;
        width: 100%;
    }

    .avatar-actions button {
        width: 100%;
    }
}
</style>