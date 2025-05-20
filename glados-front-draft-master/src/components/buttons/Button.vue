<template>
  <button
    type="submit"
    :disabled="disabled || loading"
    class="
      inline-flex justify-center items-center py-2 px-4 border border-transparent shadow-sm font-medium rounded-md text-white
      transition-colors duration-300
      focus:outline-none
      disabled:bg-gray-300 disabled:text-gray-400 disabled:cursor-not-allowed"
    :class="[classes, colorClasses]">
    {{ label }}
    <span
      v-if="emoji"
      class="ml-4">{{ emoji }}</span>
    <loading
      v-if="loading"
      :size="18"
      class="animate-spin ml-2" />
  </button>
</template>

<script>
export default {
  name: "Button",
  props: {
    label: {
      type: String,
      required: true
    },
    size: {
      type: String,
      default: "normal"
    },
    color: {
      type: String,
      default: "default",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    emoji: {
      type: String,
      required: false
    }
  },
  computed: {
    classes() {
      const SIZES_MAP = { 
        large: "uppercase text-2xl py-3 px-7 font-bold tracking-wider",
        small: "py-1 px-2 text-xs",
        statusButton: "uppercase text-lg py-0"
      }
      return SIZES_MAP[this.size] || ""
    },
    colorClasses() {
      const COLORS_MAP = { 
        default: "bg-indigo-600 hover:bg-indigo-500 focus:bg-indigo-700",
        danger: "bg-red-600 hover:bg-red-500 focus:bg-red-700",
        on: "bg-green-600 hover:bg-green-500 focus:bg-green-700",
        neutral: "bg-gray-600 hover:bg-gray-500 focus:bg-gray-700"

      }
      return COLORS_MAP[this.color] || ""
    },
  }
}
</script>

<style lang="scss" scoped>
</style>