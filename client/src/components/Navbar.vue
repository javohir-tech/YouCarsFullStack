<template>
    <header class="navbar">
        <!-- ///////////////////////////////// -->
        <!-- ////////// UNDER NAVBAR /////// -->
        <!-- /////////////////////////////// -->
        <div class="under_navbar">
            <div class="container">
                <Row align="center">
                    <Col :xs="24" :sm="24" :md="14" :lg="14">
                        <ul class="menu_list">
                            <li><router-link to="/">Главная</router-link></li>
                            <li><router-link to="/">Каталог</router-link></li>
                            <li><router-link to="/">О нас</router-link></li>
                            <li><router-link to="/">Новости</router-link></li>
                            <li><router-link to="/">Контакты</router-link></li>
                        </ul>
                    </Col>
                    <Col :xs="0" :sm="0" :md="10" :lg="10">
                        <div class="under_rigth">
                            <div class="icons">
                                <a href="#">
                                    <InstagramOutlined class="icon" />
                                </a>
                                <a href="#">
                                    <WhatsAppOutlined class="icon" />
                                </a>
                                <a href="#">
                                    <LinkedinOutlined class="icon" />
                                </a>
                            </div>
                            <div>
                                <a href="#">
                                    <PhoneOutlined class="icon" />
                                    <span> +77 123 29 04</span>
                                </a>
                            </div>
                            <div>
                                <a href="#">
                                    <MailOutlined class="icon" />
                                    <span> suvonovjavohir625@gmail.com</span>
                                </a>
                            </div>
                            <div>
                                <a-select ref="select" v-model:value="value1" style="width: 100px" @focus="focus"
                                    @change="handleChange">
                                    <a-select-option value="ru">RU</a-select-option>
                                    <a-select-option value="en">EN</a-select-option>
                                    <a-select-option value="uz">UZ</a-select-option>
                                </a-select>
                            </div>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>

        <!-- ///////////////////////////////// -->
        <!-- ////////// BOTTOM NAVBAR /////// -->
        <!-- /////////////////////////////// -->
        <div class="bottom_navbar">
            <div class="container">
                <Row align="middle">
                    <Col :xs="24" :sm="24" :md="19" :lg="19">
                        <div class="bottom_left">
                            <div class="banner">
                                <router-link to="/">
                                    <span class="you">You</span>
                                    <span class="car">Car</span>
                                </router-link>
                            </div>

                            <!-- Mobile Search (центрда) -->
                            <div class="mobile_search">
                                <a-input-search v-model:value="value" placeholder="Поиск по названию" />
                            </div>

                            <div class="dropdown-wrapper">
                                <div>
                                    <span><router-link to="/avtomobiles">Автомобили</router-link></span>
                                    <SwapRightOutlined class="avto_icon" />
                                </div>
                                <div>
                                    <span><router-link to="/transport">Коммерческий транспорт</router-link></span>
                                    <SwapRightOutlined class="avto_icon" />
                                </div>
                                <div>
                                    <span><router-link to="/moto">Мотоциклы</router-link></span>
                                    <SwapRightOutlined class="avto_icon" />
                                </div>
                            </div>

                            <div class="search">
                                <a-input-search v-model:value="value" placeholder="input search text"
                                    style="width: 400px" />
                            </div>

                            <div class="message">
                                <router-link to="/">
                                    <a-badge count="0">
                                        <CommentOutlined class="messanger" />
                                    </a-badge>
                                </router-link>
                            </div>

                            <!-- Mobile Menu Button (o'ng tarafda) -->
                            <div class="mobile_menu_btn" @click="toggleMobileMenu">
                                <MenuOutlined v-if="!isMobileMenuOpen" />
                                <CloseOutlined v-else />
                            </div>
                        </div>
                    </Col>

                    <Col :xs="0" :sm="0" :md="5" :lg="5">
                        <div class="bottom_rigth" v-if="userStore.access_token">
                            <router-link to="/profile">
                                <div class="avatar">
                                    <p>{{ userStore.username }}</p>
                                    <a-spin v-if="loading" />
                                    <img v-show="!loading" :src="userStore.avatarUrl" @load="onLoad" @error="onError"
                                        alt="avatar image">
                                </div>
                            </router-link>
                        </div>
                        <div class="bottom_rigth" v-else>
                            <Button>
                                <router-link to="/login">
                                    Войти
                                </router-link>
                            </Button>
                            <Button type="primary">
                                <router-link to="singup">
                                    Регистрация
                                </router-link>
                            </Button>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>

        <!-- ///////////////////////////////// -->
        <!-- ////////// MOBILE SIDEBAR ////// -->
        <!-- /////////////////////////////// -->
        <Transition name="sidebar">
            <div v-if="isMobileMenuOpen" class="mobile_sidebar_overlay" @click="closeMobileMenu">
                <div class="mobile_sidebar" @click.stop>
                    <!-- User Section -->
                    <div class="mobile_user_section" v-if="userStore.access_token">
                        <div class="mobile_avatar_wrapper" @click="toProfile">
                            <div class="mobile_avatar_circle">
                                <a-spin v-if="loading" />
                                <img v-show="!loading" :src="userStore.avatarUrl" @load="onLoad" @error="onError"
                                    alt="avatar">
                            </div>
                            <div class="mobile_user_info">
                                <p class="mobile_username">{{ userStore.username }}</p>
                            </div>
                            <div @click.stop>
                                <BellOutlined class="notification_icon" />
                            </div>
                        </div>
                    </div>

                    <!-- Language Selector -->
                    <div class="mobile_language_section" @click.stop>
                        <div class="language_label">
                            <GlobalOutlined class="language_icon" />
                            <span>Язык / Til</span>
                        </div>
                        <a-config-provider :getPopupContainer="(triggerNode) => triggerNode.parentNode">
                            <a-select v-model:value="value1" style="width: 100%" size="large" @change="handleChange">
                                <a-select-option value="ru">Русский</a-select-option>
                                <a-select-option value="en">English</a-select-option>
                                <a-select-option value="uz">O'zbekcha</a-select-option>
                            </a-select>
                        </a-config-provider>
                    </div>

                    <!-- Main Menu -->
                    <div class="mobile_menu_section">
                        <!-- Top Menu Items -->
                        <div class="mobile_menu_group">
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Главная</span>
                            </router-link>
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Каталог</span>
                            </router-link>
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>О нас</span>
                            </router-link>
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Новости</span>
                            </router-link>
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Контакты</span>
                            </router-link>
                        </div>

                        <!-- Category Section -->
                        <div class="mobile_menu_group">
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Автомобили</span>
                                <RightOutlined class="menu_icon_right" />
                            </router-link>
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Коммерческий транспорт</span>
                                <RightOutlined class="menu_icon_right" />
                            </router-link>
                            <router-link to="/" class="mobile_menu_item" @click="closeMobileMenu">
                                <span>Мотоциклы</span>
                                <RightOutlined class="menu_icon_right" />
                            </router-link>
                        </div>

                        <!-- Contact Section -->
                        <div class="mobile_contact_section">
                            <a href="tel:+771232904" class="mobile_contact_item">
                                <PhoneOutlined />
                                <span>+77 123 29 04</span>
                            </a>
                            <a href="mailto:suvonovjavohir625@gmail.com" class="mobile_contact_item">
                                <MailOutlined />
                                <span>suvonovjavohir625@gmail.com</span>
                            </a>
                        </div>

                        <!-- Social Icons -->
                        <div class="mobile_social_section">
                            <a href="#" class="social_icon">
                                <InstagramOutlined />
                            </a>
                            <a href="#" class="social_icon">
                                <WhatsAppOutlined />
                            </a>
                            <a href="#" class="social_icon">
                                <LinkedinOutlined />
                            </a>
                        </div>

                        <!-- Auth Buttons -->
                        <div class="mobile_auth_section" v-if="!userStore.access_token">
                            <Button type="primary" block size="large">
                                <router-link to="singup" @click="closeMobileMenu">
                                    Регистрация
                                </router-link>
                            </Button>
                            <Button block size="large">
                                <router-link to="login" @click="closeMobileMenu">
                                    Войти
                                </router-link>
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </Transition>
    </header>
</template>

<script setup>
import { Button, Row, Col } from 'ant-design-vue';
import {
    CommentOutlined,
    InstagramOutlined,
    LinkedinOutlined,
    MailOutlined,
    PhoneOutlined,
    SwapRightOutlined,
    WhatsAppOutlined,
    MenuOutlined,
    CloseOutlined,
    RightOutlined,
    BellOutlined,
    GlobalOutlined
} from "@ant-design/icons-vue"
import { ref, watch } from 'vue';
import { useUserStore } from '@/store/useUserStore';
import router from '@/router';

const userStore = useUserStore()
const value1 = ref('ru');
const value = ref("")
const loading = ref(true)
const isMobileMenuOpen = ref(false)

const focus = () => {
    console.log('focus');
};

const handleChange = value => {
    console.log(`selected ${value}`);
};

const onLoad = () => {
    loading.value = false
}

const onError = () => {
    loading.value = false
}

const toggleMobileMenu = () => {
    isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
}

const toProfile = () => {
    const access_token = localStorage.getItem("access_token")
    if (access_token) {
        router.push('profile')
        closeMobileMenu()
    }
}

// Prevent body scroll when mobile menu is open
watch(isMobileMenuOpen, (newValue) => {
    if (newValue) {
        document.body.style.overflow = 'hidden'
    } else {
        document.body.style.overflow = ''
    }
})
</script>

<style scoped>
/* UNDER NAVBAR */
.under_navbar {
    background-color: #F6F6F6;
    padding: 15px 0;
}

.menu_list {
    display: flex;
    height: 100%;
    gap: 15px;
    padding-left: 0;
    margin-bottom: 0;
    align-items: center;
}

.menu_list li {
    list-style: none;
    font-weight: 500;
    font-size: 14px;
    color: #434343;
}

.menu_list li a {
    color: inherit;
}

.under_rigth {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 20px;
    justify-content: space-between;
}

.under_rigth span {
    font-weight: 400;
    color: #989898;
    font-size: 14px;
}

.icons {
    display: flex;
    gap: 10px;
    align-items: center;
}

.icon {
    font-size: 18px;
    color: #989898;
}

/* BOTTOM NAVBAR */
.bottom_navbar {
    padding: 20px 0;
    background-color: #FFFFFF;
    box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.15);
}

.banner span {
    font-size: 30px;
    font-weight: 700;
}

.banner .you {
    color: #2684E5;
}

.banner .car {
    color: #010101;
}

.bottom_left {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.messanger {
    font-size: 20px;
}

.bottom_rigth {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: end;
}

/* Dropdown wrapper styling */
.dropdown-wrapper {
    display: flex;
    gap: 15px;
}

.dropdown-wrapper>div {
    display: flex;
    align-items: center;
    gap: 4px;
}

.dropdown-wrapper>div a {
    color: inherit;
}

.dropdown-wrapper>div span {
    font-weight: 400;
    font-size: 16px;
    color: #010101;
}

.avto_icon {
    color: #2684E5 !important;
}

.avatar {
    display: flex;
    align-items: center;
    gap: 15px;
}

.avatar p {
    margin-bottom: 0;
    color: #293843ed;
    font-size: 14px;
    font-weight: 400;
}

.avatar img {
    width: 32px;
    height: 32px;
    border-radius: 100%;
}

/* Mobile Menu Button */
.mobile_menu_btn {
    display: none;
    font-size: 24px;
    cursor: pointer;
    color: #010101;
}

/* Mobile Search */
.mobile_search {
    display: none;
}

/* ///////////////////////////////// */
/* ////////// MOBILE SIDEBAR ////// */
/* ///////////////////////////////// */

.mobile_sidebar_overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9999;
}

.mobile_sidebar {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 85%;
    max-width: 320px;
    background-color: #FFFFFF;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.mobile_user_section {
    padding: 20px 16px;
    background-color: #F6F6F6;
    border-bottom: 1px solid #E8E8E8;
}

.mobile_avatar_wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}

.mobile_avatar_circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background-color: #2684E5;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 18px;
    overflow: hidden;
}

.mobile_avatar_circle img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.mobile_user_info {
    flex: 1;
}

.mobile_username {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
    color: #010101;
}

.notification_icon {
    font-size: 20px;
    color: #2684E5;
    cursor: pointer;
}

.mobile_language_section {
    padding: 16px;
    border-bottom: 1px solid #E8E8E8;
    background-color: #FFFFFF;
}

.language_label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
    color: #434343;
    font-size: 14px;
    font-weight: 500;
}

.language_icon {
    font-size: 18px;
    color: #2684E5;
}

.mobile_menu_section {
    flex: 1;
    padding: 8px 0;
}

.mobile_menu_group {
    border-bottom: 1px solid #E8E8E8;
    padding: 8px 0;
}

.mobile_menu_item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    color: #010101;
    font-size: 15px;
    text-decoration: none;
    transition: background-color 0.2s;
}

.mobile_menu_item:hover {
    background-color: #F6F6F6;
}

.menu_icon_right {
    color: #989898;
    font-size: 14px;
}

.mobile_contact_section {
    padding: 16px;
    border-bottom: 1px solid #E8E8E8;
}

.mobile_contact_item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    color: #010101;
    text-decoration: none;
    font-size: 14px;
}

.mobile_contact_item span {
    color: #010101;
}

.mobile_social_section {
    display: flex;
    gap: 16px;
    padding: 16px;
    border-bottom: 1px solid #E8E8E8;
}

.social_icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #2684E5;
}

.social_icon img {
    width: 100%;
    height: 100%;
}

.mobile_auth_section {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-bottom: 1px solid #E8E8E8;
}

/* Sidebar Transition */
.sidebar-enter-active,
.sidebar-leave-active {
    transition: opacity 0.3s ease;
}

.sidebar-enter-active .mobile_sidebar,
.sidebar-leave-active .mobile_sidebar {
    transition: transform 0.3s ease;
}

.sidebar-enter-from,
.sidebar-leave-to {
    opacity: 0;
}

.sidebar-enter-from .mobile_sidebar,
.sidebar-leave-to .mobile_sidebar {
    transform: translateX(100%);
}

/* ///////////////////////////////// */
/* ////////// RESPONSIVE ////////// */
/* ///////////////////////////////// */

/* Tablet (768px - 991px) */
@media (max-width: 991px) {
    .under_navbar {
        display: none;
    }

    .dropdown-wrapper {
        display: none;
    }

    .search {
        flex: 1;
    }

    .search .ant-input-search {
        width: 100% !important;
    }

    .banner span {
        font-size: 24px;
    }
}

/* Mobile (до 767px) */
@media (max-width: 767px) {
    .under_navbar {
        display: none;
    }

    .bottom_navbar {
        padding: 12px 0;
    }

    .mobile_menu_btn {
        display: block;
    }

    .dropdown-wrapper {
        display: none;
    }

    .search {
        display: none;
    }

    .message {
        display: none;
    }

    .mobile_sidebar_overlay {
        display: block;
    }

    .mobile_search {
        display: block;
        flex: 1;
        margin: 0 15px;
    }

    .mobile_search .ant-input-search {
        width: 100%;
    }

    .banner span {
        font-size: 22px;
    }

    .bottom_left {
        gap: 0;
        width: 100%;
    }
}

/* Extra small mobile */
@media (max-width: 375px) {
    .banner span {
        font-size: 20px;
    }

    .mobile_sidebar {
        width: 90%;
    }
}
</style>