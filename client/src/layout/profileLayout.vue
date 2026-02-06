<template>
    <div class="profile_layout_box">
        <div class="container">
            <!-- Mobile Menu Button -->
            <div class="mobile_menu_btn">
                <a-button type="primary" @click="showDrawer">
                    <MenuOutlined />
                    Меню
                </a-button>
            </div>

            <a-row :gutter="[16, 24]" class="profile_container">
                <!-- Desktop Sidebar -->
                <a-col class="gutter-row desktop_sidebar" :xs="0" :sm="0" :md="6" :lg="6" :xl="6">
                    <div class="side_bar_sticy">
                        <div class="gutter-box profile_sidebar">
                            <div class="profile_info">
                                <a-flex gap="middle" align="center">
                                    <div class="avatar">
                                        <img :src="userStore.avatarUrl" alt="" @load="onLoad" @error="onError">
                                    </div>
                                    <div class="user_info">
                                        <h3>{{ userStore.username }}</h3>
                                        <p>Рейтинг 5.0</p>
                                    </div>
                                </a-flex>

                                <div class="under_line"></div>

                                <div class="user_email">
                                    <a-flex justify="space-between" align="center">
                                        <p>E-mail</p>
                                        <p>
                                            <a href="#">{{ userStore.email }}</a>
                                        </p>
                                    </a-flex>
                                    <a-flex justify="space-between" align="center">
                                        <p>Тариф</p>
                                        <p>
                                            <a href="#">
                                                <InfoCircleOutlined /> Базовый тариф
                                            </a>
                                        </p>
                                    </a-flex>
                                </div>

                                <div class="profile_routes">
                                    <router-link to="/profile/storage" class="profile_route">
                                        <StarOutlined class="router_icon" />
                                        <p>Избранное</p>
                                    </router-link>
                                    <router-link to="/profile" class="profile_route">
                                        <MessageOutlined class="router_icon" />
                                        <p>Сообщения</p>
                                    </router-link>
                                    <div class="profile_route">
                                        <LayoutOutlined class="router_icon" />
                                        <a-dropdown>
                                            <a class="ant-dropdown-link" style="width: 100%;" @click.prevent>
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
                                                    <a-menu-item>
                                                        <router-link to="/upload">
                                                            Добавить авто
                                                        </router-link>
                                                    </a-menu-item>
                                                </a-menu>
                                            </template>
                                        </a-dropdown>
                                    </div>
                                    <router-link to="/profile" class="profile_route">
                                        <ThunderboltOutlined class="router_icon" />
                                        <p>Тариф</p>
                                    </router-link>
                                    <router-link to="/profile" class="profile_route">
                                        <ToolOutlined class="router_icon" />
                                        <p>Настройки аккаунта</p>
                                    </router-link>
                                </div>
                                <div class="log_out">
                                    <a-popconfirm title="Вы действительно хотите выйти?" ok-text="Да" cancel-text="Нет"
                                        @confirm="handleLogOut" @cancel="cancel">
                                        <a-button block danger>Выйти</a-button>
                                    </a-popconfirm>
                                </div>
                            </div>
                        </div>
                    </div>
                </a-col>

                <!-- Content -->
                <a-col class="gutter-row" :xs="24" :sm="24" :md="18" :lg="18" :xl="18">
                    <div class="gutter-box">
                        <div class="profile_router_view">
                            <RouterView />
                        </div>
                    </div>
                </a-col>
            </a-row>

            <!-- Mobile Drawer (Sidebar) -->
            <a-drawer v-model:open="drawerVisible" placement="left" :closable="true" width="280" title="Меню">
                <div class="profile_sidebar">
                    <div class="profile_info">
                        <a-flex gap="middle" align="center">
                            <div class="avatar">
                                <img :src="userStore.avatarUrl" alt="" @load="onLoad" @error="onError">
                            </div>
                            <div class="user_info">
                                <h3>{{ userStore.username }}</h3>
                                <p>Рейтинг 5.0</p>
                            </div>
                        </a-flex>

                        <div class="under_line"></div>

                        <div class="user_email">
                            <a-flex justify="space-between" align="center">
                                <p>E-mail</p>
                                <p>
                                    <a href="#">Khamzat.arslanaliyev@mail.ru</a>
                                </p>
                            </a-flex>
                            <a-flex justify="space-between" align="center">
                                <p>Тариф</p>
                                <p>
                                    <a href="#">
                                        <InfoCircleOutlined /> Базовый тариф
                                    </a>
                                </p>
                            </a-flex>
                        </div>

                        <div class="profile_routes">
                            <router-link to="/profile/storage" class="profile_route" @click="closeDrawer">
                                <StarOutlined class="router_icon" />
                                <p>Избранное</p>
                            </router-link>
                            <router-link to="/profile" class="profile_route" @click="closeDrawer">
                                <MessageOutlined class="router_icon" />
                                <p>Сообщения</p>
                            </router-link>
                            <div class="profile_route">
                                <LayoutOutlined class="router_icon" />
                                <a-dropdown>
                                    <a class="ant-dropdown-link" style="width: 100%;" @click.prevent>
                                        Разместить объявление
                                        <DownOutlined />
                                    </a>
                                    <template #overlay>
                                        <a-menu>
                                            <a-menu-item>
                                                <router-link to="/profile/mycars" @click="closeDrawer">
                                                    Мои объвления
                                                </router-link>
                                            </a-menu-item>
                                            <a-menu-item>
                                                <router-link to="/upload" @click="closeDrawer">
                                                    Добавить авто
                                                </router-link>
                                            </a-menu-item>
                                        </a-menu>
                                    </template>
                                </a-dropdown>
                            </div>
                            <router-link to="/profile" class="profile_route" @click="closeDrawer">
                                <ThunderboltOutlined class="router_icon" />
                                <p>Тариф</p>
                            </router-link>
                            <router-link to="/profile" class="profile_route" @click="closeDrawer">
                                <ToolOutlined class="router_icon" />
                                <p>Настройки аккаунта</p>
                            </router-link>
                        </div>
                        <div class="log_out">
                            <a-popconfirm title="Вы действительно хотите выйти?" ok-text="Да" cancel-text="Нет"
                                @confirm="handleLogOut" @cancel="cancel">
                                <a-button block danger>Выйти</a-button>
                            </a-popconfirm>
                        </div>
                    </div>
                </div>
            </a-drawer>
        </div>
    </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';
import { useRouter } from 'vue-router';

/////////////////////////// ICONS //////////////////
import {
    DownOutlined,
    InfoCircleOutlined,
    LayoutOutlined,
    MessageOutlined,
    StarOutlined,
    ThunderboltOutlined,
    ToolOutlined,
    MenuOutlined
} from "@ant-design/icons-vue"
import api from '@/utils/axios';
import { message } from 'ant-design-vue';
import { ref } from 'vue';

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const imageLoading = ref(false)
const drawerVisible = ref(false)

const showDrawer = () => {
    drawerVisible.value = true
}

const closeDrawer = () => {
    drawerVisible.value = false
}

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
            closeDrawer()
        }
    } catch (error) {
        console.log(error)
    } finally {
        loading.value = false
    }
}

const cancel = () => {
    message.info("Отменено")
}
</script>

<style scoped>
/* Mobile Menu Button */
.mobile_menu_btn {
    display: none;
    padding: 15px 0;
}

@media (max-width: 768px) {
    .mobile_menu_btn {
        display: block;
    }
}

.side_bar_sticy {
    position: sticky;
    top: 20px;
}

.profile_container {
    padding: 20px 0px;
}

@media (max-width: 768px) {
    .profile_container {
        padding: 10px 0;
    }
}

.profile_layout_box {
    background-color: #F5F5F5;
    min-height: 100vh;
}

.profile_sidebar {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 10px;
}

/* Drawer ichidagi sidebar uchun padding yo'q */
.ant-drawer .profile_sidebar {
    padding: 0;
    border-radius: 0;
    background-color: transparent;
}

.avatar {
    width: 48px;
    height: 48px;
    flex-shrink: 0;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 100%;
}

.user_info {
    flex: 1;
}

.user_info h3 {
    font-weight: 700;
    font-size: 16px;
    color: #293843;
    margin: 0;
}

.user_info p {
    margin: 0;
    font-weight: 400;
    font-size: 14px;
    color: #5A5A5A;
}

.under_line {
    height: 1px;
    background-color: #F0F0F0;
    margin: 16px 0;
}

.user_email {
    padding: 0;
    margin-bottom: 16px;
}

.user_email > div {
    margin-bottom: 8px;
}

.user_email p {
    font-size: 13px;
    color: #5A5A5A;
    margin: 0;
}

.user_email a {
    color: #1890ff;
    font-size: 13px;
    text-decoration: none;
}

.profile_routes {
    margin: 0;
}

.profile_route {
    padding: 10px 0;
    display: flex;
    gap: 12px;
    align-items: center;
    transition: all 0.2s ease;
    text-decoration: none;
    border-radius: 6px;
    margin-bottom: 4px;
}

.profile_route p,
.profile_route a {
    margin: 0;
    color: #293843;
    font-size: 15px;
    font-weight: 400;
}

.profile_route:hover {
    background-color: rgba(0, 0, 0, 0.04);
}

.router-link-active {
    color: #1890ff;
}

.router-link-active .router_icon {
    color: #5A5A5A;
}

.router_icon {
    font-size: 18px;
    color: #5A5A5A;
}

.log_out {
    padding-top: 24px;
}

.log_out button {
    width: 100%;
}

.profile_router_view {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 15px;
    min-height: 500px;
}

@media (max-width: 768px) {
    .profile_router_view {
        padding: 12px;
        border-radius: 8px;
    }
}

/* Drawer ichki padding ni olib tashlash */
:deep(.ant-drawer-body) {
    padding: 16px !important;
}

/* Drawer header */
:deep(.ant-drawer-header) {
    padding: 16px !important;
    border-bottom: 1px solid #f0f0f0;
}

:deep(.ant-drawer-title) {
    font-size: 16px;
    font-weight: 600;
}

</style>