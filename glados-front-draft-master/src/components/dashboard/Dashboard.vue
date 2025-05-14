<template>
  <div class="flex flex-col gap-5">
    <div class="flex flex-row justify-between">
      <span class="text-indigo-600 font-bold text-2xl">Dashboard</span>
      <span>
        <span
          v-for="field in filterFields"
          :key="field.key">
          <select 
            v-model="filters[field.key]"
            class="border rounded px-2 py-1 pr-6 text-sm text-gray-700">
            <option value="">{{ field.label }}</option>
            <option
              v-for="option in field.options"
              :key="option"
              :value="option" >{{ option }}</option>
          </select>

        </span>
        <button 
          @click="getEntities"
          class="px-3 py-1 ml-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
          Sort
        </button>
      </span>
    </div>
    <ul
      v-if="entities.length"
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <li
        v-for="entity in entities"
        :key="entity.id">
        <EntityCard
          :entity="entity"
          @click="selectEntity(entity)"/>
      </li>
    </ul>
    <EmptyState v-else/>
    <EntityDetailsCard
      v-if="selected"
      :entity="selected"
      @close="selected=null"/>
  </div>
</template>

<script>
import EntityCard from "@/components/cards/EntityCard.vue"
import EntityDetailsCard from "@/components/cards/EntityDetailsCard.vue"
import EmptyState from "@/components/emptyState/EmptyState.vue"
import coreApi from "@/providers/core-api"
import { ENTITY_TYPES, ENTITY_STATUSES } from "@/constants/entityConstants"

export default {
  name: "Dashboard",
  components: {
    EntityCard,
    EntityDetailsCard,
    EmptyState
  },
  created() {
    this.getEntities()
  },
  data() {
    return {
      entities: [],
      selected: null,
      isLoading: false,
      isError: false,
      filters: {
        type: "",
        status: "",
        room: ""
      },
      filterFields: [
        { key: "type", label: "Type", options: ENTITY_TYPES },
        { key: "status", label: "Status", options: ENTITY_STATUSES },
        { key: "room", label: "Room", options: [] }
      ]
    }
  },
  mounted() {
    this.getEntities()
  },
  methods: { 
    getEntities() {
      this.isLoading = true
      coreApi.glados.getEntities(this.filters)
        .then((entities) => {
          this.entities = entities
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.isError = true
        })
        .finally(() => {
          this.filters = {
            type: "",
            status: "",
            room: ""
          },
          this.isLoading = false
        })
    },
    selectEntity(entity) {
      this.selected = entity
    }
  } 
}
</script>