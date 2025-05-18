<template>
  <div class="flex flex-col gap-5">
    <div class="flex flex-row justify-between items-center">
      <span class="text-indigo-600 font-bold text-2xl">Room Manager</span>
      <span class="flex gap-2">
        <Button 
          label="Rename"
          @click="isEditing=true"
          :disabled="!selectedRoom"/>
        <Button 
          label="delete"
          color="danger"
          @click="isDeleting=true"
          :disabled="!selectedRoom"/>
      </span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-[1fr_4fr] gap-6">
      <!-- Rooms list -->
      <div>
        <div class="flex flex-row justify-between items-center pb-2">
          <h3 class="text-lg font-semibold mb-2">Rooms</h3>
          <Button 
            label="+ Add Room"
            size="small"
            @click="isCreating=true"/>
        </div>
        <ul class="space-y-2">
          <li
            v-for="room in rooms"
            :key="room.id"
            @click="selectRoom(room)"
            class="cursor-pointer p-2 rounded border hover:bg-indigo-50"
            :class="{ 'bg-indigo-100': room.id === selectedRoom?.id }">
            {{ room.name }}
          </li>
        </ul>
      </div>  
      <!-- Entities viewer -->
      <div class="min-w-0">
        <h3 
          v-if="selectedRoom"
          class="text-lg font-semibold mb-4">
          Entities in {{ selectedRoom.name }}</h3>  
        <div v-if="entities.length">
          <div class="space-y-4">
            <template
              v-for="field in fields"
              :key="field">
              <div
                v-for="option in field.options"
                :key="option"
                class="border w-full">
                <h4 class="font-bold text-indigo-700 capitalize">
                  <div class="flex gap-4 items-center p-2">
                    {{ option.replace(/_/g, " ") }}
                    <Button
                      v-if="option === 'on'"
                      label="Turn Off All Entities"
                      size="small"
                      color="danger"
                      :disabled="statuses['on']"/>
                    <Button
                      v-if="option === 'off'"
                      label="Turn On All Entities"
                      size="small"
                      color="on"
                      :disabled="statuses['off']"/>
                  </div>
                </h4>
                <div class="overflow-x-auto w-full">
                  <div class="flex space-x-4">
                    <EntityCard
                      v-for="entity in filteredBy(field.key, option)"
                      :key="entity.id"
                      class="min-w-[300px] flex-shrink-0"
                      :entity="entity"
                      @click="selectEntity(entity)"/>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>  

        <EmptyState v-else-if="selectedRoom && !isLoading"/>
        
        <div 
          v-else
          class="text-gray-500 italic">
          Select a room to view its entities.
        </div>
      </div>
    </div>

    <EntityDetailsCard
      v-if="selectedEntity"
      :entity="selectedEntity"
      @close="selectedEntity = null"/>

    <ConfirmDeleteCard 
      v-if="isDeleting"
      itemType="Room"
      :obj="selectedRoom"
      @close="isDeleting=false"
      @confirm="deleteRoom"/>

    <FormRoomModal
      v-if="isCreating || isEditing"
      :existingRooms="rooms.map(r => r.name)"
      :room="getRoomToForm()"
      @submit="editRoom"
      @close="isCreating=isEditing=false"/>
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
import FormRoomModal from "@/components/forms/FormRoomModal.vue"

export default {
  name: "Rooms",
  components: {
    EntityCard,
    EntityDetailsCard,
    EmptyState,
    Button,
    FormRoomModal,
    ConfirmDeleteCard
  },
  created() {
    this.getRooms()
  },
  data() {
    return {
      entities: [],
      rooms: [],
      statuses: {
        on: false,
        off: false 
      },
      selectedEntity: null,
      selectedRoom: null,
      isLoading: false,
      isError: false,
      isCreating: false,
      isEditing: false,
      isDeleting: false,
      fields: [
        {
          key: "status",
          label: "Status",
          options: ENTITY_STATUSES 
        },
        {
          key: "type",
          label: "Type",
          options: ENTITY_TYPES 
        },
      ]
    }
  },
  methods: { 
    getRoomEntities(room) {
      this.isLoading = true
      coreApi.glados.getRoomEntities(room.id)
        .then((entities) => {
          this.selectedRoom = room
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
          this.isLoading = false
        })
    },
    createRoom(roomName) {
      this.isLoading = true
      coreApi.glados.createRoom(roomName)
        .then(() => {
          this.isCreating = false
          this.getRooms()
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
    renameRoom(room) {
      this.isLoading = true
      coreApi.glados.renameRoom(room)
        .then(() => {
          this.isEditing = false
          this.getRooms()
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
    deleteRoom() {
      this.isLoading = true
      coreApi.glados.deleteRoom(this.selectedRoom.id)
        .then(() => {
          this.selectedRoom = null
          this.isDeleting = false
          this.getRooms()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.isError = true
        })
        .finally(() => {
          this.getRooms()
          this.isLoading = false
        })
    },
    editRoom(roomName) {
      if (this.isEditing) {
        this.selectedRoom.name = roomName
        this.renameRoom(this.selectedRoom)
        return
      }
      this.createRoom(roomName)
    },
    filteredBy(key, option) {
      if (option === "on" || option === "off") {
        const statusesList = this.entities.filter(e => e[key] === option)
        this.statuses[option] = statusesList.length === 0

        return statusesList
      }
      return this.entities.filter(e => e[key] === option)
    },
    selectEntity(entity) {
      this.selectedEntity = entity
    },
    selectRoom(room) {
      if (room === this.selectedRoom) {
        this.selectedRoom = null
        this.entities = []
        return
      }
      this.selectedRoom = room
      this.getRoomEntities(room)
    },
    getRoomToForm() {
      if (this.isEditing) return this.selectedRoom
      return null
    },
  } 
}
</script>