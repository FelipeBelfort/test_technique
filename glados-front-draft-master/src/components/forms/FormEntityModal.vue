<template>
  <div
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click.self="$emit('close')">
    <div class="bg-white rounded-xl p-6 shadow-lg max-w-xl w-full">
      <h3 class="text-xl font-bold mb-4">{{ isEditing ? 'Edit ' : 'Create ' }}Entity</h3>

      <div class="space-y-4">
        <Input
          label="Name"
          prop="name"
          v-model="entityForm.name"
          :mask="{
            mask: new Array(26).join('L'),
            tokens: { 'L': { pattern: /[0-9A-zÀ-ú- ]/ } }
          }"
          :placeholders="['Smart Light', 'Motion Sensor']"/>
        <p
          v-if="isDuplicate"
          class="text-sm text-yellow-600">
          {{ entity ? "" : "This entity name is already used. " }}Please choose a different name.
        </p>

        <div class="flex flex-row gap-2 items-center">

          <p><strong>Room:</strong></p>
          <select
            v-model="entityForm.room_id"
            class="block w-full mt-1 border-gray-300 rounded-md">
            <option 
              disabled 
              value="">Select Room</option>
            <option value="null">No Room</option>
            <option
              v-for="room in rooms"
              :key="room.id"
              :value="room.id">{{ room.name }}</option>
          </select>
        </div>

        <div class="flex flex-row gap-2 items-center">

          <p class="mr-2"><strong>Type:</strong></p>
          <select
            v-model="entityForm.type"
            class="block w-full mt-1 border-gray-300 rounded-md">
            <option 
              disabled 
              value="">Select Type</option>
            <option 
              v-for="type in types" 
              :key="type" 
              :value="type">{{ type.replace(/_/g, " ") }}</option>
          </select>
        </div>
        
        <div class="flex flex-row gap-2 items-center">
          <p><strong>Status:</strong></p>
          <select
            v-model="entityForm.status"
            class="block w-full mt-1 border-gray-300 rounded-md">
            <option 
              disabled 
              value="">Select Status</option>
            <option 
              v-for="status in statuses" 
              :key="status" 
              :value="status">{{ status }}</option>
          </select>
        </div>

        <div class="flex flex-row gap-2 items-center">
          <p><strong>Value:</strong></p>
          <Input
            prop="value"
            v-model="entityForm.value"
            :mask="{
              mask: new Array(16).join('L'),
              tokens: { 'L': { pattern: /[0-9A-zÀ-ú- ]/ } }
            }"
            :placeholders="['Optional Value']"/>
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <Button 
          label="Cancel" 
          color="neutral" 
          @click="$emit('close')" />
        <Button
          :label="isEditing ? 'Update' : 'Create'"
          :disabled="!isValid"
          @click="submitEntity" />
      </div>
    </div>
  </div>
</template>

<script>
import { ENTITY_TYPES, ENTITY_STATUSES } from "@/constants/entityConstants"
import Button from "@/components/buttons/Button.vue"
import Input from "@/components/forms/Input.vue"

export default {
  name: "FormEntityModal",
  components: {
    Input,
    Button,
  },
  props: {
    entity: {
      type: Object,
      required: true
    },
    rooms: {
      type: Array,
      required: true
    },
    isEditing: {
      type: Boolean,
      default: false
    },
    existingEntities: {
      type: Array,
      required: true
    },
  },
  data() {
    return {
      types: ENTITY_TYPES,
      statuses: ENTITY_STATUSES,
      entityForm: {
        name: this.entity?.name ?? "",
        type: this.entity?.type ?? "",
        status: this.entity?.status ?? "",
        room_id: this.entity?.room_id ?? (this.entity?.room_id === null ? "null" : ""),
        value: this.entity?.value ?? "",
      }
    }
  },
  computed: {
    isValid() {
      return (
        this.entityForm.name &&
        this.entityForm.type &&
        this.entityForm.room_id &&
        this.entityForm.status
      )
    },
    isDuplicate() {
      const name = this.entityForm.name.trim().toLowerCase()
      return this.existingEntities.some(r => r.name.toLowerCase() === name)
    },
  },
  methods: {
    submitEntity() {
      if (this.entityForm.room_id === "null") this.entityForm.room_id = null
      if (this.entityForm.value === "") this.entityForm.value = null
      this.$emit("submit", { ...this.entityForm })
    }
  }
}
</script>
