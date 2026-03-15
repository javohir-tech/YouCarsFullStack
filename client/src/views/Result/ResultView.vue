<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item>{{ getInitialSearch() }}</a-breadcrumb-item>
        </a-breadcrumb>

        <a-row class="results" :gutter="[16, 24]">
            <a-col v-if="loading" class="gutter-row" v-for="_ in new Array(8).fill(0)" :xs="24" :md="12" :lg="8"
                :xl="6">
                <a-skeleton active />
            </a-col>
            <a-col v-else-if="!loading && results.length > 0" v-for="car in results" class="gutter-row" :key="car.id"
                :xs="24" :md="12" :lg="8" :xl="6">
                <CarCard :id="car.id" :model="car.car_model" :like="car.me_liked" :images="car.images"
                    :marka="car.marka" :price="car.price" :milage="car.milage" :displacement="car.displacement"
                    :year="car.year" :transmission_type="car.transmission_type" :power="car.power" :fuel="car.fuel"
                    :drive_type="car.drive_type" :country="car.country" />
            </a-col>
        </a-row>
        <a-pagination v-if="results.length > 0" class="pagination" @v-model:pageSize="pageSize"
            @change="handlePagination" v-model:current="current" :show-size-changer="total > 500" :total="total"
            :pageSize="pageSize" />
        <div v-if="!loading && results.length === 0" class="empty">
            <a-empty description="natijalar topilmadi" />
        </div>

        <CallCard />
    </div>
</template>

<script setup>
import { CallCard, CarCard } from '@/components';
import api from '@/utils/axios';
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()

//// fetch
const loading = ref(false)
const results = ref([])
////// Pagination
const pageSize = ref(12)
const current = ref(1)
const total = ref(0)

const getInitialSearch = () => {
    const { search, marka, model } = route.query
    if (marka && model) return `${marka}-${model}`
    if (marka) return marka
    if (search) return search
    return ""
}

const getResult = async (params) => {
    loading.value = true
    try {
        const { data } = await api.get("/cars/cars/", {
            params: { ...params, page_size: 12 }
        })
        console.log(data)
        total.value = data.count
        results.value = data.result
    } catch (error) {
        console.log(error.response || error)
    } finally {
        loading.value = false
    }
}

const handlePagination = (page) => {
    current.value = page
    const params = { ...route.query, page }
    window.scroll({
        top: 0,
        behavior: "smooth"
    })
    getResult(params)
}

watch(() => route.query, () => {
    getResult(route.query)
    getInitialSearch()
})

onMounted(() => {
    getResult(route.query)
})
</script>

<style scoped>
.pagination {
    margin-top: 30px;
    text-align: end;
}
</style>