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
    <div class="flex flex-row justify-between">
      <SpeechButton 
        label="Listen to all"
        :entities="entities"/>
      <span>
        <span
          v-for="field in filterFields"
          :key="field.key">
          <select 
            v-model="filters[field.key]"
            class="border rounded px-2 py-1 pr-6 text-sm text-gray-700">
            <option value="">{{ field.label }}</option>
            <option
              v-if="field.key === 'room'"
              class="text-indigo-900"
              value="@@null@@">No Room</option>
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
          @click="selectedEntity=entity"
          @toggle="toggleEntityStatus(entity)"/>
      </li>
    </ul>
    <EmptyState v-else-if="!isLoading"/>

    <EntityDetailsCard
      v-if="selectedEntity"
      :entity="selectedEntity"
      @edit="showEntityForm=true"
      @delete="isDeleting=true"
      @close="selectedEntity=null"/>

    <ConfirmDeleteCard 
      v-if="isDeleting"
      itemType="Entity"
      :obj="selectedEntity"
      @close="isDeleting=false"
      @confirm="deleteEntity"/>

    <FormEntityModal
      v-if="showEntityForm"
      :entity="selectedEntity"
      :existingEntities="entities"
      :rooms="rooms"
      :isEditing="!!selectedEntity"
      @submit="handleEntityFormSubmit"
      @close="showEntityForm=false; selectedEntity=null"/>
  </div>
</template>

<script>
import Button from "@/components/buttons/Button.vue"
import ConfirmDeleteCard from "@/components/cards/ConfirmDeleteCard.vue"
import EmptyState from "@/components/emptyState/EmptyState.vue"
import EntityCard from "@/components/cards/EntityCard.vue"
import EntityDetailsCard from "@/components/cards/EntityDetailsCard.vue"
import FormEntityModal from "@/components/forms/FormEntityModal.vue"
import SpeechButton from "../buttons/SpeechButton.vue"
import useEntities from "@/composables/useEntities"

export default {
  name: "Dashboard",
  components: {
    EntityCard,
    EntityDetailsCard,
    EmptyState,
    FormEntityModal,
    Button,
    ConfirmDeleteCard,
    SpeechButton,
  },
  setup() {
    const {
      entities,
      rooms,
      selectedEntity,
      isLoading,
      isDeleting,
      isError,
      showEntityForm,
      filters,
      filterFields,
      getEntities,
      getRooms,
      handleEntityFormSubmit,
      toggleEntityStatus,
      deleteEntity
    } = useEntities()

    getRooms()
    getEntities()

    return {
      entities,
      rooms,
      selectedEntity,
      isLoading,
      isDeleting,
      isError,
      showEntityForm,
      filters,
      filterFields,
      getEntities,
      getRooms,
      handleEntityFormSubmit,
      toggleEntityStatus,
      deleteEntity,
    }
  },
}
</script>