<template>


  <div class="add-car-page">
    <div class="error" v-if="errors">
      <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist." />
    </div>
    <a-spin :spinning="isLoading" tip="Loading..." size="large">

      <div v-if="!errors" class="container">
        <div class="page-header">
          <h1>{{ route.params.id ? "Редактировать объявление" : "Разместите объявление" }}</h1>
          <p>{{
            route.params.id ?
              "Укажите данные об автомобиле для редактирования объявления"
              :
              "Укажите данные об автомобиле для размещения объявления"
          }}
          </p>
        </div>

        <!-- Step 1: Vehicle Type Selection -->
        <div class="type-tabs">
          <a-radio-group v-model:value="selectedType" button-style="solid" size="large">
            <a-radio-button value="automobile">Автомобили</a-radio-button>
            <a-radio-button value="commercial">Коммерческий транспорт</a-radio-button>
            <a-radio-button value="motorcycle">Мотоциклы</a-radio-button>
          </a-radio-group>
        </div>

        <!-- Step 2: Brand Selection -->
        <div class="form-section">
          <a-select v-model:value="formData.marka" placeholder="Марка" size="large" show-search :loading="loadingBrands"
            :disabled="!selectedType" @change="handleMarkaChange" :filter-option="filterOption"
            :status="validationErrors.marka ? 'error' : ''">
            <a-select-option v-for="brand in brands" :key="brand.id" :value="brand.marka" :label="brand.marka">
              {{ brand.marka }}
            </a-select-option>
          </a-select>
          <div v-if="validationErrors.marka" class="error-message">{{ validationErrors.marka }}</div>
        </div>

        <!-- Step 3: Model Selection -->
        <div class="form-section" v-if="formData.marka">
          <a-select v-model:value="formData.car_model" placeholder="Модель" size="large" show-search
            :loading="loadingModels" @change="handleModelChange" :filter-option="filterOption"
            :status="validationErrors.car_model ? 'error' : ''">
            <a-select-option v-for="model in models" :key="model.id" :value="model.name" :label="model.name">
              {{ model.name }}
            </a-select-option>
          </a-select>
          <div v-if="validationErrors.car_model" class="error-message">{{ validationErrors.car_model }}</div>
        </div>

        <!-- Main Form (Shows after model is selected) -->
        <div v-if="formData.car_model" class="main-form">

          <!-- Characteristics Section -->
          <div class="characteristics-section">
            <h2>Характеристики</h2>

            <a-form layout="vertical" :model="formData">
              <a-row :gutter="16">
                <!-- Year -->
                <a-col :span="12">
                  <a-form-item label="Год выпуска" :validate-status="validationErrors.year ? 'error' : ''"
                    :help="validationErrors.year">
                    <a-input-number v-model:value="formData.year" placeholder="2024" style="width: 100%" size="large"
                      @blur="validateField('year')" />
                  </a-form-item>
                </a-col>

                <!-- Mileage -->
                <a-col :span="12">
                  <a-form-item label="Пробег" :validate-status="validationErrors.milage ? 'error' : ''"
                    :help="validationErrors.milage">
                    <a-input-number v-model:value="formData.milage" placeholder="16 000" style="width: 100%"
                      size="large" @blur="validateField('milage')">
                      <template #addonAfter>км</template>
                    </a-input-number>
                  </a-form-item>
                </a-col>

                <!-- Country -->
                <a-col :span="12">
                  <a-form-item label="Страна" :validate-status="validationErrors.country ? 'error' : ''"
                    :help="validationErrors.country">
                    <a-select v-model:value="formData.country" placeholder="США" size="large" show-search
                      :loading="loadingCountries" :filter-option="filterOption" @change="validateField('country')">
                      <!-- <a-select-option v-for="country in countries" :key="country.id" :value="country.country">
                      {{ country.country }}
                    </a-select-option> -->
                      <a-select-option v-for="country in countries" :key="country.id" :value="country.country"
                        :label="country.country"></a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Fuel -->
                <a-col :span="12">
                  <a-form-item label="Топливо" :validate-status="validationErrors.fuel ? 'error' : ''"
                    :help="validationErrors.fuel">
                    <a-select v-model:value="formData.fuel" placeholder="Бензин" size="large" :loading="loadingFuels"
                      @change="validateField('fuel')">
                      <a-select-option v-for="fuel in fuels" :key="fuel.id" :value="fuel.name">
                        {{ fuel.name }}
                      </a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Displacement -->
                <a-col :span="12">
                  <a-form-item label="Объем" :validate-status="validationErrors.displacement ? 'error' : ''"
                    :help="validationErrors.displacement">
                    <a-input-number v-model:value="formData.displacement" :step="0.1" placeholder="1.8"
                      style="width: 100%" size="large" @blur="validateField('displacement')">
                      <template #addonAfter>л</template>
                    </a-input-number>
                  </a-form-item>
                </a-col>

                <!-- Power -->
                <a-col :span="12">
                  <a-form-item label="Мощность" :validate-status="validationErrors.power ? 'error' : ''"
                    :help="validationErrors.power">
                    <a-input-number v-model:value="formData.power" placeholder="153" style="width: 100%" size="large"
                      @blur="validateField('power')">
                      <template #addonAfter>л.с</template>
                    </a-input-number>
                  </a-form-item>
                </a-col>

                <!-- Drive Type -->
                <a-col :span="12">
                  <a-form-item label="Привод" :validate-status="validationErrors.drive_type ? 'error' : ''"
                    :help="validationErrors.drive_type">
                    <a-select v-model:value="formData.drive_type" placeholder="Передний" size="large"
                      @change="validateField('drive_type')">
                      <a-select-option value="FWD">Передний</a-select-option>
                      <a-select-option value="RWD">Задний</a-select-option>
                      <a-select-option value="AWD">Полный</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Transmission -->
                <a-col :span="12">
                  <a-form-item label="КПП" :validate-status="validationErrors.transmission_type ? 'error' : ''"
                    :help="validationErrors.transmission_type">
                    <a-select v-model:value="formData.transmission_type" placeholder="Автомат" size="large"
                      @change="validateField('transmission_type')">
                      <a-select-option value="MT">Механика</a-select-option>
                      <a-select-option value="AT">Автомат</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Doors Count -->
                <a-col :span="12">
                  <a-form-item label="Количество дверей" :validate-status="validationErrors.doors_count ? 'error' : ''"
                    :help="validationErrors.doors_count">
                    <a-select v-model:value="formData.doors_count" placeholder="5" size="large"
                      @change="validateField('doors_count')">
                      <a-select-option :value="2">2</a-select-option>
                      <a-select-option :value="3">3</a-select-option>
                      <a-select-option :value="4">4</a-select-option>
                      <a-select-option :value="5">5</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Body Type -->
                <a-col :span="12">
                  <a-form-item label="Кузов" :validate-status="validationErrors.body ? 'error' : ''"
                    :help="validationErrors.body">
                    <a-select v-model:value="formData.body" placeholder="Седан" size="large"
                      @change="validateField('body')">
                      <a-select-option value="sedan">Седан</a-select-option>
                      <a-select-option value="hatchback">Хэтчбек</a-select-option>
                      <a-select-option value="suv">Внедорожник</a-select-option>
                      <a-select-option value="crossover">Кроссовер</a-select-option>
                      <a-select-option value="coupe">Купе</a-select-option>
                      <a-select-option value="convertible">Кабриолет</a-select-option>
                      <a-select-option value="wagon">Универсал</a-select-option>
                      <a-select-option value="pickup">Пикап</a-select-option>
                      <a-select-option value="minivan">Минивэн</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Condition -->
                <a-col :span="12">
                  <a-form-item label="Состояние" :validate-status="validationErrors.condition ? 'error' : ''"
                    :help="validationErrors.condition">
                    <a-select v-model:value="formData.condition" placeholder="С пробегом" size="large"
                      @change="validateField('condition')">
                      <a-select-option value="new">Новый</a-select-option>
                      <a-select-option value="excellent">Отличное</a-select-option>
                      <a-select-option value="good">Хорошее</a-select-option>
                      <a-select-option value="fair">Среднее</a-select-option>
                      <a-select-option value="poor">Плохое</a-select-option>
                      <a-select-option value="damaged">Битый</a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>

                <!-- Color -->
                <a-col :span="12">
                  <a-form-item label="Цвет" :validate-status="validationErrors.color ? 'error' : ''"
                    :help="validationErrors.color">
                    <a-select v-model:value="formData.color" placeholder="Белый" size="large" :loading="loadingColors"
                      @change="validateField('color')">
                      <a-select-option v-for="color in colors" :key="color.id" :value="color.color">
                        <div style="display: flex; align-items: center; gap: 8px;">
                          <span :style="{
                            display: 'inline-block',
                            width: '16px',
                            height: '16px',
                            borderRadius: '50%',
                            backgroundColor: color.code || '#000',
                            border: '1px solid #d9d9d9'
                          }"></span>
                          {{ color.color }}
                        </div>
                      </a-select-option>
                    </a-select>
                  </a-form-item>
                </a-col>
              </a-row>

              <!-- Availability Radio -->
              <a-form-item>
                <a-radio-group v-model:value="formData.availability">
                  <a-radio value="in_stock">В наличии</a-radio>
                  <a-radio value="on_order">Под заказ</a-radio>
                </a-radio-group>
              </a-form-item>
            </a-form>
          </div>

          <!-- Photos Section -->
          <div class="photos-section">
            <h2>Фото</h2>
            <p class="section-subtitle">Загрузите фото вашего автомобиля четко с разных ракурсов</p>

            <div class="upload-container">
              <div class="uploaded-images">
                <div v-for="(image, index) in uploadedImages" :key="index" class="image-item">
                  <a-spin class="image_loading" v-if="imageLoading" />
                  <img :src="image.url" v-show="!imageLoading" @load="onLoad" @error="onError"
                    :alt="`Car photo ${index + 1}`" />
                  <div class="image-overlay">
                    <a-button type="text" danger @click="removeImage(index, image.id)" :icon="h(DeleteOutlined)" />
                  </div>
                  <a-progress v-if="image.uploading" :percent="image.progress" :show-info="false"
                    style="position: absolute; bottom: 0; left: 0; right: 0;" />
                </div>

                <!-- Upload Button -->
                <div v-if="uploadedImages.length < 6" class="upload-button" @click="triggerFileInput">
                  <CameraOutlined style="font-size: 32px; color: #1890ff;" />
                  <p>Выберите или перетащите фото</p>
                </div>
              </div>
              <div v-if="validationErrors.images" class="error-message">{{ validationErrors.images }}</div>
              <input ref="fileInput" type="file" accept="image/*" multiple style="display: none;"
                @change="handleFileSelect" />
            </div>
          </div>

          <!-- Description Section -->
          <div class="description-section">
            <h2>Описание</h2>
            <p class="section-subtitle">Не указывайте ссылки на источники, цены, контакты и не предлагайте другие
              услуги!
              Объявление не пройдет модерацию</p>

            <a-form-item :validate-status="validationErrors.description ? 'error' : ''"
              :help="validationErrors.description">
              <a-textarea v-model:value="formData.description" placeholder="Четко опишите вашу авто" :rows="6"
                :maxlength="1200" show-count @blur="validateField('description')" />
            </a-form-item>
          </div>

          <!-- Price Section -->
          <div class="price-section">
            <h2>Цена</h2>
            <a-form-item :validate-status="validationErrors.price ? 'error' : ''" :help="validationErrors.price">
              <a-input-number v-model:value="formData.price" placeholder="1 850 000" size="large" style="width: 100%"
                @blur="validateField('price')">
                <template #addonAfter>
                  <a-select v-model:value="currency" style="width: 60px">
                    <a-select-option value="USD">$</a-select-option>
                    <a-select-option value="UZS">сўм</a-select-option>
                  </a-select>
                </template>
              </a-input-number>
            </a-form-item>
          </div>

          <!-- Submit Button -->
          <div class="submit-section">
            <a-button type="primary" size="large" block :loading="submitting" @click="handleSubmit">
              {{ route.params.id ? 'Сохранить изменения'
                : 'Опубликовать объявление' }}
            </a-button>
          </div>
        </div>
      </div>

    </a-spin>
  </div>
</template>

<script setup>
import { ref, reactive, computed, h, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { CameraOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import { watch } from 'vue';
import api from '@/utils/axios';
import { useRoute, useRouter } from 'vue-router';

// State
const selectedType = ref('automobile');
const formData = reactive({
  avto_type: null,
  marka: null,
  car_model: null,
  country: null,
  color: null,
  fuel: null,
  price: null,
  year: null,
  milage: null,
  displacement: null,
  power: null,
  drive_type: null,
  transmission_type: null,
  doors_count: null,
  description: '',
  body: null,
  condition: null,
  availability: 'in_stock',
  status: 'PD'
});

// Validation errors
const validationErrors = reactive({
  marka: '',
  car_model: '',
  year: '',
  milage: '',
  country: '',
  fuel: '',
  displacement: '',
  power: '',
  drive_type: '',
  transmission_type: '',
  doors_count: '',
  body: '',
  condition: '',
  color: '',
  description: '',
  price: '',
  images: ''
});

const currency = ref('USD');
const currentYear = new Date().getFullYear();
const route = useRoute()
const router = useRouter()
// Loading states
const isLoading = ref(false)
const loadingBrands = ref(false);
const loadingModels = ref(false);
const loadingCountries = ref(false);
const loadingColors = ref(false);
const loadingFuels = ref(false);
const submitting = ref(false);
const imageLoading = ref(true)

// errors
const errors = ref(false)

// Data lists
const brands = ref([]);
const models = ref([]);
const countries = ref([]);
const colors = ref([]);
const fuels = ref([]);

// Images
const uploadedImages = ref([]);
const fileInput = ref(null);
const createdCarId = ref(null);

// Validation rules
const validationRules = {
  marka: {
    required: true,
    message: 'Пожалуйста, выберите марку автомобиля'
  },
  car_model: {
    required: true,
    message: 'Пожалуйста, выберите модель автомобиля'
  },
  year: {
    required: true,
    message: 'Пожалуйста, укажите год',
    validate: (value) => {
      if (!value) return 'Год обязателен';
      if (value < 1951) return 'Год не может быть меньше 1951';
      if (value > currentYear) return `Год не может быть больше ${currentYear}`;
      return '';
    }
  },
  milage: {
    required: true,
    message: 'Пожалуйста, укажите пробег',
    validate: (value) => {
      if (value === null || value === undefined) return 'Пробег обязателен';
      if (value < 0) return 'Пробег не может быть отрицательным';
      if (value > 2000000) return 'Пробег не может превышать 2 000 000 км';
      return '';
    }
  },
  country: {
    required: true,
    message: 'Пожалуйста, выберите страну'
  },
  fuel: {
    required: true,
    message: 'Пожалуйста, выберите тип топлива'
  },
  displacement: {
    required: true,
    message: 'Пожалуйста, укажите объем двигателя',
    validate: (value) => {
      if (value === null || value === undefined) return 'Объем двигателя обязателен';
      if (value < 0) return 'Объем не может быть отрицательным';
      if (value > 9.9) return 'Объем не может превышать 9.9 л';
      if (value === 0) return 'Объем должен быть больше 0';
      return '';
    }
  },
  power: {
    required: true,
    message: 'Пожалуйста, укажите мощность',
    validate: (value) => {
      if (value === null || value === undefined) return 'Мощность обязательна';
      if (value < 0) return 'Мощность не может быть отрицательной';
      if (value > 2000) return 'Мощность не может превышать 2000 л.с.';
      if (value === 0) return 'Мощность должна быть больше 0';
      return '';
    }
  },
  drive_type: {
    required: true,
    message: 'Пожалуйста, выберите тип привода'
  },
  transmission_type: {
    required: true,
    message: 'Пожалуйста, выберите тип коробки передач'
  },
  doors_count: {
    required: true,
    message: 'Пожалуйста, выберите количество дверей'
  },
  body: {
    required: true,
    message: 'Пожалуйста, выберите тип кузова'
  },
  condition: {
    required: true,
    message: 'Пожалуйста, выберите состояние автомобиля'
  },
  color: {
    required: true,
    message: 'Пожалуйста, выберите цвет'
  },
  description: {
    required: true,
    message: 'Пожалуйста, добавьте описание',
    validate: (value) => {
      if (!value || value.trim().length === 0) return 'Описание обязательно';
      if (value.trim().length < 10) return 'Описание должно содержать не менее 10 символов';
      if (value.length > 1200) return 'Описание не может превышать 1200 символов';
      // Проверка на запрещенные шаблоны
      const forbiddenPatterns = [
        /https?:\/\//i, // URL-адреса
        /www\./i, // www ссылки
        /\+\d{1,3}[\s-]?\d/i, // Номера телефонов
        /@[a-zA-Z0-9]/i, // Email/социальные сети
        /telegram/i,
        /whatsapp/i,
        /viber/i
      ];

      for (const pattern of forbiddenPatterns) {
        if (pattern.test(value)) {
          return 'Описание не должно содержать ссылки, контакты или упоминания мессенджеров';
        }
      }

      return '';
    }
  },
  price: {
    required: true,
    message: 'Пожалуйста, укажите цену',
    validate: (value) => {
      if (value === null || value === undefined) return 'Цена обязательна';
      if (value <= 0) return 'Цена должна быть больше 0';
      if (value > 999999999) return 'Цена слишком высокая';
      return '';
    }
  },
  images: {
    required: true,
    message: 'Загрузите минимум 1 фото',
    validate: (images) => {
      if (!images || images.length === 0) return 'Загрузите минимум 1 фото';
      if (images.length > 6) return 'Максимум 6 фотографий';
      return '';
    }
  }
};

// Validate single field
const validateField = (fieldName) => {
  const rule = validationRules[fieldName];
  if (!rule) return true;

  let value = formData[fieldName];

  // For images validation
  if (fieldName === 'images') {
    value = uploadedImages.value;
  }

  // Check if required
  if (rule.required && (value === null || value === undefined || value === '')) {
    validationErrors[fieldName] = rule.message;
    return false;
  }

  // Custom validation
  if (rule.validate) {
    const error = rule.validate(value);
    validationErrors[fieldName] = error;
    return !error;
  }

  // Clear error if valid
  validationErrors[fieldName] = '';
  return true;
};

// Validate all fields
const validateForm = () => {
  let isValid = true;

  // Clear all errors first
  Object.keys(validationErrors).forEach(key => {
    validationErrors[key] = '';
  });

  // Validate each field
  Object.keys(validationRules).forEach(fieldName => {
    const fieldValid = validateField(fieldName);
    if (!fieldValid) {
      isValid = false;
    }
  });

  return isValid;
};

// API Functions
const carData = {
  async getBrandsByType(type) {
    try {
      const { data } = await api.post("cars/marka/", {
        avto_type: type
      })
      if (data.success) {
        const markas = data.data.map((item) => {
          return { id: item.id, marka: item.marka }
        })
        return markas
      }
    } catch (error) {
      if (error.response) {
        const errors = error.response.data
        if (errors.type) {
          message.error(errors.type[0])
        } else if (errors.marka) {
          message.error(errors.marka[0])
        } else {
          console.log(error.response)
        }
      } else {
        console.log(error)
      }
    }
  },

  async getModelsByBrand(brand) {
    try {
      const { data } = await api.post("cars/models/", {
        marka: brand
      })

      if (data.success) {
        const models = data.models.map((item) => {
          return { id: item.id, name: item.name }
        })
        return models
      }
    } catch (error) {
      if (error.response) {
        const errors = error.response.data
        if (errors.car_models) {
          message.warning(errors.car_models[0])
        }
      } else {
        console.log(error)
      }
    }
  },

  async getCountries() {
    try {
      const { data } = await api.get("/cars/countries/")
      const countries = data.map((item) => {
        return { id: item.id, country: item.country }
      })
      return countries
    } catch (error) {
      if (error.response) {
        console.log(error.response)
      } else {
        console.log(error)
      }
    }
  },

  async getColors() {
    try {
      const { data } = await api.get("cars/colors/")
      const colors = data.map((item) => {
        return { id: item.id, color: item.color, code: item.color_code }
      })
      return colors
    } catch (error) {
      if (error.response) {
        console.error(error.response)
      } else {
        console.log(error)
      }
    }
  },

  async getFuels() {
    try {
      const { data } = await api.get("cars/fuel/")
      const fuels = data.map((item) => {
        return { id: item.id, name: item.name }
      })
      return fuels
    } catch (error) {
      if (error.response) {
        console.log(error.response)
      } else {
        console.log(error)
      }
    }
  },

  async createCar(data) {
    try {
      const response = await api.post("/cars/car/", { ...data })
      return response.data.data.id
    } catch (error) {
      if (error.response) {
        const errors = error.response.data
        for (let item in errors) {
          if (errors[item]) {
            message.error(errors[item][0])
            break
          }
        }
        console.log(error.response)
      } else {
        console.log(error)
      }
      throw error;
    }
  },

  async changeCar(data) {
    try {
      const response = await api.put(`/cars/car/${route.params.id}/`, { ...data })
      console.log(response)
      return response.data.data.id
    } catch (error) {
      if (error.response) {
        const errors = error.response.data
        for (let item in errors) {
          if (errors[item]) {
            message.error(errors[item][0])
            break
          }
        }
        console.log(error.response)
      } else {
        console.log(error)
      }
      throw error;
    }
  },

  async uploadImage(carId, file, onProgress, isMain = false) {
    const formData = new FormData();
    formData.append('car', carId);
    formData.append('image', file);
    formData.append('is_main', isMain);
    try {
      const response = await api.post('/cars/car/image/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      });
      return response.data;
    } catch (error) {
      if (error.response) {
        console.error('Upload error:', error.response.data);
        throw new Error(error.response.data.message || 'Error uploading image');
      } else {
        console.error('Network error:', error);
        throw new Error('Network error');
      }
    }
  }
};

// Methods

const onLoad = () => {
  imageLoading.value = false
}

const onError = () => {
  imageLoading.value = false
}

const filterOption = (input, option) => {
  const label = option.label || option.children || '';
  return String(label).toLowerCase().includes(input.toLowerCase());
};

const handleMarkaChange = async (brand) => {
  formData.car_model = null;
  models.value = [];
  validateField('marka');

  if (brand) {
    loadingModels.value = true;
    try {
      models.value = await carData.getModelsByBrand(brand);
    } catch (error) {
      message.error('Error loading models');
    } finally {
      loadingModels.value = false;
    }
  }
};

const handleModelChange = async () => {
  validateField('car_model');

  if (!countries.value.length) {
    loadingCountries.value = true;
    try {
      countries.value = await carData.getCountries();
    } catch (error) {
      message.error('Error loading countries');
    } finally {
      loadingCountries.value = false;
    }
  }

  if (!colors.value.length) {
    loadingColors.value = true;
    try {
      colors.value = await carData.getColors();
    } catch (error) {
      message.error('Error loading colors');
    } finally {
      loadingColors.value = false;
    }
  }

  if (!fuels.value.length) {
    loadingFuels.value = true;
    try {
      fuels.value = await carData.getFuels();
    } catch (error) {
      message.error('Error loading fuel types');
    } finally {
      loadingFuels.value = false;
    }
  }
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files);
  const remainingSlots = 6 - uploadedImages.value.length;

  if (files.length > remainingSlots) {
    message.warning(`You can only add ${remainingSlots} more photo(s)`);
    return;
  }

  // Validate file types and sizes
  const maxSize = 10 * 1024 * 1024; // 10MB
  const validFiles = files.filter(file => {
    if (!file.type.startsWith('image/')) {
      message.error(`${file.name} is not an image file`);
      return false;
    }
    if (file.size > maxSize) {
      message.error(`${file.name} is too large (maximum 10MB)`);
      return false;
    }
    return true;
  });

  validFiles.forEach(file => {
    const imageObj = {
      file,
      url: URL.createObjectURL(file),
      uploading: false,
      progress: 0,
      uploaded: false
    };
    uploadedImages.value.push(imageObj);
  });

  // Clear validation error if images are added
  if (uploadedImages.value.length > 0) {
    validationErrors.images = '';
  }

  event.target.value = '';
};

const removeImage = async (index, image_id) => {
  URL.revokeObjectURL(uploadedImages.value[index].url);
  uploadedImages.value.splice(index, 1);

  console.log(image_id)
  if (image_id) {
    try {
      const response = await api.delete(`/cars/car/image/${image_id}/`)
      message.success(response.data.message)
    } catch (error) {
      if (error.response) {
        console.log(error.response)
      } else {
        console.log(error)
      }
    }
  }

  validateField('images');
};

const uploadImages = async (carId) => {
  for (const imageObj of uploadedImages.value) {
    if (!imageObj.uploaded) {
      imageObj.uploading = true;
      try {
        const result = await carData.uploadImage(
          carId,
          imageObj.file,
          (progress) => {
            imageObj.progress = Math.round(progress);
          }
        );
        imageObj.uploaded = true;
        imageObj.uploading = false;
      } catch (error) {
        console.error('Error uploading image:', error);
        message.error(`Error uploading image: ${error.message}`);
        imageObj.uploading = false;
        throw error;
      }
    }
  }
};

const handleSubmit = async () => {
  // Validate entire form
  const isValid = validateForm();

  if (!isValid) {
    message.error('Please fill in all required fields');
    // Scroll to first error
    const firstErrorField = Object.keys(validationErrors).find(key => validationErrors[key]);
    if (firstErrorField) {
      const element = document.querySelector(`[name="${firstErrorField}"]`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
    return;
  }

  submitting.value = true;

  try {
    // Type mapping
    const typeMap = {
      'automobile': 'CR',
      'commercial': 'CT',
      'motorcycle': 'MO'
    };
    formData.avto_type = typeMap[selectedType.value];

    let carId = null
    if (route.params.id) {
      carId = await carData.changeCar({ ...formData });
    } else {
      carId = await carData.createCar({ ...formData });
    }

    if (!carId) {
      throw new Error('Car ID not received');
    }

    createdCarId.value = carId;

    // Step 2: Upload images
    // console.log('Uploading images...', carId);
    await uploadImages(carId);

    if (route.params.id) {
      message.success('Изменения успешно сохранены!')
    } else {
      message.success('Объявление успешно опубликовано!')
    }

    
    router.push(`/cars/detail/${carId}`)
  } catch (error) {
    console.error('Submit error:', error);
    message.error('Error creating listing');
  } finally {
    submitting.value = false;
  }
};

// Load initial data
const loadBrandsForType = async () => {
  const typeMap = {
    'automobile': 'CR',
    'commercial': 'CT',
    'motorcycle': 'MO'
  };

  loadingBrands.value = true;
  try {
    brands.value = await carData.getBrandsByType(typeMap[selectedType.value]);
  } catch (error) {
    message.error('Error loading brands');
  } finally {
    loadingBrands.value = false;
  }
};

const getDataCar = async () => {
  if (!route.params.id) return
  isLoading.value = true
  try {
    const response = await api.get(`/cars/car/${route.params.id}`)
    const data = response.data.data
    formData.avto_type = data.avto_type

    const typeMap = {
      'CR': 'automobile',
      'CT': 'commercial',
      'MO': 'motorcycle',
    };

    selectedType.value = typeMap[data.avto_type]
    formData.marka = data.marka
    formData.year = data.year
    formData.milage = data.milage
    formData.country = data.country
    formData.displacement = data.displacement
    formData.power = data.power
    formData.drive_type = data.drive_type
    formData.transmission_type = data.transmission_type
    formData.doors_count = data.doors_count
    formData.body = data.body
    formData.condition = data.condition
    formData.fuel = data.fuel
    formData.color = data.color
    formData.availability = data.availability
    formData.description = data.description
    formData.price = data.price
    uploadedImages.value = data.images.map((item) => {
      return {
        file: null,
        id: item.id,
        url: item.image,
        uploading: false,
        progress: 0,
        uploaded: true
      }
    })
    await handleMarkaChange(data.marka)
    formData.car_model = data.car_model
    await handleModelChange()
  } catch (error) {
    if (error.response) {
      console.log(error.response)
    } else {
      console.log(error)
    }
    errors.value = true
  } finally {
    isLoading.value = false
  }
}

// Watch for type change
watch(selectedType, () => {
  if (isLoading.value) return true
  formData.marka = null;
  formData.car_model = null;
  models.value = [];
  validationErrors.marka = '';
  validationErrors.car_model = '';
  loadBrandsForType();
});

// Initialize
onMounted(() => {
  loadBrandsForType();
  getDataCar()
});
</script>

<style scoped>
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.add-car-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #000;
}

.page-header p {
  font-size: 14px;
  color: #666;
}

.type-tabs {
  margin-bottom: 24px;
}

.type-tabs :deep(.ant-radio-group) {
  width: 100%;
  display: flex;
}

.type-tabs :deep(.ant-radio-button-wrapper) {
  flex: 1;
  text-align: center;
}

.form-section {
  margin-bottom: 16px;
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-top: 4px;
  line-height: 1.5;
}

.main-form {
  background: white;
  border-radius: 8px;
  padding: 24px;
  margin-top: 24px;
}

.characteristics-section,
.photos-section,
.description-section,
.price-section {
  margin-bottom: 32px;
}

.characteristics-section h2,
.photos-section h2,
.description-section h2,
.price-section h2 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #000;
}

.section-subtitle {
  font-size: 13px;
  color: #666;
  margin-bottom: 16px;
}

.upload-container {
  margin-top: 16px;
}

.uploaded-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
}

.image-item {
  position: relative;
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #d9d9d9;
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 8px;
  right: 8px;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-item:hover .image-overlay {
  opacity: 1;
}

.image-overlay button {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
}

.upload-button {
  aspect-ratio: 1;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #fafafa;
}

.upload-button:hover {
  border-color: #1890ff;
  background: #f0f7ff;
}

.upload-button p {
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

.submit-section {
  margin-top: 32px;
}

.submit-section :deep(.ant-btn) {
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
}

:deep(.ant-select),
:deep(.ant-input-number) {
  width: 100%;
}

/* Error state styling */
:deep(.ant-select-status-error .ant-select-selector),
:deep(.ant-input-number-status-error) {
  border-color: #ff4d4f !important;
}

:deep(.ant-select-status-error .ant-select-selector:hover),
:deep(.ant-input-number-status-error:hover) {
  border-color: #ff4d4f !important;
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 24px;
  }

  .uploaded-images {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>