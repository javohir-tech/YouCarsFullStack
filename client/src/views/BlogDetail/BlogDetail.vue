<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item><router-link to="/">Новости</router-link></a-breadcrumb-item>
            <a-breadcrumb-item>{{ blog.title }}</a-breadcrumb-item>
        </a-breadcrumb>

        <div class="header">
            <h1>{{ blog.title }}</h1>
        </div>
        <div class="blog_box">
            <a-row :gutter="[16, 23]" align="strech">
                <a-col class="gutter-row" :xs="24" :md="12" :lg="16">
                    <div class="blog_image">
                        <img :src="blog.image" :alt="blog.title">
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="24" :md="12" :lg="8">
                    <div class="similer_blogs">
                        <h1>Читайте другие статьи в нашем блоге:</h1>
                        <div v-for="similar in similarBlogs" class="similar_blog_boxs">
                            <p>{{ similar.title}}</p>
                        </div>
                    </div>
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import api from '@/utils/axios';
import { onMounted, ref } from 'vue';

const route = useRoute()

const blog = ref([])
const loading = ref(false)
const err = ref(null)

const similarBlogs = ref([])
const similarLoading = ref(false)
const similarErr= ref(null)

const handleBlogGet = async () => {
    loading.value = true
    try {
        const { data } = await api.get(`/blog/blog/detail/${route.params.id}`)
        blog.value = data
    } catch (error) {
        console.log(error.response || error)
        err.value = error.response ?? error
    } finally {
        loading.value = false
    }
}

const handleGetSimilerBlogs = async () => {
    similarLoading.value = true
    try {
        const {data} = await api.get(`/blog/blog/semiler/${route.params.id}/`)
        console.log(data.result)
        similarBlogs.value = data.result
        console.log(similarBlogs.value)
        // console.log(data.result)
    } catch (error) {
        similarErr.value = error.reponse ?? error
        console.log(error.reponse || error)
    }finally{
        similarLoading.value = false
    }
}

onMounted(() => {
    handleBlogGet()
    handleGetSimilerBlogs()
})
</script>

<style scoped>
.header {
    width: 50%;
}

.similar_blog_boxs{
    padding-bottom: 10px;
    border-bottom: 1px solid red;
}

.blog_image {
    border-radius: 10px;
    height: 100%;
}

.blog_image img {
    width: 100%;
    border-radius: 10px;
    height: 350px;
    object-fit: cover;
    object-position: center;
}

.similer_blogs {
    padding: 15px 10px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    height: 100%;

    h1 {
        font-size: 20px;
        font-weight: 500;
    }
}

@media(max-width : 768px) {
    .header {
        width: 100%;
    }
}
</style>