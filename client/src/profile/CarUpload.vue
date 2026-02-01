<template>
  <div class="add-car-page">
    <div class="container">
      <div class="page-header">
        <h1>Разместите объявление</h1>
        <p>Укажите данные об автомобиле для размещения объявления</p>
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
          :disabled="!selectedType" @change="handleMarkaChange" :filter-option="filterOption">
          <a-select-option v-for="brand in brands" :key="brand.id" :value="brand.id" :label="brand.marka">
            {{ brand.marka }}
          </a-select-option>
        </a-select>
      </div>

      <!-- Step 3: Model Selection -->
      <div class="form-section" v-if="formData.marka">
        <a-select v-model:value="formData.car_model" placeholder="Модель" size="large" show-search
          :loading="loadingModels" @change="handleModelChange" :filter-option="filterOption">
          <a-select-option v-for="model in models" :key="model.id" :value="model.id" :label="model.name">
            {{ model.name }}
          </a-select-option>
        </a-select>
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
                <a-form-item label="Год выпуска">
                  <a-input-number v-model:value="formData.year" :min="1951" :max="currentYear" placeholder="2024"
                    style="width: 100%" size="large" />
                </a-form-item>
              </a-col>

              <!-- Price -->
              <a-col :span="12">
                <a-form-item label="Пробег">
                  <a-input-number v-model:value="formData.milage" :min="0" :max="2000000" placeholder="16 000"
                    style="width: 100%" size="large">
                    <template #addonAfter>км</template>
                  </a-input-number>
                </a-form-item>
              </a-col>

              <!-- Country -->
              <a-col :span="12">
                <a-form-item label="Страна">
                  <a-select v-model:value="formData.country" placeholder="США" size="large" show-search
                    :loading="loadingCountries" :filter-option="filterOption">
                    <a-select-option v-for="country in countries" :key="country.id" :value="country.id">
                      {{ country.country }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>

              <!-- Fuel -->
              <a-col :span="12">
                <a-form-item label="Топливо">
                  <a-select v-model:value="formData.fuel" placeholder="Бензин" size="large" :loading="loadingFuels">
                    <a-select-option v-for="fuel in fuels" :key="fuel.id" :value="fuel.id">
                      {{ fuel.name }}
                    </a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>

              <!-- Displacement -->
              <a-col :span="12">
                <a-form-item label="Объем">
                  <a-input-number v-model:value="formData.displacement" :min="0" :max="9.9" :step="0.1"
                    placeholder="1.8" style="width: 100%" size="large">
                    <template #addonAfter>л</template>
                  </a-input-number>
                </a-form-item>
              </a-col>

              <!-- Power -->
              <a-col :span="12">
                <a-form-item label="Мощность">
                  <a-input-number v-model:value="formData.power" :min="0" :max="2000" placeholder="153"
                    style="width: 100%" size="large">
                    <template #addonAfter>л.с</template>
                  </a-input-number>
                </a-form-item>
              </a-col>

              <!-- Transmission -->
              <a-col :span="12">
                <a-form-item label="Привод">
                  <a-select v-model:value="formData.drive_type" placeholder="Передний" size="large">
                    <a-select-option value="FWD">Передний</a-select-option>
                    <a-select-option value="RWD">Задний</a-select-option>
                    <a-select-option value="AWD">Полный</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>

              <!-- КПП -->
              <a-col :span="12">
                <a-form-item label="КПП">
                  <a-select v-model:value="formData.transmission_type" placeholder="Автомат" size="large">
                    <a-select-option value="MT">Механика</a-select-option>
                    <a-select-option value="AT">Автомат</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>

              <!-- Doors Count -->
              <a-col :span="12">
                <a-form-item label="Количество дверей">
                  <a-select v-model:value="formData.doors_count" placeholder="5" size="large">
                    <a-select-option :value="2">2</a-select-option>
                    <a-select-option :value="3">3</a-select-option>
                    <a-select-option :value="4">4</a-select-option>
                    <a-select-option :value="5">5</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>

              <!-- Body Type -->
              <a-col :span="12">
                <a-form-item label="Кузов">
                  <a-select v-model:value="formData.body" placeholder="Седан" size="large">
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
                <a-form-item label="Состояние">
                  <a-select v-model:value="formData.condition" placeholder="С пробегом" size="large">
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
                <a-form-item label="Цвет">
                  <a-select v-model:value="formData.color" placeholder="Белый" size="large" :loading="loadingColors">
                    <a-select-option v-for="color in colors" :key="color.id" :value="color.id">
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
                <img :src="image.url" :alt="`Car photo ${index + 1}`" />
                <div class="image-overlay">
                  <a-button type="text" danger @click="removeImage(index)" :icon="h(DeleteOutlined)" />
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
            <input ref="fileInput" type="file" accept="image/*" multiple style="display: none;"
              @change="handleFileSelect" />
          </div>
        </div>

        <!-- Description Section -->
        <div class="description-section">
          <h2>Описание</h2>
          <p class="section-subtitle">Не указывайте ссылки на источники, цены, контакты и не предлагайте другие услуги!
            Объявление не пройдет модерацию</p>

          <a-form-item>
            <a-textarea v-model:value="formData.description" placeholder="Четко опишите вашу авто" :rows="6"
              :maxlength="1200" show-count />
          </a-form-item>
        </div>

        <!-- Price Section -->
        <div class="price-section">
          <h2>Цена</h2>
          <a-form-item>
            <a-input-number v-model:value="formData.price" :min="0" :max="999999999" placeholder="1 850 000"
              size="large" style="width: 100%">
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
            Опубликовать объявления
          </a-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, h, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { CameraOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import { watch } from 'vue';
import api from '@/utils/axios';

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
  status: 'DF'
});

const currency = ref('USD');
const currentYear = new Date().getFullYear();

// Loading states
const loadingBrands = ref(false);
const loadingModels = ref(false);
const loadingCountries = ref(false);
const loadingColors = ref(false);
const loadingFuels = ref(false);
const submitting = ref(false);

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

  async getModelsByBrand(brandId) {
    try {
      const { data } = await api.post("cars/models/", {
        marka_id: brandId
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
      const { data } = await api.get("cars/countries/")
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
      const response = await api.post("cars/upload/", { ...data })
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
      throw error; // ← Muhim: xatoni qayta tashlash
    }
  },

  // carData obyekti ichida
  async uploadImage(carId, file, onProgress , isMain = false) {
    const formData = new FormData();
    formData.append('car', carId);
    formData.append('image', file);
    formData.append('is_main', isMain);
    try {
      const response = await api.post('cars/upload/image/', formData, {
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
        console.error('Upload xatosi:', error.response.data);
        throw new Error(error.response.data.message || 'Rasm yuklashda xatolik');
      } else {
        console.error('Network xatosi:', error);
        throw new Error('Tarmoq xatosi');
      }
    }
  }
};

// Methods
const filterOption = (input, option) => {
  return option.label.toLowerCase().includes(input.toLowerCase());
};

const handleMarkaChange = async (brandId) => {
  formData.car_model = null;
  models.value = [];

  if (brandId) {
    loadingModels.value = true;
    try {
      models.value = await carData.getModelsByBrand(brandId);
    } catch (error) {
      message.error('Modellarni yuklashda xatolik');
    } finally {
      loadingModels.value = false;
    }
  }
};

const handleModelChange = async () => {
  if (!countries.value.length) {
    loadingCountries.value = true;
    try {
      countries.value = await carData.getCountries();
    } catch (error) {
      message.error('Davlatlarni yuklashda xatolik');
    } finally {
      loadingCountries.value = false;
    }
  }

  if (!colors.value.length) {
    loadingColors.value = true;
    try {
      colors.value = await carData.getColors();
    } catch (error) {
      message.error('Ranglarni yuklashda xatolik');
    } finally {
      loadingColors.value = false;
    }
  }

  if (!fuels.value.length) {
    loadingFuels.value = true;
    try {
      fuels.value = await carData.getFuels();
    } catch (error) {
      message.error('Yoqilg\'i turlarini yuklashda xatolik');
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
    message.warning(`Faqat ${remainingSlots} ta rasm qo'shishingiz mumkin`);
    return;
  }

  files.forEach(file => {
    if (file.type.startsWith('image/')) {
      const imageObj = {
        file,
        url: URL.createObjectURL(file),
        uploading: false,
        progress: 0,
        uploaded: false
      };
      uploadedImages.value.push(imageObj);
    }
  });

  event.target.value = '';
};

const removeImage = (index) => {
  URL.revokeObjectURL(uploadedImages.value[index].url); // Memory cleanup
  uploadedImages.value.splice(index, 1);
};

const uploadImages = async (carId) => {
  // Rasmlarni ketma-ket yuklash (reaktivlikni yaxshiroq saqlash uchun)
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
        // console.log('Rasm yuklandi:', result);
      } catch (error) {
        console.error('Rasm yuklashda xatolik:', error);
        message.error(`Rasmni yuklashda xatolik: ${error.message}`);
        imageObj.uploading = false;
        throw error;
      }
    }
  }
};

const handleSubmit = async () => {
  // Validatsiya
  if (!formData.marka || !formData.car_model) {
    message.warning('Marka va modelni tanlang');
    return;
  }

  if (uploadedImages.value.length === 0) {
    message.warning('Kamida bitta rasm yuklang');
    return;
  }

  submitting.value = true;

  try {
    // Type mapping
    const typeMap = {
      'automobile': 'bf763424-691f-4a5d-a1e8-299983ef708e',
      'commercial': 'f972a831-6bf5-4e20-9908-2617ec6a5417',
      'motorcycle': '2e035902-ba42-487e-bae2-be723156c6c1'
    };
    formData.avto_type = typeMap[selectedType.value];

    // Step 1: Mashina yaratish
    console.log('Mashina yaratilmoqda...', formData);
    const carId = await carData.createCar({ ...formData }); // ← Bu allaqachon ID

    if (!carId) {
      throw new Error('Mashina ID olinmadi');
    }

    createdCarId.value = carId;
    message.success('Avtomobil ma\'lumotlari saqlandi');

    // Step 2: Rasmlarni yuklash
    console.log('Rasmlar yuklanmoqda...', carId);
    await uploadImages(carId);
    message.success('Rasmlar yuklandi');

    message.success('E\'lon muvaffaqiyatli yaratildi!');

    // Redirect yoki formni tozalash
    // router.push('/my-listings');

  } catch (error) {
    console.error('Submit xatosi:', error);
    message.error('E\'lonni yaratishda xatolik yuz berdi');
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
    message.error('Markalarni yuklashda xatolik');
  } finally {
    loadingBrands.value = false;
  }
};

// Watch for type change
watch(selectedType, () => {
  formData.marka = null;
  formData.car_model = null;
  models.value = [];
  loadBrandsForType();
});

// Initialize
onMounted(() => {
  loadBrandsForType();
});
</script>

<style scoped>
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

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 24px;
  }

  .uploaded-images {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>