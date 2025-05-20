import coreApi from "@/providers/core-api"
import { ref } from "vue"

export default function useSharedElements() {
  const isLoading = ref(false)
  const isDeleting = ref(false)
  const selectedEntity = ref(null)
  const selectedRoom = ref(null)
  const isError = ref(false)
  const isEditing = ref(false)
  const rooms = ref([])
  const roomsNames = ref([])

  async function getRooms() {
    isLoading.value = true
    try {
      const res = await coreApi.glados.getRooms()
      rooms.value = res
      roomsNames.value = res.map(obj => obj.name)
    } catch (error) {
      console.error(error)
      isError.value = true
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    isDeleting,
    isEditing,
    isError,
    selectedEntity,
    selectedRoom,
    rooms,
    roomsNames,
    getRooms
  }
}