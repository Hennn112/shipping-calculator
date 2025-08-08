<!-- components/FreightForm.vue -->
<template>
  <div class="p-6 bg-white rounded-lg shadow w-full max-w-sm">
    <h2 class="text-lg font-bold mb-4">Freight Calculator</h2>

    <label class="block mb-2">Origin</label>
    <select v-model="form.countryId" class="input" @change="loadCategories">
      <option value="">Select Country</option>
      <option 
        v-for="country in countries" 
        :key="country.id" 
        :value="country.id"
      >
        {{ country.country_name }}
      </option>
    </select>

    <label class="block mt-4 mb-2">Destination</label>
    <div class="relative">
      <input
        v-model="destinationSearch"
        type="text"
        class="input"
        placeholder="Search destination..."
        @input="searchDestination"
      />
      <div v-if="destinations.length > 0" class="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-b max-h-40 overflow-y-auto z-10">
        <div 
          v-for="dest in destinations" 
          :key="dest.subdistrict_id"
          class="p-2 hover:bg-gray-100 cursor-pointer text-sm"
          @click="selectDestination(dest)"
        >
          {{ dest.subdistrict_name }}, {{ dest.city_name }}, {{ dest.province_name }}, {{ dest.zip_code }}
        </div>
      </div>
    </div>

    <label class="block mt-4 mb-2">Product Category</label>
    <select v-model="form.categoryId" class="input" :disabled="!form.countryId">
      <option value="">Select Category</option>
      <option 
        v-for="category in categories" 
        :key="category.id" 
        :value="category.id"
      >
        {{ category.category_title }}
      </option>
    </select>

    <label class="block mt-4 mb-2">Total Weight</label>
    <div class="flex items-center gap-2">
      <input 
        v-model="form.weight" 
        type="number" 
        class="input w-full" 
        placeholder="15" 
        step="0.1"
        min="0.1"
      />
      <span>Kg</span>
    </div>

    <button 
      class="mt-6 w-full bg-blue-600 text-white p-2 rounded disabled:bg-gray-400" 
      @click="calculate"
      :disabled="loading || !canCalculate"
    >
      {{ loading ? 'Calculating...' : 'Calculate' }}
    </button>

    <div v-if="error" class="mt-4 p-2 bg-red-100 text-red-700 rounded text-sm">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['calculate', 'result'])

const BASE_URL = 'http://localhost:8000/api'

const loading = ref(false)
const error = ref('')
const countries = ref([])
const categories = ref([])
const destinations = ref([])
const destinationSearch = ref('')
const selectedDestination = ref(null)

const form = reactive({
  countryId: '',
  categoryId: '',
  weight: 1,
  destinationId: ''
})

const canCalculate = computed(() => {
  return form.countryId && form.categoryId && form.weight > 0 && selectedDestination.value
})

// Load countries on mount
onMounted(() => {
  loadCountries()
})

async function loadCountries() {
  try {
    const response = await $fetch(`${BASE_URL}/countries/`)
    countries.value = response.results || response
  } catch (err) {
    error.value = 'Failed to load countries'
    console.error(err)
  }
}

async function loadCategories() {
  if (!form.countryId) {
    categories.value = []
    return
  }
  
  try {
    const response = await $fetch(`${BASE_URL}/categories/?country_id=${form.countryId}`)
    categories.value = response.results || response
    form.categoryId = '' // Reset category selection
  } catch (err) {
    error.value = 'Failed to load categories'
    console.error(err)
  }
}

let searchTimeout = null
async function searchDestination() {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  if (destinationSearch.value.length < 3) {
    destinations.value = []
    return
  }

  searchTimeout = setTimeout(async () => {
    try {
      const response = await $fetch(`${BASE_URL}/destinations/?keyword=${destinationSearch.value}`)
      destinations.value = response.data || []
    } catch (err) {
      console.error('Failed to search destinations:', err)
      destinations.value = []
    }
  }, 300)
}

function selectDestination(dest) {
  selectedDestination.value = dest
  form.destinationId = dest.id
  destinationSearch.value = `${dest.subdistrict_name}, ${dest.city_name}, ${dest.province_name}, ${dest.zip_code}`
  destinations.value = []
}

async function calculate() {
  if (!canCalculate.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const params = new URLSearchParams({
      country_id: form.countryId,
      category_id: form.categoryId,
      weight: form.weight,
      destination_subdistrict_id: form.destinationId
    })

    const result = await $fetch(`${BASE_URL}/calculate/?${params}`)
    
    // Emit result to parent
    emit('result', {
      ...result,
      destination: destinationSearch.value,
      weight: form.weight
    })
    
  } catch (err) {
    console.error('Calculation error:', err)
    error.value = err.data?.error || 'Failed to calculate shipping cost'
  } finally {
    loading.value = false
  }
}

// Close dropdown when clicking outside
function handleClickOutside(event) {
  if (!event.target.closest('.relative')) {
    destinations.value = []
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.input {
  @apply w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500;
}
</style>