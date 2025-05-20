import coreApiClient from "@/providers/core-api/CoreApi"

function getRequestUrl(filters) {

  const params = Object.entries(filters)
    .filter(entry => entry[1] !== "")
    .map(([key, value]) => `${key}=${value}`)

  if (params.length === 0) {
    return "/entities"
  }

  return `/entities?${params.join("&")}`
}

export default {
  //  Entities API //
  getEntities(filters) {

    const requestUrl = getRequestUrl(filters)

    return coreApiClient.sendRequest("get", requestUrl, {})
  },

  patchEntity(id, json) {
    return coreApiClient.sendRequest("patch", `/entities/${id}`, json)
  },

  createEntity(json) {
    return coreApiClient.sendRequest("post", "/entities", json)
  },

  deleteEntity(entityId) {
    return coreApiClient.sendRequest("delete", `/entities/${entityId}`, {})
  },

  //  Rooms API //
  getRooms() {
    return coreApiClient.sendRequest("get", "/rooms", {})
  },

  getRoomEntities(id) {
    return coreApiClient.sendRequest("get", `/rooms/${id}`, {})
  },

  createRoom(roomName) {
    return coreApiClient.sendRequest("post", "/rooms", { "name": roomName })
  },

  renameRoom(room) {
    return coreApiClient.sendRequest("patch", `/rooms/${room.id}`, { "name": room.name })
  },

  deleteRoom(roomId) {
    return coreApiClient.sendRequest("delete", `/rooms/${roomId}`, {})
  },
}
