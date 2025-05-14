<template>
  <div class="flex flex-col gap-5">
    <span class="text-indigo-600 font-bold text-2xl">Dashboard</span>
    <ul class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <li
        v-for="entity in entities"
        :key="entity.id">
        <EntityCard
          :entity="entity"
          @click="selectEntity(entity)"/>
      </li>
    </ul>
    <EntityDetailsCard
      v-if="selected"
      :entity="selected"
      @close="selected=null"/>
  </div>
</template>

<script>
import EntityCard from "@/components/cards/EntityCard.vue"
import EntityDetailsCard from "@/components/cards/EntityDetailsCard.vue"
import coreApi from "@/providers/core-api"

export default {
  name: "Dashboard",
  components: {
    EntityCard,
    EntityDetailsCard
  },
  created() {
    this.getEntities()
  },
  data() {
    return {
      entities: [],
      selected: null,
      isLoading: false,
      isError: false 
    }
  },
  methods: { 
    getEntities() {
      this.isLoading = true

      coreApi.glados.getEntities()
        .then((entities) => {
          this.entities = entities
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.isError = true
        })
        .finally(() => {
          this.isLoading = false
        })
    },
    selectEntity(entity) {
      this.selected = entity
    }
  } 
}
</script>