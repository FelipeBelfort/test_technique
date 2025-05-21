import { ENTITY_STATUSES, ENTITY_TYPES } from "@/constants/entityConstants"
import coreApi from "@/providers/core-api"
import { ref } from "vue"
import useSharedElements from "@/composables/useSharedElements"

export default function useEntities() {
  const {
    isLoading,
    isDeleting,
    isError,
    selectedEntity,
    rooms,
    roomsNames,
    getRooms,
  } = useSharedElements()

  const entities = ref([])
  const showEntityForm = ref(false)

  const filters = ref({
    type: "",
    status: "",
    room: ""
  })

  const filterFields = ref([
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
    {
      key: "room",
      label: "Room",
      options: []
    }
  ])

  async function getEntities() {
    isLoading.value = true
    try {
      const data = await coreApi.glados.getEntities(filters.value)
      entities.value = data
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      filterFields.value[2].options = roomsNames.value
      filters.value = {
        type: "",
        status: "",
        room: ""
      }
      isLoading.value = false
    }
  }

  async function handleEntityFormSubmit(form) {
    isLoading.value = true
    try {
      if (selectedEntity.value) {
        await modifyEntity(selectedEntity.value.id, form, entities.value)
      } else {
        await coreApi.glados.createEntity(form)
        await getEntities()
      }
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      showEntityForm.value = false
      selectedEntity.value = null
      isLoading.value = false
    }
  }

  function toggleEntityStatus(entity, list = entities.value) {
    if (entity.status === ENTITY_STATUSES[2]) return
    const newStatus = entity.status === ENTITY_STATUSES[0] ? ENTITY_STATUSES[1] : ENTITY_STATUSES[0]
    modifyEntity(entity.id, { status: newStatus }, list)
  }

  async function modifyEntity(id, json, list) {
    isLoading.value = true
    try {
      const updated = await coreApi.glados.patchEntity(id, json)
      const i = list.findIndex(e => e.id === id)
      if (i !== -1) {
        list[i] = updated
      }
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      showEntityForm.value = false
      selectedEntity.value = null
      isLoading.value = false
    }
  }

  async function deleteEntity() {
    isLoading.value = true
    try {
      await coreApi.glados.deleteEntity(selectedEntity.value.id)
      await getEntities()
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      isDeleting.value = false
      selectedEntity.value = null
      isLoading.value = false
    }
  }

  return {
    entities,
    rooms,
    roomsNames,
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
  }
}
