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
  getEntities(filters) {

    const requestUrl = getRequestUrl(filters)

    return coreApiClient.sendRequest("get", requestUrl, {})
  },
}
