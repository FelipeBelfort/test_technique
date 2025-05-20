<template>
  <div class="flex flex-col gap-5">
    <div class="flex flex-row justify-between">
      <span 
        class="text-indigo-600 font-bold text-2xl cursor-pointer"
        @click="getEntities">Dashboard</span>
      <span>
        <Button
          @click="showEntityForm=true"
          label="+ Add Entity"/>
      </span>
    </div>
    <div class="flex flex-row justify-end">
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
              class="text-indigo-900"
              :value="option" >{{ option.replace(/_/g, " ") }}</option>
          </select>

        </span>
        <Button
          @click="getEntities"
          label="Search"
          size="small"
          class="ml-1"/>
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
          @click="selectEntity(entity)"
          @toggle="toggleEntityStatus(entity)"/>
      </li>
    </ul>
    <EmptyState v-else-if="!isLoading"/>

    <EntityDetailsCard
      v-if="selected"
      :entity="selected"
      @edit="showEntityForm=true"
      @delete="isDeleting=true"
      @close="selected=null"/>

    <ConfirmDeleteCard 
      v-if="isDeleting"
      itemType="Entity"
      :obj="selected"
      @close="isDeleting=false"
      @confirm="deleteEntity"/>

    <FormEntityModal
      v-if="showEntityForm"
      :entity="selected"
      :existingEntities="entities"
      :rooms="rooms"
      :isEditing="!!selected"
      @submit="handleFormSubmit"
      @close="showEntityForm=false; selected=null"/>
  </div>
</template>

<script>
import { ENTITY_STATUSES, ENTITY_TYPES } from "@/constants/entityConstants"
import Button from "@/components/buttons/Button.vue"
import ConfirmDeleteCard from "@/components/cards/ConfirmDeleteCard.vue"
import coreApi from "@/providers/core-api"
import EmptyState from "@/components/emptyState/EmptyState.vue"
import EntityCard from "@/components/cards/EntityCard.vue"
import EntityDetailsCard from "@/components/cards/EntityDetailsCard.vue"
import FormEntityModal from "@/components/forms/FormEntityModal.vue"

export default {
  name: "Dashboard",
  components: {
    EntityCard,
    EntityDetailsCard,
    EmptyState,
    FormEntityModal,
    Button,
    ConfirmDeleteCard,
  },
  created() {
    this.getEntities()
    this.getRooms()
  },
  data() {
    return {
      entities: [],
      rooms: [],
      selected: null,
      isLoading: false,
      isDeleting: false,
      isError: false,
      showEntityForm: false,
      filters: {
        type: "",
        status: "",
        room: ""
      },
      filterFields: [
        {
          key: "type",
          label: "Type",
          options: ENTITY_TYPES 
        },
        {
          key: "status",
          label: "Status",
          options: ENTITY_STATUSES 
        },
        {
          key: "room",
          label: "Room",
          options: [] 
        }
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
    getRooms() {
      this.isLoading = true
      coreApi.glados.getRooms()
        .then((rooms) => {
          this.rooms = rooms
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.isError = true
        })
        .finally(() => {
          this.filterFields[2].options = this.rooms.map(obj => obj.name)
          this.isLoading = false
        })
    },
    selectEntity(entity) {
      this.selected = entity
    },
    handleFormSubmit(form) {
      if (this.selected) {
        this.modifyEntity(this.selected.id, form)
      } else {
        this.isLoading = true
        coreApi.glados.createEntity(form)
          .then(() => {
            this.getEntities()
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error)
            this.isError = true
          }).finally(() => {
            this.showEntityForm = false
            this.selected = null
            this.isLoading = false
          })
      }
    },
    toggleEntityStatus(entity) {
      const newStatus = entity.status === "on" ? "off" : "on"
      this.modifyEntity(entity.id, {"status": newStatus})
    },
    modifyEntity(id, json) {
      this.isLoading = true
      coreApi.glados.patchEntity(id, json)
        .then((updated) => {
          const i = this.entities.findIndex(e => e.id === id)
          if (i !== -1) {
            this.entities[i] = updated
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.isError = true
        })
        .finally(() => {
          this.showEntityForm = false
          this.selected = null
          this.isLoading = false
        })
    },
    deleteEntity() {
      this.isLoading = true
      coreApi.glados.deleteEntity(this.selected.id)
        .then(() => {
          this.getEntities()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.isError = true
        })
        .finally(() => {
          this.isDeleting = false
          this.selected = null
          this.isLoading = false
        })
    },
  } 
}
</script>