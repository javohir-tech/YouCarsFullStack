<template>
    <div class="my_cars">
        <div v-if="!loading" v-for="item in cars_data" class="my_car" :key="item.id">

            <a-row :gutter="[16, 24]">
                <a-col class="gutter-row" :span="14">
                    <div class="car_left">
                        <div class="car_image" v-if="item.images.length > 0">
                            <img :src="item.images[0].image" alt="car_image">
                        </div>
                        <div class="car_info">
                            <p class="car_name">
                                {{ item.marka }} {{ item.car_model }}, {{ item.year }}
                            </p>
                            <p class="car_price">{{ item.price }}$</p>
                            <p class="car_country">{{ item.country }}</p>
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :span="10">
                    <div class="car_right">
                        <div class="car_status">
                            <a-flex class="car_view" gap="10" align="center">
                                <EyeOutlined class="car_info_icon" />
                                <p>{{ item.views || 0 }}</p>
                            </a-flex>
                            <a-flex class="car_view" gap="10" align="center">
                                <UserOutlined class="car_info_icon" />
                                <p>{{ item.inquiries || 0 }}</p>
                            </a-flex>
                            <a-flex class="car_view" gap="10" align="center">
                                <HeartOutlined class="car_info_icon heart_icon" />
                                <p>{{ item.likes || 0 }}</p>
                            </a-flex>
                            <a-flex class="car_view" gap="10" align="center">
                                <MessageOutlined class="car_info_icon" />
                                <p>{{ item.messages || 'Нет новых сообщений' }}</p>
                            </a-flex>
                        </div>
                        <a-dropdown placement="bottomLeft">
                            <a class="ant-dropdown-link" @click.prevent>
                              <EllipsisOutlined class="car_menu" />
                            </a>
                            <template #overlay>
                                <a-menu>
                                    <a-menu-item>
                                        <a href="javascript:;">Редактировать</a>
                                    </a-menu-item>
                                    <a-menu-item>
                                        <a href="javascript:;">Снять с публикации</a>
                                    </a-menu-item>
                                </a-menu>
                            </template>
                        </a-dropdown>
                    </div>
                </a-col>
            </a-row>
        </div>

        <div class="loader" v-if="loading">
            <a-spin />
        </div>

        <div class="error" v-if="error" style="height: 200px;">
            <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist." />
        </div>

        <div class="empty" v-if="cars_data.length === 0 && !loading">
            <a-empty />
        </div>
    </div>
</template>

<script setup>
import api from '@/utils/axios'
import { DownOutlined, EllipsisOutlined, EyeOutlined, HeartOutlined, MessageOutlined, UserOutlined } from '@ant-design/icons-vue'
import { onMounted, ref } from 'vue'

// ─── Data ────────────────────────────────────
const error = ref(false)
const loading = ref(false)
const cars_data = ref([])

// ─── Fetch cars ──────────────────────────────
const getUserDraftCars = async () => {
    loading.value = true
    try {
        const { data } = await api.get('/cars/user/cars/published/')
        console.log(data)
        cars_data.value = data.result
    } catch (err) {
        error.value = true
        console.log(err.response || err)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    getUserDraftCars()
})


// ─── Оставить активным ───────────────────────
// ← o'z API chaqirigingiz yozing
const handleKeepDeactive = async () => {
    keepLoading.value = true
    try {
        // await api.patch(`/cars/${selectedCar.value.id}/`, { status: 'active' })

        // Lokal status "active" qilib qo'yildi
        const car = cars_data.value.find(c => c.id === selectedCar.value.id)
        if (car) {
            car.status = 'active'
        }

        closeModal()
    } catch (err) {
        console.log(err.response || err)
    } finally {
        keepLoading.value = false
    }
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
    gap: 20px;
    align-items: flex-start;
    flex: 1;
    min-width: 0;
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

/* Right: stats + menu — pinned to right edge */
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

.car_menu {
    padding: 6px;
    font-size: 18px;
    background-color: #fff;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s;
    transform: rotate(90deg);
}

.car_menu:hover {
    background-color: #ececec;
}
</style>