<template>
    <div class="my_cars">
        <div v-if="!loading">
            <div v-for="item in cars_data" class="my_car" :key="item.id" @click="handleNavigate(item.id)">

                <a-row :gutter="[16, 24]">
                    <!-- Left section: image + info - responsive breakpoints -->
                    <a-col class="gutter-row" :xs="24" :sm="24" :md="14" :lg="14" :xl="14">
                        <div class="car_left">
                            <div class="car_image" v-if="item.images.length > 0">
                                <a-skeleton-image v-if="imageLoading" />
                                <img v-show="!imageLoading" @load="onLoad" @error="onError" :src="item.images[0].image"
                                    alt="car_image">

                                <!-- Dropdown menu overlay - faqat mobile uchun -->
                                <a-dropdown placement="bottomLeft" class="dropdown_mobile">
                                    <a class="ant-dropdown-link" @click.prevent>
                                        <EllipsisOutlined class="car_menu_mobile" />
                                    </a>
                                    <template #overlay>
                                        <a-menu>
                                            <a-menu-item>
                                                <router-link :to="`/update/${item.id}`">
                                                    Редактировать
                                                </router-link>
                                            </a-menu-item>
                                            <a-menu-item>
                                                <a @click="handleKeepDeactive(item.id)">Снять с публикации</a>
                                            </a-menu-item>
                                        </a-menu>
                                    </template>
                                </a-dropdown>
                            </div>
                            <div class="car_info">
                                <p class="car_name">
                                    {{ capitalizeWords(item.marka) }} {{ capitalizeWords(item.car_model) }}, {{
                                        item.year }}
                                </p>
                                <p class="car_price">{{ item.price }}$</p>
                                <p class="car_country">{{ capitalizeWords(item.country) }}</p>
                            </div>
                        </div>
                    </a-col>

                    <!-- Right section: stats + menu -->
                    <a-col class="gutter-row" :xs="24" :sm="24" :md="10" :lg="10" :xl="10">
                        <div class="car_right">
                            <div class="car_status">
                                <a-flex class="car_view" gap="10" align="center">
                                    <EyeOutlined class="car_info_icon" />
                                    <p>{{ item.views }}</p>
                                </a-flex>
                                <a-flex class="car_view" gap="10" align="center">
                                    <UserOutlined class="car_info_icon" />
                                    <p>{{ item.inquiries || 0 }}</p>
                                </a-flex>
                                <a-flex class="car_view" gap="10" align="center">
                                    <HeartOutlined class="car_info_icon heart_icon" />
                                    <p>{{ item.likes_count }}</p>
                                </a-flex>
                                <a-flex class="car_view" gap="10" align="center">
                                    <MessageOutlined class="car_info_icon" />
                                    <p>{{ item.messages || 'Нет новых сообщений' }}</p>
                                </a-flex>
                            </div>

                            <!-- Dropdown menu - desktop uchun -->
                            <a-dropdown @click.stop placement="bottomLeft" class="dropdown_desktop">
                                <a class="ant-dropdown-link" @click.prevent>
                                    <EllipsisOutlined class="car_menu_desktop" />
                                </a>
                                <template #overlay>
                                    <a-menu>
                                        <a-menu-item>
                                            <router-link :to="`/update/${item.id}`">
                                                Редактировать
                                            </router-link>
                                        </a-menu-item>
                                        <a-menu-item>
                                            <a @click="handleKeepDeactive(item.id)">Снять с публикации</a>
                                        </a-menu-item>
                                    </a-menu>
                                </template>
                            </a-dropdown>
                        </div>
                    </a-col>
                </a-row>
            </div>

            <a-pagination style="text-align: end;" v-if="total > 10" @change="handlePagination" class="pagination"
                v-model:current="current" :total="total" show-less-items />
        </div>

        <div class="loader" v-if="loading">
            <a-spin />
        </div>

        <div class="error" v-if="error" style="height: 400px;">
            <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist." />
        </div>

        <div class="empty" v-if="total === 0 && !loading && !error">
            <a-empty />
        </div>
    </div>
</template>

<script setup>
import api from '@/utils/axios'
import { EllipsisOutlined, EyeOutlined, HeartOutlined, MessageOutlined, UserOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ─── Data ────────────────────────────────────
const error = ref(false)
const loading = ref(false)
const cars_data = ref([])
const keepLoading = ref(false)
const total = ref(0)
const current = ref(1)
const imageLoading = ref(true)

const handlePagination = (value) => {
    getUserDraftCars(value)
}

const handleNavigate = (id) => {
    router.push(`/cars/detail/${id}`)
}


// ─── Fetch cars ──────────────────────────────
const getUserDraftCars = async (page) => {
    loading.value = true
    try {
        const { data } = await api.get('/cars/user/cars/published/', {
            params: {
                page: page
            }
        })
        total.value = data.count
        cars_data.value = data.result
    } catch (err) {
        error.value = true
        console.log(err.response || err)
    } finally {
        loading.value = false
    }
}

const onLoad = () => {
    imageLoading.value = false
}

const onError = () => {
    imageLoading.value = false
}

onMounted(() => {
    getUserDraftCars()
})



const handleKeepDeactive = async (carId) => {
    keepLoading.value = true
    try {
        const response = await api.patch(`/cars/car/${carId}/`, {
            status: "DF"
        })
        cars_data.value = cars_data.value.filter(c => c.id !== carId)
        message.success(response.data.message)
        total.value -= 1
        if (cars_data.value.length === 0) {
            getUserDraftCars()
        }
    } catch (err) {
        console.log(err.response || err)
    } finally {
        keepLoading.value = false
    }
}


function capitalizeWords(text) {
    if (!text) return text
    return text.split(" ").map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(" ")
}
</script>

<style scoped>
/* === Loader  === */

.loader,
.error,
.empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 300px;
}

/* ═══ PAGE ═══ */
.my_cars {
    margin: 10px auto;
}

/* ═══ CAR CARD ═══ */
.my_car {
    padding: 14px;
    border-radius: 10px;
    background-color: #F6F6F6;
    margin-bottom: 12px;
}

/* Left: image + name/price/country — fills available space */
.car_left {
    display: flex;
    gap: 8px;
    align-items: flex-start;
    flex: 1;
    min-width: 0;
}

.car_image {
    position: relative;
}

.car_image img {
    width: 186px;
    height: 125px;
    border-radius: 10px;
    object-fit: cover;
}

.car_info p {
    margin-bottom: 6px;
}

.car_name {
    font-weight: 400;
    font-size: 17px;
    color: #293843;
    margin-top: 6px !important;
}

.car_price {
    font-weight: 700;
    font-size: 20px;
    color: #293843;
}

.car_country {
    font-weight: 400;
    font-size: 14px;
    color: #989898;
}

/* Right: stats + menu */
.car_right {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    height: 100%;
    flex-shrink: 0;
    margin-left: auto;
}

.car_status {
    display: flex;
    flex-direction: column;
    gap: 8px;
    height: 100%;
    justify-content: center;
}

.car_status_label {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 2px !important;
}

.status_sold {
    color: #293843;
}

.status_active {
    color: #4caf50;
}

.car_view p {
    margin: 0;
    font-size: 14px;
    color: #293843;
}

.car_info_icon {
    font-size: 16px;
    color: #293843;
}

.heart_icon {
    color: #e53935 !important;
}

/* Dropdown desktop */
.dropdown_desktop {
    display: block;
}

.dropdown_mobile {
    display: none;
}

/* Menu button - Desktop (o'ng tomonda) */
.car_menu_desktop {
    padding: 6px;
    font-size: 18px;
    background-color: #fff;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
    transform: rotate(90deg);
}

.car_menu_desktop:hover {
    background-color: #ececec;
}

/* Dropdown menu overlay on image - mobile */
.car_image .ant-dropdown-link {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 10;
}

.car_menu_mobile {
    padding: 6px;
    font-size: 18px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
    transform: rotate(90deg);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.car_menu_mobile:hover {
    background-color: #fff;
}

/* ═══════════════════════════════════════════════════ */
/* ═══ RESPONSIVE STYLES ═══ */
/* ═══════════════════════════════════════════════════ */

/* Tablet va kichikroq ekranlar (1012px va past) */
@media (max-width: 1012px) {
    .car_image img {
        width: 150px;
        height: 100px;
    }

    .car_name {
        font-size: 15px;
    }

    .car_price {
        font-size: 18px;
    }

    .car_left {
        gap: 8px;
    }
}

/* Medium tablet (768px - 1012px) */
@media (max-width: 768px) {
    .my_car {
        padding: 12px;
    }

    .car_left {
        gap: 8px;
    }

    .car_image img {
        width: 140px;
        height: 95px;
    }

    /* Desktop dropdown yashirish, mobile ko'rsatish */
    .dropdown_desktop {
        display: none;
    }

    .dropdown_mobile {
        display: block;
    }

    /* Stats qismi pastga tushadi */
    .car_right {
        margin-left: 0;
        margin-top: 12px;
        justify-content: flex-start;
    }

    .car_status {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 12px;
        flex: 1;
    }

    .car_view {
        min-width: 70px;
    }
}

/* Mobile ekranlar (576px va past) */
@media (max-width: 576px) {
    .my_car {
        padding: 10px;
    }

    /* Rasm va info vertical */
    .car_left {
        flex-direction: column;
        gap: 8px;
    }

    .car_image {
        width: 100%;
    }

    .car_image img {
        width: 100%;
        height: auto;
        max-height: 200px;
    }

    .car_name {
        font-size: 16px;
        margin-top: 0 !important;
    }

    .car_price {
        font-size: 20px;
    }

    /* Stats grid layout */
    .car_right {
        margin-top: 10px;
    }

    .car_status {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }

    .car_view {
        min-width: auto;
    }

    .car_view p {
        font-size: 13px;
    }

    .car_info_icon {
        font-size: 14px;
    }
}

/* Juda kichik ekranlar (400px va past) */
@media (max-width: 400px) {
    .my_cars {
        margin: 5px auto;
    }

    .my_car {
        padding: 8px;
        margin-bottom: 10px;
    }

    .car_name {
        font-size: 14px;
    }

    .car_price {
        font-size: 18px;
    }

    .car_country {
        font-size: 13px;
    }

    .car_view p {
        font-size: 12px;
    }

    .car_info_icon {
        font-size: 13px;
    }
}
</style>