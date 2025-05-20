import { ref, watch } from "vue"
import coreApi from "@/providers/core-api"
import useSharedElements from "@/composables/useSharedElements"

export default function useRooms() {
  const {
    isLoading,
    isDeleting,
    isEditing,
    isError,
    selectedEntity,
    selectedRoom,
    rooms,
    roomsNames,
    getRooms
  } = useSharedElements()

  const roomEntities = ref([])
  const showRoomForm = ref(false)

  async function handleRoomFormSubmit(roomName) {
    if (isLoading.value) return
    if (isEditing.value) {
      selectedRoom.value.name = roomName
      await renameRoom(selectedRoom.value)
    } else {
      await createRoom(roomName)
    }
  }

  async function createRoom(roomName) {
    isLoading.value = true
    try {
      await coreApi.glados.createRoom(roomName)
      await getRooms()
      showRoomForm.value = false
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      isLoading.value = false
    }
  }

  async function renameRoom(room) {
    isLoading.value = true
    try {
      await coreApi.glados.renameRoom(room)
      await getRooms()
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      isEditing.value = false
      isLoading.value = false
    }
  }

  async function deleteRoom() {
    isLoading.value = true
    try {
      await coreApi.glados.deleteRoom(selectedRoom.value.id)
      selectedRoom.value = null
      isDeleting.value = false
      await getRooms()
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      isLoading.value = false
    }
  }

  async function handleDelete(func) {
    isDeleting.value = false
    await func()
    if (selectedRoom.value) await getRoomEntities(selectedRoom.value)
  }

  function selectRoom(room) {
    if (room?.id === selectedRoom.value?.id) {
      selectedRoom.value = null
    } else {
      selectedRoom.value = room
    }
  }

  function getRoomToForm() {
    return isEditing.value ? selectedRoom.value : null
  }

  async function getRoomEntities(room) {
    isLoading.value = true
    try {
      const entities = await coreApi.glados.getRoomEntities(room.id)
      roomEntities.value = entities
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      isLoading.value = false
    }
  }

  watch(selectedRoom, async (room) => {
    if (room) {
      await getRoomEntities(room)
    } else {
      roomEntities.value = []
    }
  })

  return {
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
  }
}
