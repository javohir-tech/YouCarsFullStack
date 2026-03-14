<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item><router-link to="/kontak">Контакты</router-link></a-breadcrumb-item>
        </a-breadcrumb>

        <a-row :gutter="[16, 24]">
            <a-col :xs="24" :sm="24" :md="10">
                <div class="header">
                    <h1>Контакты</h1>
                </div>
                <div class="kontaks">
                    <a target="_blank" href="tel:+998771232904" class="kontak_item">
                        <div class="icon_section">
                            <i class="fa-solid fa-phone icon"></i>
                        </div>
                        <p>+998 77 123 29 04</p>
                    </a>
                    <a target="_blank" href="https://t.me/Suvonov_Javoh1r" class="kontak_item">
                        <div class="icon_section">
                            <i class="fa-brands fa-telegram icon"></i>
                        </div>
                        <p>@Suvonov_Javoh1r</p>
                    </a>
                    <a target="_blank" href="https://maps.google.com/?q=Tashkent" class="kontak_item">
                        <div class="icon_section">
                            <i class="fa-solid fa-location-dot icon"></i>
                        </div>
                        <p>Ташкент</p>
                    </a>
                </div>
                <div class="under_icons">
                    <a target="_blank" href="https://www.instagram.com/suvonov_javohir1/">
                        <instagram-outlined class="under_icon" />
                    </a>
                    <a target="_blank" href="https://github.com/javohir-tech/YouCarsFullStack">
                        <github-outlined class="under_icon" />
                    </a>
                    <a target="_blank" href="http://www.linkedin.com/in/javohir-suvonov-a98925303">
                        <linkedin-outlined class="under_icon" />
                    </a>
                </div>
            </a-col>
            <a-col :xs="24" :sm="24" :md="14">
                <iframe
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3561.696672427011!2d69.20557647078006!3d41.35196326274695!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38ae8c3da3c6e5c3%3A0x9882f2a6b7329d1d!2z0KLQsNGI0LrQtdC90YLRgdC60LjQuSDQs9C-0YHRg9C00LDRgNGB0YLQstC10L3QvdGL0Lkg0YLQtdGF0L3QuNGH0LXRgdC60LjQuSDRg9C90LjQstC10YDRgdC40YLQtdGC!5e0!3m2!1sru!2s!4v1773426478160!5m2!1sru!2s"
                    width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade"></iframe>
            </a-col>
        </a-row>
    </div>
</template>

<script setup>
import { GithubOutlined, InstagramOutlined, LinkedinOutlined } from '@ant-design/icons-vue';

</script>

<style scoped>
.kontaks {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin: 20px 0;
}

.kontak_item {
    display: flex;
    align-items: center;
    gap: 10px;

    p {
        margin: 0;
        color: #5A5A5A;
        font-weight: 500;
        font-size: 17px;
    }
}

.icon_section {
    padding: 10px;
    background-color: #F3F3F3;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
}

.icon {
    font-size: 24px;
    color: #050B20;
}

.under_icons {
    margin-top: 20px;
    display: flex;
    gap: 10px;
}

.under_icon {
    font-size: 24px;
}
</style>