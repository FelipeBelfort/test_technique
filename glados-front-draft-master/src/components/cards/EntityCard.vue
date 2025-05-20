<template>
  <div class="bg-stone-100 rounded-xl shadow p-4  gap-2 border border-gray-100 hover:shadow-xl hover:cursor-pointer transition">
    <div class="flex flex-col">
      <h3 class="text-lg pl-2 font-semibold text-gray-800 capitalize">{{ entity.name }}</h3>
      <p class="text-md pl-2 text-gray-600 ">{{ entity.room ?? "N/A" }}</p>
      <p class="text-sm pl-2 text-gray-500 pb-2">{{ entity.type.replace(/_/g, " ") }} <component :is="typeIcon"/> </p>
      <Button
        :label="entity.status"
        :color="buttonColor"
        @click="modifyEntity"
        size="statusButton"
        :disabled="entity.status === 'unavailable'"/>
    </div>
  </div>
</template>

<script>

import Button from "@/components/buttons/Button.vue"
import getTypeIcon from "@/utils/entityTypeIcons.js"

export default {
  name: "EntityCard",
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
    },
    buttonColor() {
      return this.entity.status === "on" ? "on" : "danger"
    },
  },
  methods: {
    modifyEntity(event) {
      event.stopPropagation()
      this.$emit("toggle", this.entity)
    },
  },
}
</script>
  