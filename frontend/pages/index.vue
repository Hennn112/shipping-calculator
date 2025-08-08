<!-- pages/index.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 to-red-100 p-10">
    <div class="container mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">International Freight Calculator</h1>
        <p class="text-gray-600">Calculate shipping costs from international origins to Indonesia</p>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
        <FreightForm @result="handleResult" />
        
        <div v-if="calculationResult" class="space-y-4">
          <FreightResult :result="calculationResult" />
        </div>
        
        <div v-else-if="!calculationResult" class="flex items-center justify-center">
          <div class="text-center text-gray-500">
            <div class="text-6xl mb-4">📦</div>
            <p class="text-lg">Fill the form to calculate shipping costs</p>
            <p class="text-sm mt-2">Select origin, destination, category and weight to get started</p>
          </div>
        </div>
      </div>

      <!-- Loading overlay -->
      <div v-if="isCalculating" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>Calculating shipping costs...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import FreightForm from '~/components/FreightForm.vue'
import FreightResult from '~/components/FreightResult.vue'

// Meta tags
useHead({
  title: 'International Freight Calculator',
  meta: [
    { name: 'description', content: 'Calculate international shipping costs to Indonesia' }
  ]
})

const calculationResult = ref(null)
const isCalculating = ref(false)

function handleResult(result) {
  calculationResult.value = result
  
  // Optional: scroll to result on mobile
  if (process.client && window.innerWidth < 1024) {
    setTimeout(() => {
      const resultElement = document.querySelector('[data-result]')
      if (resultElement) {
        resultElement.scrollIntoView({ behavior: 'smooth' })
      }
    }, 100)
  }
}

// Optional: Clear result when starting new calculation
provide('clearResult', () => {
  calculationResult.value = null
})
</script>

<style scoped>
/* Additional responsive styles */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
}

/* Custom scrollbar for mobile */
:deep(.overflow-y-auto) {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

:deep(.overflow-y-auto::-webkit-scrollbar) {
  width: 6px;
}

:deep(.overflow-y-auto::-webkit-scrollbar-track) {
  background: #f7fafc;
}

:deep(.overflow-y-auto::-webkit-scrollbar-thumb) {
  background: #cbd5e0;
  border-radius: 3px;
}
</style>