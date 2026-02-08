<template>
  <div class="filter_box">
    <div>
      <div class="filter_radio">
        <a-radio-group v-model:value="condition" @change="handleChangeCondition" button-style="solid" size="large">
          <a-radio-button value="all">Все</a-radio-button>
          <a-radio-button value="new">Новые</a-radio-button>
          <a-radio-button value="fair">С пробегом</a-radio-button>
        </a-radio-group>
        <div class="check_box">
          <a-checkbox v-model:checked="in_stock" @change="handleInStockChange">В наличии</a-checkbox>
          <a-checkbox v-model:checked="on_order" @change="handleOnOrderChange">Под заказ</a-checkbox>
        </div>
      </div>
      <div class="select_box">
        <div class="select_item">
          <p class="select_title">Выберите марку</p>
          <a-select v-model:value="marka" class="select_form" placeholder="Marka" :options="markas" @focus="focus"
            @change="handleChange" :loading="markaLoading" :filter-option="filterOption" show-search
            popupClassName="multi-column-dropdown">
          </a-select>
        </div>
        <div class="select_item">
          <p class="select_title">ВЫберите модель</p>
          <a-select v-model:value="model" class="select_form" placeholder="Model" :options="models" @focus="focusModel"
            @change="handleChangeModel" :filter-option="filterOption" show-search :loading="modelLoading"
            popupClassName="multi-column-dropdown">
          </a-select>
        </div>
        <div class="select_item">
          <p class="select_title">Страна</p>
          <a-select v-model:value="country" class="select_form" placeholder="Country" :options="countries"
            @focus="focusCountry" @change="handleChangeCountry" :filter-option="filterOption" show-search
            :loading="countryLoading" popupClassName="multi-column-dropdown">
          </a-select>
        </div>
        <div class="select_item">
          <p class="select_title">Год</p>
          <a-range-picker v-model:value="year" class="select_form" @change="onRangeChange" picker="year" />
        </div>
        <div class="select_item">
          <p class="select_title">Цена</p>
          <a-slider v-model:value="value2" range :step="1000" :max="200000" @afterChange="onAfterChange" />
        </div>
      </div>
    </div>
    <div class="filter_btns">
      <a-button size="large" @click="handleClear">Сбросить</a-button>
      <a-button type="primary" size="large" :disabled="paramsValid">{{ props.count }} Предложений</a-button>
    </div>
  </div>
</template>

<script setup>
import api from '@/utils/axios';
import { computed, ref } from 'vue';

const emit = defineEmits(['params'])
const props = defineProps({
  count: Number
})


const params = ref({})
const paramsValid = computed(() => {
  return Object.keys(params.value).length > 0
})

const condition = ref('all')
const in_stock = ref(false)
const on_order = ref(false)

const marka = ref("Марка");
const model = ref("Модель")
const country = ref("Страна") 

// Loaders
const markaLoading = ref(false)
const modelLoading = ref(false)
const countryLoading = ref(false)

const markas = ref([]);
const models = ref([]);
const countries = ref([])
const year = ref()
const value2 = ref([20, 50]);

const focus = () => {
  handleGetMarka()
};

const focusModel = () => {
  handleGetModels()
}

const focusCountry = () => {
  handleGetCountries()
}

/////////////////////// param berish

const handleChangeModel = (value) => {
  params.value = { ...params.value, model: value }
  emit("params", params.value)
}

const handleChangeCountry = (value) => {
  params.value = { ...params.value, country: value }
  emit("params", params.value)
}

const handleChange = (value) => {
  params.value = { ...params.value, marka: value }
  emit("params", params.value)
}

const onRangeChange = (value, dateString) => {
  const year_to = dateString[1]
  const year_from = dateString[0]
  params.value = { ...params.value, year_from: year_from, year_to: year_to }
  emit("params", params.value)
};

const onAfterChange = value => {
  const price_from = value[0]
  const price_to = value[1]
  params.value = { ...params.value, price_from: price_from, price_to: price_to }
  emit("params", params.value)
};

const filterOption = (input, option) => {
  return option.value.toLowerCase().indexOf(input.toLowerCase()) >= 0;
};

const handleInStockChange = (e) => {
  if (in_stock.value) {
    params.value['availability'] = "in_stock"
    emit('params', params.value)
  }
}

const handleChangeCondition = (e) => {
  params.value = { ...params.value, condition: e.target.value }
  emit('params', params.value)
}

const handleOnOrderChange = (e) => {
  if (on_order.value) {
    params.value['availability'] = 'on_order'
    emit('params', params.value)
  }
}


///////////////////////////////// get api ///////////////////////////////////////
const handleGetMarka = async () => {
  markaLoading.value = true
  try {
    const { data } = await api.get("/cars/marka/all/")
    markas.value = data.map((item) => {
      return { value: item.marka, label: item.marka }
    })
  } catch (error) {
    console.log(error.response || error)
  } finally {
    markaLoading.value = false
  }
}

const handleGetModels = async () => {
  modelLoading.value = true
  try {
    const { data } = await api.get("/cars/models/all/")
    models.value = data.map((item) => {
      return { value: item.name, label: item.name }
    })
  } catch (error) {
    console.log(error.response || error)
  } finally {
    modelLoading.value = false
  }
}

const handleGetCountries = async () => {
  countryLoading.value = true
  try {
    const { data } = await api.get("/cars/countries/")
    countries.value = data.map((item) => {
      return { value: item.country, label: item.country }
    })
  } catch (error) {
    console.log(error.response || error)
  } finally {
    countryLoading.value = false
  }
}


///////////////////////////// CLEAR /////////////////////
const handleClear = () =>{
  params.value = {}
  model.value = "Модель"
  marka.value = "Марка"
  country.value = "Страна"
  emit('params' , params.value)
}
</script>

<style scoped>
.filter_box {
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 20px;
}

.filter_radio {
  display: flex;
  align-items: center;
  gap: 20px;
}

.select_box {
  margin-top: 25px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.select_box .select_item {
  flex: 1;
}

.select_form {
  width: 100%;
}

.select_title {
  font-weight: 400;
  font-size: 14px;
  color: #050B20;
  margin-bottom: 10px;
}

.filter_btns {
  margin-top: 20px;
  display: flex;
  justify-content: end;
  gap: 20px;
}
</style>

<style>
/* Global style - scoped bo'lmasligi kerak! */
.multi-column-dropdown {
  min-width: 500px !important;
}

.multi-column-dropdown .rc-virtual-list-holder-inner {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 4px !important;
  padding: 8px !important;
}

.multi-column-dropdown .ant-select-item {
  padding: 8px 12px !important;
  font-size: 14px !important;
}

.multi-column-dropdown .ant-select-item-option-active {
  background-color: #f5f5f5 !important;
}

.multi-column-dropdown .ant-select-item-option-selected {
  background-color: #e6f4ff !important;
}

/* Responsive */
@media (max-width: 768px) {
  .multi-column-dropdown {
    min-width: 350px !important;
  }

  .multi-column-dropdown .rc-virtual-list-holder-inner {
    grid-template-columns: repeat(2, 1fr) !important;
  }

  .filter_radio {
    flex-direction: column;
    align-items: start;
    justify-content: start;
  }

  .select_box {
    flex-direction: column;
  }

  .select_item {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .multi-column-dropdown {
    min-width: 280px !important;
  }

  .multi-column-dropdown .rc-virtual-list-holder-inner {
    grid-template-columns: 1fr !important;
  }
}
</style>