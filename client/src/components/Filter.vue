<template>
    <div class="filter_box">
        <div class="filter_radio">
            <a-radio-group v-model:value="condition" button-style="solid" size="large">
                <a-radio-button value="all">Все</a-radio-button>
                <a-radio-button value="new">Новые</a-radio-button>
                <a-radio-button value="fair">С пробегом</a-radio-button>
            </a-radio-group>
            <div class="check_box">
                <a-checkbox v-model:checked="in_stock">В наличии</a-checkbox>
                <a-checkbox v-model:checked="on_order">Под заказ</a-checkbox>
            </div>
        </div>
        <div class="select_box">
            <div class="select_item">
                <p class="select_title">Выберите марку</p>
                <a-select
                    v-model:value="value3"
                    placeholder="Marka"
                    :dropdown-render="dropdownRender"
                    @focus="focus"
                    @change="handleChange"
                    :loading="false"
                    style="width: 100%"> 
                </a-select>
            </div>
            <div class="select_item">
                <p class="select_title">Выберите марку</p>
                <a-select
                    v-model:value="value3"
                    placeholder="Marka"
                    :dropdown-render="dropdownRender"
                    @focus="focus"
                    @change="handleChange"
                    :loading="false"
                    style="width: 100%"> 
                </a-select>
            </div>
        </div>
    </div>
</template>

<script setup>
// import api from '@/utils/axios';
import { ref , h } from 'vue';

const condition = ref('all')
const in_stock = ref(false)
const on_order = ref(false)
const value3 = ref('lucy');

const options1 = ref([
  {
    value: 'jack',
    label: 'Jack',
  },
  {
    value: 'lucy',
    label: 'Lucy',
  },
  {
    value: 'disabled',
    label: 'Disabled',
    disabled: true,
  },
  {
    value: 'yiminghe',
    label: 'Yiminghe',
  },
]);
const focus = () => {
  console.log('focus');
};

const handleChange = (value) =>{
    console.log(value)
}

const brands = [
  'AC', 'Acura', 'Adlar', 'Aito', 'Aiways', 'Aixam',
  'Alfa Romeo', 'Alpina', 'AlpinaAM', 'General',
  'Hyndai', 'Acura', 'Adlar', 'Aito', 'Aiways', 'Aixam',
  'Alfa Romeo', 'Alpina', 'AlpinaAM', 'General',
  // ... boshqa brendlar
];

const dropdownRender = ({ menuNode }) => {
  return h('div', {
    style: {
      padding: '8px',
      maxHeight: '300px',
      overflowY: 'auto'
    }
  }, [
    h('div', {
      style: {
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '8px'
      }
    }, brands.map(brand => 
      h('div', {
        style: {
          padding: '8px 12px',
          cursor: 'pointer',
          fontSize: '14px',
          color: '#000',
          borderRadius: '4px',
          transition: 'background-color 0.2s'
        },
        onMouseenter: (e) => {
          e.target.style.backgroundColor = '#f5f5f5';
        },
        onMouseleave: (e) => {
          e.target.style.backgroundColor = 'transparent';
        },
        onClick: () => {
          value3.value = brand;
          handleChange(brand);
        }
      }, brand)
    ))
  ]);
};


// const handleGetMarka = async () => {
//     try {
//         const response = await api.get()
//     } catch (error) {
        
//     }
// }
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

.select_box{
    margin-top: 25px;
    display: flex;
    gap: 20px;
}

.select_title{
    font-weight: 400;
    font-size: 14px;
    color: #050B20;
    margin-bottom: 10px;
}
</style>