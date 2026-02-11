<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item>Каталог</a-breadcrumb-item>
        </a-breadcrumb>

        <div>
            <div class="header">
                <h1>
                    Каталог
                </h1>
            </div>
            <Filter @params="handleGetcCars" :count="filterCount" @clear="handleClear"/>
        </div>
        <div class="katalok_section">
            <a-row class="cars" :gutter="[16, 24]">
                <a-col v-if="carsLoading" v-for="_ in new Array(12).fill(0)" :xs="24" :md="12" :lg="8" :xl="6">
                    <a-skeleton active />
                </a-col>
                <a-col v-if="!carsLoading && carsData.length > 0" v-for="car in carsData" class="gutter-row" :xs="24"
                    :md="12" :lg="8" :xl="6">
                    <CarCard :id="car.id" :model="car.car_model" :like="car.me_liked" :images="car.images"
                        :marka="car.marka" :price="car.price" :milage="car.milage" :displacement="car.displacement"
                        :year="car.year" :transmission_type="car.transmission_type" :power="car.power" :fuel="car.fuel"
                        :drive_type="car.drive_type" :country="car.country" />
                </a-col>
            </a-row>

            <a-pagination class="pagination" @change="handlePagination" v-model="current" :total="total" />
        </div>
        <CallCard/>
    </div>
</template>

<script setup>
import { CallCard, CarCard, Filter } from '@/components';
import api from '@/utils/axios';
import { onMounted, ref } from 'vue';

const carsData = ref([])
const carsLoading = ref(false)
const filterCount = ref(0)
const total = ref(0)

const filterParams = ref({})

const current = ref(1)

const handlePagination = async (pagination)=>{
    const pagination_params = { ...filterParams.value , page : pagination }
    handleGetcCars(pagination_params)
}

const handleClear = () =>{
    filterCount.value = 0
}

///////////////////////////////////////////////////////
////////////// GET CARS         //////////////////////
//////////////////////////////////////////////////////
const handleGetcCars = async (params) => {
    console.log(params)
    carsLoading.value = true
    try {
        const response = await api.get(`/cars/cars/`, {
            params: {
                page_size: 12,
                ...params
            }
        })
        console.log(response)
        total.value = response.data.count
        carsData.value = response.data.result
        if (params) {
            filterParams.value = params
            filterCount.value = response.data.count
        } else {
            filterCount.value = 0
        }
    } catch (error) {
        console.log(error.response || error)
    } finally {
        carsLoading.value = false
    }
}

onMounted(() => {
  handleGetcCars()
})
</script>

<style scoped>
.katalok_section {
    margin-top: 30px;
}

.pagination{
    margin-top: 30px;
    text-align: end;
}
</style>