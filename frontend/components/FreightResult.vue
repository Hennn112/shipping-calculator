<!-- components/FreightResult.vue -->
<template>
  <div class="p-6 bg-white rounded-lg shadow w-full">
    <h2 class="font-bold mb-2">
      Origin 
      <span class="text-gray-500 float-right">Destination</span>
    </h2>
    <p class="mb-4">
      <strong>{{ result.origin }}</strong>
      <span class="float-right font-bold">{{ result.destination }}</span>
    </p>

    <div class="mb-4 text-sm text-gray-600">
      <p><strong>Category:</strong> {{ result.category_name }}</p>
      <p><strong>Weight:</strong> {{ result.weight }} Kg</p>
    </div>

    <div class="space-y-2">
      <div class="flex justify-between">
        <span>International Shipping Price</span>
        <span class="font-bold text-lg">Rp. {{ formatCurrency(result.international_price) }}</span>
      </div>
      <div class="flex justify-between">
        <span>Domestic Shipping Price</span>
        <span class="font-bold">Rp. {{ formatCurrency(result.domestic_price) }}</span>
      </div>
      <hr class="my-2" />
      <div class="flex justify-between text-lg font-bold">
        <span>Total Shipping Price</span>
        <span>Rp. {{ formatCurrency(result.total_price) }}</span>
      </div>
    </div>

    <div class="mt-4 pt-4 border-t text-xs text-gray-500">
      <p>* International price calculated based on weight × category rate</p>
      <p>* Domestic price from cheapest shipping service available</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  result: {
    type: Object,
    required: true
  }
})

function formatCurrency(amount) {
  // Convert string to number and format with thousand separators
  const num = parseFloat(amount) || 0
  return num.toLocaleString('id-ID')
}
</script>