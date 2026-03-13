<template>
    <div class="markas_section">
        <a-row class="markas" :gutter="[0, 0]">
            <a-col v-if="loading" class="marka_col" v-for="_ in new Array(12).fill(1)" :xs="12" :sm="8" :md="6" :lg="4">
                <a-skeleton active />
            </a-col>
            <a-col v-else class="marka_col" :xs="12" :sm="8" :md="6" :lg="4" v-for="marka in data" :key="marka.id">
                <div class="marka_box">
                    <img :src="marka.photo" :alt="marka.marka">
                    <p>{{ capitalize(marka.marka) }}</p>
                </div>
            </a-col>
        </a-row>
    </div>
</template>

<script setup>
import useFetch from '@/Hooks/useFetch';
import { onMounted } from 'vue';
const { data, loading, error, getData } = useFetch()

//////////////////////  methods ////////////////////////
const capitalize = (text) => {
    return text[0].toUpperCase() + text.slice(1, text.length)
}

onMounted(() => {
    // getData("https://api.youcarrf.ru/marks")
    getData("/cars/marka/all/")
})
</script>

<style scoped>
/* ===============================  MARKAS CSS ============================================== */
.markas_section {
    margin-top: 100px;
}

.error {
    display: flex;
    align-items: center;
    justify-content: center;
}

.marka_col {
    width: 216px;
}

.marka_col:hover {
    cursor: pointer;
    box-shadow: 0 21px 21px rgba(176, 176, 176, 0.09);

    img {
        transition: all 0.3s ease-in-out;
        scale: 1.1;
    }


}

.marka_box {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    height: 168px;
    width: 100%;
    border: 1px #F1F1F1 solid;

    p {
        margin: 0;
        font-size: 16px;
        font-weight: 500;
        color: rgba(41, 56, 67, 1);
    }
}

@media(max-width:992px) {
    .marka_box {
        font-size: 12px;
    }

    .markas_section {
        margin-top: 75px;
    }
}

@media(max-width : 768px) {

    .marka_col {
        width: 167px;
    }

    .marka_box {
        height: 130px;
    }
}
</style>