<template>
    <div class="profile_layout_box">
        <div class="container">
            <a-row :gutter="[16, 24]" class="profile_container">
                <a-col class="gutter-row" :span="6">
                    <div  class="side_bar_sticy">
                        <div class="gutter-box profile_sidebar">
                            <div class="profile_info">
                                <a-flex gap="middle" align="center">
                                    <div class="avatar">
                                        <img :src="userStore.avatarUrl" alt="" @v-show="!imageLoading" @load="onLoad"
                                            @error="onError">
                                    </div>
                                    <div class="user_info">
                                        <h3>
                                            {{ userStore.username }}
                                        </h3>
                                        <p>Рейтинг 5.0</p>
                                    </div>
                                </a-flex>

                                <div class="under_line"></div>

                                <div class="user_email">
                                    <a-flex justify="space-between" align="center">
                                        <p>
                                            E-mail
                                        </p>
                                        <p>
                                            <a href="#">Khamzat.arslanaliyev@mail.ru</a>
                                        </p>
                                    </a-flex>
                                    <a-flex justify="space-between" align="center">
                                        <p>
                                            Тариф
                                        </p>
                                        <p>
                                            <a href="#">
                                                <InfoCircleOutlined /> Базовый тариф
                                            </a>
                                        </p>
                                    </a-flex>
                                </div>

                                <div class="profile_routes">
                                    <router-link to="/" class="profile_route">
                                        <StarOutlined class="router_icon" />
                                        <p>
                                            Избранное
                                        </p>
                                    </router-link>
                                    <router-link to="/" class="profile_route">
                                        <MessageOutlined class="router_icon" />
                                        <p>
                                            Сообщения
                                        </p>
                                    </router-link>
                                    <div class="profile_route">
                                        <LayoutOutlined class="router_icon" />
                                        <a-dropdown>
                                            <a class="ant-dropdown-link" @click.prevent>
                                                Разместить объявление
                                                <DownOutlined />
                                            </a>
                                            <template #overlay>
                                                <a-menu>
                                                    <a-menu-item>
                                                        <router-link to="/profile/mycars">
                                                            Мои объвления
                                                        </router-link>
                                                    </a-menu-item>
                                                </a-menu>
                                            </template>
                                        </a-dropdown>
                                    </div>
                                    <router-link to="/" class="profile_route">
                                        <ThunderboltOutlined class="router_icon" />
                                        <p>
                                            Тариф
                                        </p>
                                    </router-link>
                                    <router-link to="profile" class="profile_route">
                                        <ToolOutlined class="router_icon" />
                                        <p>
                                            Настройки аккаунта
                                        </p>
                                    </router-link>
                                </div>
                                <div class="log_out">
                                    <a-popconfirm title="Are you sure delete this task?" ok-text="Yes" cancel-text="No"
                                        @confirm="handleLogOut" @cancel="cancel">
                                        <a-button>Выйти</a-button>
                                    </a-popconfirm>
                                </div>
                            </div>
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :span="18">
                    <div class="gutter-box" >
                        <div class="profile_router_view">
                            <RouterView />
                        </div>
                    </div>
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';
import { useRouter } from 'vue-router';

/////////////////////////// ICONS //////////////////
import { DownOutlined, InfoCircleOutlined, LayoutOutlined, MessageOutlined, OrderedListOutlined, StarOutlined, ThunderboltOutlined, ToolOutlined } from "@ant-design/icons-vue"
import api from '@/utils/axios';
import { message } from 'ant-design-vue';
import { ref } from 'vue';

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const imageLoading = ref(false)

const onLoad = () => {
    imageLoading.value = false
}

const onError = () => {
    imageLoading.value = false
}

const handleLogOut = async () => {
    loading.value = true
    try {

        const refresh_token = localStorage.getItem('refresh_token')

        const { data } = await api.post('auth/logout/', {
            refresh: refresh_token
        })

        if (data.success) {
            localStorage.clear()
            userStore.clear()
            message.success(data.message)
            router.push("/")
        }
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false
    }
}

const cancel = () => {
    message.success("biz bilan qolganizdan hursandmiz")
}


</script>

<style scoped>
.side_bar_sticy {
    position: sticky;
    top: 20px;
}

.profile_container {
    padding-top: 20px;
}

.profile_layout_box {
    background-color: #F5F5F5;
}

.profile_sidebar {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 10px;
}

.avatar {
    width: 36px;
    height: 36px;

    img {
        border-radius: 100%;
    }
}

.user_info {
    padding-bottom: 20px;

    h3 {
        border-radius: 700;
        font-size: 15px;
        color: #293843;
    }

    p {
        margin: 0;
        font-weight: 400;
        font-size: 14px;
        color: #5A5A5A;
    }
}

.under_line {
    height: 1.5px;
    border-radius: 10px;
    background-color: #F0F0F0;
}

.user_email {
    padding-top: 20px;
}

.profile_route {
    padding: 12px 10px;
    border-radius: 10px;
    display: flex;
    gap: 10px;
    align-items: center;
    transition: all 0.8ms ease-in;

    p,
    a {
        margin: 0;
        color: #293843;
        font-size: 15px;
        font-weight: 400;
    }
}

.profile_route:hover {
    background-color: #F3F5FC;
}

.router_icon {
    font-size: 18px;
    color: #293843;
}

.log_out {
    padding-top: 30px;

    button {
        width: 100%;
    }
}

.profile_router_view{
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 15px;
}
</style>