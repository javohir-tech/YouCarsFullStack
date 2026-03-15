<template>
    <a-auto-complete v-model:value="searchQuery" style="width: 400px" placeholder="Mashina qidirish..."
        :options="options" :default-active-first-option="false" :loading="loading" @search="onSearch" @select="onSelect"
        @keydown.enter="OnEnter">
        <a-input>
            <template #suffix>
                <search-outlined :spin="loading" />
            </template>
        </a-input>
    </a-auto-complete>
</template>

<script setup>
import router from '@/router'
import api from '@/utils/axios'
import { SearchOutlined } from '@ant-design/icons-vue'
import { ref } from 'vue'

const searchQuery = ref('')
const options = ref([])
const loading = ref(false)
let debounceTimer = null
const isSelected = ref(false)

const onSearch = (val) => {
    clearTimeout(debounceTimer)

    if (!val.trim()) {
        options.value = []
        return
    }

    debounceTimer = setTimeout(async () => {
        loading.value = true
        try {
            const { data } = await api('/cars/filter/', {
                params: { search: val }
            })
            console.log(data.result)
            options.value = data.result.map(car => ({
                label: `${car.marka} - ${car.car_model}`,
                value: String(car.id),
                car: car
            }))
        } catch (error) {
            console.log(error)
        } finally {
            loading.value = false
        }
    }, 300)
}

const onSelect = (val, option) => {
    const currentSearchQuery = searchQuery.value
    console.log(currentSearchQuery)
    searchQuery.value = option.label
    isSelected.value = true
    const car = option.car
    console.log(option.car)
    router.push({
        name: "result",
        query: {
            marka: car.marka,
            car_model: car.car_model,
        }
    })
}


const OnEnter = () => {
    if (isSelected.value) {
        isSelected.value = false
        return
    }
    router.push({
        name: "result",
        query: {
            search: searchQuery.value
        }
    })
    console.log("Qidirilayotgan:", searchQuery.value)
}
</script>