<template>
    <div class="car_container">
        <h1>Избранное</h1>
        <div v-if="loading" class="loading">
            <a-spin clas="spin" size="large" tip="loading..." />
        </div>
        <div v-if="cars.length === 0 && !getError && !loading" class="empty">
            <a-empty description="Нет сохраненных объявлений" />
            <p>Чтобы добавить авто в избранное, нажмите на сердечко на карточке машины!</p>
            <router-link to="/">
                <a-button type="primary">Перейти в каталог</a-button>
            </router-link>
        </div>
        <div v-if="getError" class="error">
            <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist." />
        </div>
        <div v-if="!loading && !getError && cars.length > 0" class="storage_cars">
            <a-row :gutter="[16, 24]">
                <a-col v-for="car in cars" :key="car.id" class="gutter-row" :xl="10" :md="12" :sm="24" :xs="24">
                    <CarCard :id="car.id" :model="car.car_model" :like="car.me_liked" :images="car.images"
                        :marka="car.marka" :price="car.price" :milage="car.milage" :displacement="car.displacement"
                        :year="car.year" :transmission_type="car.transmission_type" :power="car.power" :fuel="car.fuel"
                        :drive_type="car.drive_type" :country="car.country" @dislike="handleDislike" />
                </a-col>
            </a-row>
            <a-pagination v-if="total" class="pagination" v-model:current="current" :total="total"
                show-less-items />
        </div>
    </div>
</template>


<script setup>
import { CarCard } from '@/components';
import api from '@/utils/axios';
import { onMounted, ref } from 'vue';

const cars = ref([])
const loading = ref(false)
const getError = ref(false)
const current = ref(2);
const total = ref(0);


const getMeLikedcars = async () => {
    loading.value = true
    try {
        const { data } = await api.get("/cars/cars/meliked/")
        cars.value = data.result
        total.value = data.count
    } catch (error) {
        getError.value = true
        console.log(error.response || error)
    } finally {
        loading.value = false
    }
}

const handleDislike = (id) => {
    cars.value = cars.value.filter(c => c.id !== id)
}

onMounted(() => {
    getMeLikedcars()
})
</script>

<style scoped>
.loading,
.empty,
.error {
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    height: 300px;
}

.spin {
    flex: 1;
}

.car_container {
    padding: 20px;

    h1 {
        font-size: 30px;
        font-weight: 600;
        color: #293843;
        margin-bottom: 20px;
    }
}

.pagination {
    text-align: end;
    margin: 15px 0px;
}
</style>