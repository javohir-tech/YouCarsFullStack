<template>
  <div class="container">
    <a-breadcrumb class="bread_crumb" separator=">">
      <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
      <a-breadcrumb-item>О нас</a-breadcrumb-item>
    </a-breadcrumb>
    <!-- Hero -->
    <section class="about-hero">
      <div class="about-hero__text">
        <span class="about-badge">О нас</span>
        <div class="header">
          <h1>Новый формат <span class="about-accent">автомобильной торговли</span></h1>
        </div>
        <p class="about-hero__desc">
          YouCar — надёжный автомобильный рынок в Узбекистане. Здесь обычные пользователи
          размещают объявления о продаже своих автомобилей, а покупатели с помощью удобных
          фильтров находят подходящий вариант.
        </p>
      </div>
      <div class="about-stats">
        <div class="about-stat" v-for="item in stats" :key="item.label">
          <span class="about-stat__value">{{ item.value }}</span>
          <span class="about-stat__label">{{ item.label }}</span>
        </div>
      </div>
    </section>

    <div class="about-divider"></div>

    <!-- How it works -->
    <section class="about-section">
      <h2 class="section_header">Как это работает?</h2>
      <div class="about-steps">
        <div class="about-step" v-for="(step, i) in steps" :key="i">
          <div class="about-step__num">{{ i + 1 }}</div>
          <div class="about-step__body">
            <p class="about-step__title">{{ step.title }}</p>
            <p class="about-step__desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <div class="about-divider"></div>

    <!-- Why us -->
    <section class="about-section">
      <h2 class="section_header">Почему YouCar?</h2>
      <div class="about-features">
        <div class="about-feature" v-for="item in features" :key="item.title">
          <div class="about-feature__icon">
            <i :class="item.icon"></i>
          </div>
          <p class="about-feature__title">{{ item.title }}</p>
          <p class="about-feature__desc">{{ item.desc }}</p>
        </div>
      </div>
    </section>

    <div class="about-divider"></div>

    <!-- Contact -->
    <section class="about-section">
      <h2 class="section_header">Связаться с нами</h2>
      <div class="about-contact__grid">
        <a href="tel:+77123290" class="about-contact__item">
          <i class="fa-solid fa-phone"></i>
          <span>+77 123 29 04</span>
        </a>
        <a href="mailto:suvonovjavohir625@gmail.com" class="about-contact__item">
          <i class="fa-solid fa-envelope"></i>
          <span>suvonovjavohir625@gmail.com</span>
        </a>
        <div class="about-contact__item">
          <i class="fa-solid fa-location-dot"></i>
          <span>Узбекистан</span>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
const stats = [
  { value: '5 000+', label: 'Объявлений' },
  { value: '12 000+', label: 'Пользователей' },
  { value: '3', label: 'Года опыта' },
]

const steps = [
  {
    title: 'Зарегистрируйтесь',
    desc: 'Создайте аккаунт за несколько минут и войдите на платформу.',
  },
  {
    title: 'Разместите объявление',
    desc: 'Загрузите информацию и фотографии автомобиля, укажите цену.',
  },
  {
    title: 'Найдите покупателя',
    desc: 'Заинтересованные пользователи свяжутся с вами напрямую и договорятся о сделке.',
  },
]

const features = [
  {
    icon: 'fa-solid fa-shield-halved',
    title: 'Безопасно',
    desc: 'Объявления размещают только зарегистрированные пользователи.',
  },
  {
    icon: 'fa-solid fa-bolt',
    title: 'Быстро',
    desc: 'Ваше объявление появится на сайте в течение нескольких минут.',
  },
  {
    icon: 'fa-solid fa-magnifying-glass',
    title: 'Удобный поиск',
    desc: 'Фильтры по марке, цене, году выпуска и другим параметрам.',
  },
  {
    icon: 'fa-solid fa-comments',
    title: 'Прямое общение',
    desc: 'Продавец и покупатель общаются без посредников.',
  },
]
</script>

<style scoped>
.about-hero {
  padding: 30px 0 40px;
  display: flex;
  flex-direction: column;
  gap: 36px;
}

.about-badge {
  display: inline-block;
  background: #e8f0fe;
  color: #0057ff;
  font-size: 13px;
  font-weight: 500;
  padding: 4px 14px;
  border-radius: 20px;
  margin-bottom: 14px;
}

.about-accent {
  color: #0057ff;
}

.about-hero__desc {
  font-size: 15px;
  color: #555;
  max-width: 620px;
  line-height: 1.75;
  margin: 12px 0 0;
}

.about-stats {
  display: flex;
  gap: 48px;
  flex-wrap: wrap;
}

.about-stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.about-stat__value {
  font-size: 30px;
  font-weight: 700;
  color: #0057ff;
}

.about-stat__label {
  font-size: 13px;
  color: #888;
}

.about-divider {
  width: 100%;
  height: 1px;
  background: #e8eaf0;
}

.about-section {
  padding: 48px 0;
}

/* Steps */
.about-steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-top: 28px;
}

.about-step {
  display: flex;
  align-items: flex-start;
  gap: 18px;
}

.about-step__num {
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 50%;
  background: #0057ff;
  color: #fff;
  font-weight: 700;
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.about-step__title {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 4px;
  color: #0f0f1a;
}

.about-step__desc {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.65;
}

/* Features */
.about-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 28px;
}

.about-feature {
  border: 1px solid #e8eaf0;
  border-radius: 12px;
  padding: 24px 20px;
  transition: box-shadow 0.2s;
}

.about-feature:hover {
  box-shadow: 0 4px 16px rgba(0, 87, 255, 0.08);
}

.about-feature__icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #e8f0fe;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
  color: #0057ff;
  font-size: 17px;
}

.about-feature__title {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 6px;
  color: #0f0f1a;
}

.about-feature__desc {
  font-size: 13px;
  color: #777;
  margin: 0;
  line-height: 1.6;
}

/* Contact */
.about-contact__grid {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 28px;
}

.about-contact__item {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f5f7ff;
  border: 1px solid #dde4ff;
  border-radius: 10px;
  padding: 11px 20px;
  font-size: 14px;
  color: #0f0f1a;
  text-decoration: none;
  transition: background 0.2s;
}

.about-contact__item:hover {
  background: #e4eaff;
}

.about-contact__item i {
  color: #0057ff;
  font-size: 15px;
  width: 16px;
  text-align: center;
}

/* Responsive */
@media (max-width: 640px) {
  .about-hero {
    padding: 36px 0 28px;
  }

  .about-stats {
    gap: 28px;
  }

  .about-stat__value {
    font-size: 24px;
  }

  .about-features {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 400px) {
  .about-features {
    grid-template-columns: 1fr;
  }
}
</style>