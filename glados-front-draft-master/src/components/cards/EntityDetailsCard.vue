<template>
  <div
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click.self="$emit('close')">
    <div class="bg-white rounded-xl p-6 shadow-lg max-w-md w-full">
      <div class="flex flex-row justify-between">
        <h3 class="text-xl font-bold mb-2">{{ entity.name }}</h3>
        <Button
          label="Delete"
          color="danger"
          @click="$emit('delete')"/>
      </div>
      <p><strong>Room:</strong> {{ entity.room ?? "N/A" }}</p>
      <p class="flex flex-row gap-1">
        <strong>Type:</strong> <component :is="typeIcon"/> {{ entity.type.replace(/_/g, " ") }}</p>
      <p><strong>Status:</strong> {{ entity.status }}</p>
      <p><strong>Value:</strong> {{ entity.value ?? "-" }}</p>
      <p class="text-sm text-gray-500 mt-2">Created at: {{ formatDate(entity.created_at) }}</p>

      <div class="mt-6 flex justify-end gap-2">
        <Button 
          @click="$emit('close')"
          color="neutral"
          size="small"
          label="Close"/>
        <Button 
          @click="$emit('edit')"
          label="Edit"/>
      </div>
    </div>
  </div>
</template>
  
<script>

import Button from "@/components/buttons/Button.vue"
import getTypeIcon from "@/utils/entityTypeIcons.js"
  
export default {
  name: "EntityDetailsCard",
  components: {
    Button,
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    typeIcon() {
      return getTypeIcon(this.entity.type)
    }
  },
  methods: {
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleString("FR")
    }
  }
}
</script>
  