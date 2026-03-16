<template>
    <div class="container">
        <footer class="footer">
            <a-row :gutter="[16, 24]">
                <a-col class="gutter-row" :xs="24" :md="5">
                    <div>
                        <div class="brand">
                            <span class="you">You</span>
                            <span class="car">Car</span>
                        </div>
                        <div class="icons">
                            <a target="_blank" href="https://www.instagram.com/suvonov_javohir1/">
                                <InstagramOutlined class="icon_social" />
                            </a>
                            <a target="_blank" href="http://www.linkedin.com/in/javohir-suvonov-a98925303">
                                <LinkedinOutlined class="icon_social" />
                            </a>
                            <a target="_blank" href="https://github.com/javohir-tech/YouCarsFullStack">
                                <GithubOutlined class="icon_social" />
                            </a>
                        </div>
                        <div class="footer_info">
                            {{ t('footer.slogan') }}
                            <br>
                            {{ t('footer.tagline') }}
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="12" :md="5">
                    <div class="footer_section">
                        <h2 class="header">{{ t('footer.company') }}</h2>
                        <div class="links">
                            <router-link to="/katalog">{{ t('footer.catalog') }}</router-link>
                            <router-link to="/">{{ t('nav.about') }}</router-link>
                            <router-link to="/">{{ t('nav.news') }}</router-link>
                            <router-link to="/">{{ t('nav.contact') }}</router-link>
                            <router-link to="/">{{ t('footer.favorites') }}</router-link>
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="12" :md="5">
                    <div class="footer_section">
                        <h2 class="header">{{ t('footer.favorites') }}</h2>
                        <div class="links">
                            <router-link to="/katalog">{{ t('footer.fromEurope') }}</router-link>
                            <router-link to="/">{{ t('footer.fromUSA') }}</router-link>
                            <router-link to="/">{{ t('footer.fromUAE') }}</router-link>
                            <router-link to="/">{{ t('footer.fromChina') }}</router-link>
                            <router-link to="/">{{ t('footer.fromKorea') }}</router-link>
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="24" :md="9">
                    <div class="footer_section">
                        <h2 class="header">{{ t('footer.brands') }}</h2>
                        <div class="markas">
                            <div class="links">
                                <router-link to="/katalog">Audi</router-link>
                                <router-link to="/">Audi</router-link>
                                <router-link to="/">Acura</router-link>
                                <router-link to="/">Alfa Romeo</router-link>
                                <router-link to="/">Avatr</router-link>
                            </div>
                            <div class="links">
                                <router-link to="/katalog">BMW</router-link>
                                <router-link to="/">Baic</router-link>
                                <router-link to="/">Byd</router-link>
                                <router-link to="/">Bently</router-link>
                                <router-link to="/">Chery</router-link>
                            </div>
                            <div class="links">
                                <router-link to="/katalog">Chery</router-link>
                                <router-link to="/">Cadillac</router-link>
                                <router-link to="/">Changan</router-link>
                                <router-link to="/">Chevrolet</router-link>
                                <router-link to="/">Citroen</router-link>
                            </div>
                            <div class="links">
                                <router-link to="/katalog">daewoo</router-link>
                                <router-link to="/">Datsun</router-link>
                                <router-link to="/">Dodge</router-link>
                                <router-link to="/">EXEED</router-link>
                                <router-link to="/">Ferrari</router-link>
                            </div>
                            <div class="links">
                                <router-link to="/katalog">Fiat</router-link>
                                <router-link to="/">Ford</router-link>
                                <router-link to="/">GAC</router-link>
                                <router-link to="/">Geely</router-link>
                                <router-link to="/">Genesis</router-link>
                            </div>
                        </div>
                    </div>
                </a-col>
            </a-row>
            <div class="footer_under">
                <p class="secret_div"></p>
                <p>{{ t('footer.privacy') }}</p>
                <p>{{ t('footer.madeBy') }}</p>
            </div>
        </footer>
    </div>
</template>

<script setup>
import { GithubOutlined, InstagramOutlined, LinkedinOutlined } from '@ant-design/icons-vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

</script>

<style scoped>
.footer {
    padding-top: 40px;
    border-top: 1px solid rgba(218, 218, 218, 1);
    margin-top: 100px;
}

.brand {
    span {
        font-weight: 700;
        font-size: 30px;
    }

    .you {
        color: rgba(38, 132, 229, 1);
    }

    .car {
        color: rgba(41, 56, 67, 1);
    }
}

.icons {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
}

.icon_social {
    font-size: 21px;
    color: rgba(152, 152, 152, 1);
}

.footer_info {
    color: rgba(41, 56, 67, 1);
    font-size: 13px;
    font-weight: 500;
}

.header {
    font-weight: 700;
    font-size: 17px;
    color: rgba(41, 56, 67, 1);
}

.links {
    display: flex;
    flex-direction: column;
    gap: 10px;

    a {
        font-size: 15px;
        font-weight: 500;
        color: rgba(90, 90, 90, 1);
    }
}

.markas {
    display: flex;
    justify-content: space-between;
}

.footer_under {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 30px 0 15px 0;

    p {
        font-weight: 500;
        font-size: 13px;
        color: rgba(90, 90, 90, 1);
        margin: 0;
    }
}

@media(max-width: 768px) {
    .secret_div {
        display: none;
    }

    .markas {
        flex-wrap: wrap;
        justify-content: first baseline;
    }

    .footer {
        margin-top: 0px;
    }
}
</style>