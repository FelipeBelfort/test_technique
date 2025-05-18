<template>
  <div
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click.self="$emit('close')">
    <div class="bg-white rounded-xl p-6 shadow-lg max-w-md w-full">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">Confirm Deletion</h2>
      <p class="text-gray-600 mb-6">
        Are you sure you want to delete this {{ itemType }}?
      </p>
      <p class="text-gray-800 mb-6 text-center text-xl">
        <strong>{{ obj.name }}</strong>
      </p>

      <div class="mt-6 flex justify-between">
        <Button
          label="Cancel"
          size="small"
          color="neutral"
          @click="$emit('close')"/>
        <Button
          label="Delete"
          color="danger"
          @click="$emit('confirm')"/>
      </div>
    </div>
  </div>
</template>
  
<script>

import Button from "@/components/buttons/Button.vue"

  
export default {
  name: "ConfirmDeleteCard",
  components: { Button, },
  props: {
    obj: {
      type: Object,
      required: true
    },
    itemType: {
      type: String,
      required: true
    },
  },
}
</script>
  