<template>
    <div class="car_container">
        <h1>Saqlanganlar</h1>
        <div>
            <a-row :gutter="[16, 24]">
                <a-col v-for="car in cars" :key="car.id" class="gutter-row" :xl="8" :md="12" :sm="24" :xs="24">
                    <CarCard :id="car.id" :model="car.car_model" :like="car.me_liked" :image="car.images[0].image" :marka="car.marka" :price="car.price" :milage="car.milage" :displacement="car.displacement" :year="car.year" :transmission_type="car.transmission_type" :power="car.power" :fuel="car.fuel" :drive_type="car.drive_type" :country="car.country"/>
                </a-col>
            </a-row>
        </div>
    </div>
</template>


<script setup>
import { CarCard } from '@/components';
import api from '@/utils/axios';
import { onMounted, ref } from 'vue';

const cars = ref([])
const loading = ref(false)

const getMeLikedcars = async() => {
    loading.value = true
    try {
        const {data} =  await api.get("/cars/cars/meliked/")
        cars.value = data.result
    } catch (error) {
        console.log(error.response || error)
    }finally{
        loading.value =  false
    }
}

onMounted(()=>{
    getMeLikedcars()
})
</script>

<style scoped>
.car_container {
    padding: 20px;

    h1 {
        font-size: 30px;
        font-weight: 600;
        color: #293843;
        margin-bottom: 20px;
    }
}
</style>