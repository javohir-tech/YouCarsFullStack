<template>
    <div class="my_cars">
        <div v-if="!loading" v-for="item in cars_data" class="my_car" :key="item.id">

            <a-row :gutter="[16, 24]">
                <a-col class="gutter-row" :span="14">
                    <div class="car_left">
                        <div class="car_image" v-if="item.images.length > 0">
                            <a-skeleton-image v-if="imageLoading" />
                            <img v-show="!imageLoading" @load="onLoad" @error="onError" :src="item.images[0].image"
                                alt="car_image">
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
                            <p class="car_status_label"
                                :class="item.status === 'published' ? 'status_active' : 'status_sold'">
                                {{ item.status === 'active' ? 'Активен' : 'Продал на YouCar' }}
                            </p>
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
                                <p>{{ item.likes_count }}</p>
                            </a-flex>
                            <a-flex class="car_view" gap="10" align="center">
                                <MessageOutlined class="car_info_icon" />
                                <p>{{ item.messages || 'Нет новых сообщений' }}</p>
                            </a-flex>
                        </div>

                        <EllipsisOutlined class="car_menu" @click="openModal(item)" />
                    </div>
                </a-col>
            </a-row>
        </div>
        <a-pagination style="text-align: end;" v-if="total > 10" @change="handlePagination" class="pagination"
            v-model:current="current" :total="total" show-less-items />
        <div class="loader" v-if="loading">
            <a-spin />
        </div>

        <div class="error" v-if="error" style="height: 400px;">
            <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist." />
        </div>

        <div class="empty" v-if="total === 0 && !loading && !error">
            <a-empty />
        </div>
        <!-- ============ MODAL ============ -->
        <a-modal v-model:open="modalVisible" :footer="null" :width="400" :centered="true" class="delete_modal"
            @cancel="closeModal">
            <div class="modal_header" v-if="selectedCar">
                <div class="modal_car_image">
                    <img :src="selectedCar.images[0].image" alt="car_image">
                </div>
                <div class="modal_car_info">
                    <p class="modal_car_name">
                        {{ selectedCar.marka }} {{ selectedCar.car_model }}, {{ selectedCar.year }}
                    </p>
                    <p class="modal_car_price">{{ selectedCar.price }}$</p>
                    <p class="modal_car_country">{{ selectedCar.country }}</p>
                </div>
            </div>

            <div class="modal_reasons">
                <p class="modal_reasons_label">Выберите причину</p>
                <a-radio-group v-model:value="selectedReason" class="modal_radio_group">
                    <a-radio v-for="reason in deleteReasons" :key="reason.value" :value="reason.value"
                        class="modal_radio_item">
                        {{ reason.label }}
                    </a-radio>
                </a-radio-group>
            </div>

            <div class="modal_actions">
                <a-button class="modal_btn_delete" type="primary" :loading="deleteLoading" :disabled="!selectedReason"
                    @click="handleDelete">
                    Удалить
                </a-button>
                <a-button class="modal_btn_keep" :loading="keepLoading" @click="handleKeepActive">
                    Оставить активным
                </a-button>
            </div>
        </a-modal>
    </div>
</template>

<script setup>
import api from '@/utils/axios'
import { EllipsisOutlined, EyeOutlined, HeartOutlined, MessageOutlined, UserOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { onMounted, ref } from 'vue'

// ─── Data ────────────────────────────────────
const error = ref(false)
const loading = ref(false)
const cars_data = ref([])

// ─── Modal state ─────────────────────────────
const modalVisible = ref(false)
const selectedCar = ref(null)
const selectedReason = ref(null)
const deleteLoading = ref(false)
const keepLoading = ref(false)

const total = ref(0)
const current = ref(1)
const imageLoading = ref(true)

const handlePagination = (value) => {
    getUserDraftCars(value)
}

// ─── Delete reasons ──────────────────────────
const deleteReasons = [
    { value: 1, label: 'Продал на YouCar' },
    { value: 2, label: 'Продал где-то еще' },
    { value: 3, label: 'Другая причина' },
]

// ─── Fetch cars ──────────────────────────────
const getUserDraftCars = async (page) => {
    loading.value = true
    try {
        const { data } = await api.get('/cars/user/cars/draft/', {
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


// ─── Modal open / close ──────────────────────
function openModal(car) {
    selectedCar.value = car
    selectedReason.value = null
    modalVisible.value = true
}

function closeModal() {
    modalVisible.value = false
    selectedCar.value = null
    selectedReason.value = null
}


const handleDelete = async () => {
    if (!selectedReason.value) return

    deleteLoading.value = true
    try {
        console.log(selectedReason.value)
        console.log(selectedCar.value.id)
        const response = await api.delete(`/cars/car/${selectedCar.value.id}/`, {
            data: { reason: selectedReason.value }
        })
        message.success(response.data.message)
        cars_data.value = cars_data.value.filter(c => c.id !== selectedCar.value.id)
        total.value -= 1
        if (cars_data.value.length === 0) {
            getUserDraftCars()
        }
        closeModal()
    } catch (err) {
        console.log(err.response || err)
    } finally {
        deleteLoading.value = false
    }
}

const handleKeepActive = async () => {
    keepLoading.value = true
    try {
        const response = await api.patch(`/cars/car/${selectedCar.value.id}/`, {
            status: "PD"
        })
        message.success(response.data.message)
        cars_data.value = cars_data.value.filter(item => item.id !== selectedCar.value.id)
        closeModal()
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

onMounted(() => {
    getUserDraftCars()
})
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
    flex-shrink: 0;
    margin-left: auto;
}

.car_status {
    display: flex;
    flex-direction: column;
    gap: 8px;
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

/* ═══ MODAL ═══ */
.modal_header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
}

.modal_car_image img {
    width: 100px;
    height: 70px;
    border-radius: 8px;
    object-fit: cover;
}

.modal_car_info p {
    margin: 0 0 3px;
}

.modal_car_name {
    font-size: 14px;
    font-weight: 600;
    color: #293843;
}

.modal_car_price {
    font-size: 16px;
    font-weight: 700;
    color: #293843;
}

.modal_car_country {
    font-size: 12px;
    color: #989898;
}

.modal_reasons_label {
    font-size: 14px;
    font-weight: 600;
    color: #293843;
    margin: 0 0 12px;
}

.modal_radio_group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 24px;
}

.modal_radio_item {
    font-size: 14px;
    color: #293843;
}

.modal_actions {
    display: flex;
    gap: 12px;
}

.modal_btn_delete,
.modal_btn_keep {
    flex: 1;
    height: 42px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 600;
}

.modal_btn_keep {
    background-color: #f0f0f0;
    color: #333;
    border: none;
}

.modal_btn_keep:hover {
    background-color: #e4e4e4;
}
</style>