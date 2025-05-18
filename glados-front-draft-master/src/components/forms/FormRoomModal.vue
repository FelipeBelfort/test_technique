<template>
  <div
    @click.self="closeModal"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">{{ room ? "Rename" : "Create New" }} Room</h2>
      <form 
        @submit.prevent="submitForm" 
        class="space-y-4">
        <Input
          v-model="roomName"
          label="Room Name"
          icon="home-outline"
          :mask="{
            mask: new Array(26).join('L'),
            tokens: { 'L': { pattern: /[0-9A-zÀ-ú- ]/ } }
          }"
          :placeholders="['Living Room', 'Bedroom', 'Kitchen', 'Garage']"
          prop="name"/>
        <p
          v-if="error"
          class="text-sm text-red-500">
          {{ error }}
        </p>
        <p
          v-if="isDuplicate"
          class="text-sm text-yellow-600">
          {{ room ? "" : "This room name is already used. " }}Please choose a different name.
        </p>
        <div class="flex justify-end gap-2">
          <Button
            type="button"
            label="Cancel"
            size="small"
            color="neutral"
            @click="closeModal"/>
          <Button
            type="submit"
            :label="buttonLabel"
            :disabled="isInvalid || loading"
            :loading="loading"/>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import Button from "@/components/buttons/Button.vue"
import Input from "@/components/forms/Input.vue"

export default {
  name: "FormRoomModal",
  components: {
    Input,
    Button 
  },
  props: {
    existingRooms: {
      type: Array,
      required: true
    },
    room: {
      type: Object,
      default: null
    }
  },
  created() {
    this.hasRoom()
  },
  data() {
    return {
      oldName: "",
      roomName: "",
      buttonLabel: "Create",
      loading: false,
      error: null
    }
  },
  computed: {
    isInvalid() {
      return this.roomName.trim() === this.oldName || this.isDuplicate
    },
    isDuplicate() {
      const name = this.roomName.trim().toLowerCase()
      return this.existingRooms.some(r => r.toLowerCase() === name)
    }
  },
  methods: {
    hasRoom() {
      if (this.room) {
        this.oldName = this.room.name
        this.roomName = this.room.name
        this.buttonLabel = "Rename"
      }
    },
    closeModal() {
      this.roomName = ""
      this.error = null
      this.$emit("close")
    },
    async submitForm() {
      this.loading = true
      this.error = null

      if (this.isDuplicate) {
        this.error = "This room already exists."
        this.loading = false
        return
      }

      try {
        await this.$emit("submit", this.roomName.trim())
        this.closeModal()
      } catch (err) {
        this.error = "Failed to create room."
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
