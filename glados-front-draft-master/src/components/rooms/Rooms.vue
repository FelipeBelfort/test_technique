<template>
  <div class="flex flex-col gap-5">
    <div class="flex flex-row justify-between items-center">
      <span 
        class="text-indigo-600 font-bold text-2xl cursor-pointer"
        @click="getRooms">Room Manager</span>
      <span class="flex gap-2">
        <Button 
          label="Rename"
          @click="isEditing=true; showRoomForm=true"
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
            @click="showRoomForm=true"/>
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
        <div v-if="roomEntities.length">
          <div class="space-y-4">
            <template
              v-for="field in filterFields"
              :key="field">
              <div
                v-for="option in field.options"
                :key="option"
                class="border w-full">
                <h4 class="font-bold text-indigo-700 capitalize">
                  <div class="flex gap-4 items-center p-2">
                    {{ option.replace(/_/g, " ") }}
                    <SpeechButton
                      :entities="roomEntities.filter(e => e[field.key] === option)"
                      :text="formatString(selectedRoom.name, field.key, option)"
                      label="List this row"/>
                  </div>
                </h4>
                <div class="overflow-x-auto w-full">
                  <div class="flex space-x-4">
                    <EntityCard
                      v-for="entity in roomEntities.filter(e => e[field.key] === option)"
                      :key="entity.id"
                      class="min-w-[300px] flex-shrink-0"
                      :entity="entity"
                      @toggle="toggleEntityStatus(entity, roomEntities)"
                      @click="selectedEntity=entity"/>
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
      @delete="isDeleting=true"
      @edit="showEntityForm=true"
      @close="selectedEntity = null"/>

    <ConfirmDeleteCard 
      v-if="isDeleting"
      :itemType="selectedEntity ? 'Entity' : 'Room'"
      :obj="selectedEntity ?? selectedRoom"
      @close="isDeleting=false"
      @confirm="() => handleDelete(selectedEntity ? deleteEntity : deleteRoom)"/>

    <FormEntityModal
      v-if="showEntityForm"
      :entity="selectedEntity"
      :existingEntities="roomEntities"
      :rooms="rooms"
      @submit="handleEntityFormSubmit"
      @close="showEntityForm=false; selectedEntity=null"/>

    <FormRoomModal
      v-if="showRoomForm"
      :existingRooms="roomsNames"
      :room="getRoomToForm()"
      @submit="handleRoomFormSubmit"
      @close="showRoomForm=isEditing=false"/>
  </div>
</template>
  

<script>
import Button from "@/components/buttons/Button.vue"
import ConfirmDeleteCard from "@/components/cards/ConfirmDeleteCard.vue"
import EmptyState from "@/components/emptyState/EmptyState.vue"
import EntityCard from "@/components/cards/EntityCard.vue"
import EntityDetailsCard from "@/components/cards/EntityDetailsCard.vue"
import FormEntityModal from "@/components/forms/FormEntityModal.vue"
import FormRoomModal from "@/components/forms/FormRoomModal.vue"
import SpeechButton from "../buttons/SpeechButton.vue"
import useEntities from "@/composables/useEntities"
import useRooms from "@/composables/useRooms"
import useTextToSpeech from "@/composables/useTextToSpeech"

export default {
  name: "Rooms",
  components: {
    EntityCard,
    EntityDetailsCard,
    EmptyState,
    Button,
    FormEntityModal,
    FormRoomModal,
    ConfirmDeleteCard,
    SpeechButton,
  },
  setup() {
    const {
      isLoading,
      isDeleting,
      isEditing,
      isError,
      selectedRoom,
      rooms,
      roomsNames,
      getRooms,
      showRoomForm,
      roomEntities,
      handleRoomFormSubmit,
      handleDelete,
      deleteRoom,
      selectRoom,
      getRoomToForm,
      getRoomEntities,
    } = useRooms()

    const {
      showEntityForm,
      filterFields,
      selectedEntity,
      handleEntityFormSubmit,
      toggleEntityStatus,
      deleteEntity
    } = useEntities()

    const { formatString } = useTextToSpeech()

    getRooms()

    return {
      // useRooms
      isLoading,
      isDeleting,
      isEditing,
      isError,
      selectedEntity,
      selectedRoom,
      rooms,
      roomsNames,
      getRooms,
      showRoomForm,
      roomEntities,
      handleRoomFormSubmit,
      handleDelete,
      deleteRoom,
      selectRoom,
      getRoomToForm,
      getRoomEntities,
      // useEntities
      showEntityForm,
      filterFields,
      handleEntityFormSubmit,
      toggleEntityStatus,
      deleteEntity,
      // useTextToSpeech
      formatString,
    }
  },
}
</script>