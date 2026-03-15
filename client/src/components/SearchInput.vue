<template>
    <a-auto-complete v-model:value="searchQuery" style="width: 400px" placeholder="Mashina qidirish..."
        :options="options" :loading="loading" @search="onSearch" @select="onSelect">
        <a-input>
            <template #suffix>
                <search-outlined :spin="loading" />
            </template>
        </a-input>
    </a-auto-complete>
</template>

<script setup>
import api from '@/utils/axios'
import { SearchOutlined } from '@ant-design/icons-vue'
import { ref } from 'vue'

const searchQuery = ref('')
const options = ref([])
const loading = ref(false)
let debounceTimer = null

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

            options.value = data.result.map(car => ({
                label: `${car.marka} - ${car.car_model}-${car.author}`,
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
    searchQuery.value = option.label
    // router.push(`/cars/${val}`)
}
</script>