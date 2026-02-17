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
                <a-col class="gutter-row" :xs="{ order: 1, span: 24 }" :md="{ order: 1, span: 12 }"
                    :lg="{ order: 1, span: 16 }">
                    <div class="blog_image">
                        <a-skeleton-image class="skeleton_image" v-if="load" />
                        <img v-show="!load" :src="blog.image" @load="onLoad" @error="onError" :alt="blog.title">
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="{ order: 3, span: 24 }" :md="{ order: 2, span: 12 }"
                    :lg="{ order: 2, span: 8 }">
                    <div class="similer_blogs">
                        <h1>Читайте другие статьи в нашем блоге:</h1>
                        <div v-if="similarLoading">
                            <a-skeleton />
                            <a-skeleton />
                        </div>
                        <div v-else v-for="similar in similarBlogs"
                            @click="navigate(similar.id)" class="similar_blog_boxs" :to="`/blog/detail/${similar.id}`">
                            <p>{{ similar.title }}</p>
                            <right-outlined class="similar_icon" />
                        </div>
                        <div class="link_to_blog">
                            <router-link to="/blogs">Читать больше новостей <arrow-right-outlined
                                    class="blogs_link" /></router-link>
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row blog_text" :xs="{ order: 2, span: 24 }" :md="{ order: 3, span: 24 }"
                    :lg="{ order: 3, span: 16 }">
                    <a-skeleton active v-if="loading" />
                    <p v-else>{{ blog.text }}</p>
                </a-col>
            </a-row>
        </div>

        <call-card />
    </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router';
import api from '@/utils/axios';
import { onMounted, ref, watch } from 'vue';
import { CallCard } from '@/components';
import { ArrowRightOutlined, RightOutlined } from '@ant-design/icons-vue';

const route = useRoute()
const router = useRouter()

const load = ref(true)

const blog = ref([])
const loading = ref(false)
const err = ref(null)

const similarBlogs = ref([])
const similarLoading = ref(false)
const similarErr = ref(null)


const handleBlogGet = async (id) => {
    loading.value = true
    try {
        const { data } = await api.get(`/blog/blog/detail/${id}`)
        blog.value = data
    } catch (error) {
        console.log(error.response || error)
        err.value = error.response ?? error
    } finally {
        loading.value = false
    }
}

const handleGetSimilerBlogs = async (id) => {
    similarLoading.value = true
    try {
        const { data } = await api.get(`/blog/blog/semiler/${id}/`)
        console.log(data.result)
        similarBlogs.value = data.result
        console.log(similarBlogs.value)
        // console.log(data.result)
    } catch (error) {
        similarErr.value = error.reponse ?? error
        console.log(error.reponse || error)
    } finally {
        similarLoading.value = false
    }
}

const navigate = (id) => {
    router.push(`/blog/detail/${id}`)
    load.value = true
    handleBlogGet(id)
    handleGetSimilerBlogs(id)
}

const onLoad = () => {
    load.value = false
}

const onError = () => {
    load.value = false
}

onMounted(() => {
    handleBlogGet(route.params.id)
    handleGetSimilerBlogs(route.params.id)
})
</script>

<style scoped>
.header {
    width: 50%;
}

.blog_text {
    margin-top: 20px;

    p {
        font-size: 16px;
        font-weight: 500;
        color: rgba(152, 152, 152, 1);
    }
}

.similar_blog_boxs {
    padding: 20px 0;
    border-bottom: 1px solid rgba(221, 221, 221, 1);
    display: flex;
    align-items: center;
    justify-content: space-between;

    p {
        margin: 0;
        font-weight: 500;
        font-size: 15px;
        color: rgba(90, 90, 90, 1);
    }
}

.blog_image {
    border-radius: 10px;
    height: 100%;
}

.skeleton_image {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.blog_image img {
    width: 100%;
    border-radius: 10px;
    height: 350px;
    object-fit: cover;
    object-position: center;
}

.similar_icon {
    font-size: 15px;
    color: rgba(90, 90, 90, 1);
}

.similer_blogs {
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    height: 100%;
    display: flex;
    flex-direction: column;

    h1 {
        font-size: 20px;
        font-weight: 500;
    }
}

.blogs_link {
    margin-left: 10px;
    transform: rotate(-45deg);
}

.link_to_blog {
    margin-top: auto;

    a {
        color: rgba(32, 32, 32, 1);
    }
}

@media(max-width : 768px) {
    .header {
        width: 100%;
    }

    .link_to_blog{
        margin-top: 30px;
    }
}
</style>