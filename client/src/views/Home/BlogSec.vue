<template>
    <section class="blog_section">
        <header>
            <div class="header">
                <h1>
                    Новости
                </h1>
            </div>
        </header>

        <div class="section_blogs">
            <a-row :gutter="[16, 24]" align="strech">
                <a-col v-if="loading" v-for="_ in new Array(3).fill(1)" class="gutter-row" :xs="24" :sm="12" :md="8">
                    <a-skeleton active />
                </a-col>
                <a-col v-if="!loading && !error" v-for="blog in blogs" :key="blog.id" class="gutter-row" :xs="24"
                    :sm="12" :md="8">
                    <BlogCard :id="blog.id" :image="blog.image" :title="blog.title" :text="blog.text" />
                </a-col>
            </a-row>
            <div v-if="!loading && blogs.length === 0" class="empty">
                <a-empty />
            </div>
        </div>
    </section>
</template>

<script setup>
import { BlogCard } from '@/components';
import api from '@/utils/axios';

import { onMounted, ref } from 'vue';

const blogs = ref([])
const loading = ref(false)
const error = ref(null)

const props = defineProps({
    page_size: Number
})

const handleGetBlogs = async () => {
    loading.value = true
    try {
        const { data } = await api.get("/blog/blog/all/", {
            params: {
                page_size: props.page_size
            }
        })

        blogs.value = data.result
    } catch (err) {
        console.log(err.response || err)
        error.value(err.response || err)
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    handleGetBlogs()
})

</script>

<style scoped>
.blog_section {
    margin-top: 30px;
}
</style>