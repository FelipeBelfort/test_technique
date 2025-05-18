<template>
  <div class="bg-stone-100 rounded-xl shadow p-4  gap-2 border border-gray-100 hover:shadow-xl hover:cursor-pointer transition">
    <div class="flex flex-col">
      <h3 class="text-lg pl-2 font-semibold text-gray-800 capitalize">{{ entity.name }}</h3>
      <p class="text-md pl-2 text-gray-600 ">{{ entity.room ?? "N/A" }}</p>
      <p class="text-sm pl-2 text-gray-500 pb-2">{{ entity.type.replace(/_/g, " ") }} <component :is="typeIcon"/> </p>
      <span
        :class="[
          'text-sm text-center font-bold flex-auto rounded place-items-center',
          entity.status === 'on'
            ? 'bg-green-100 text-green-800'
            : 'bg-red-100 text-red-800'
        ]">
        {{ entity.status.toUpperCase() }}
      </span>
    </div>
  </div>
</template>

<script>

import getTypeIcon from "@/utils/entityTypeIcons.js"

export default {
  name: "EntityCard",
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
}
</script>
  