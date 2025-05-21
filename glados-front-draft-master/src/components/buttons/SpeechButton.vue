<template>
  <div class="flex items-center justify-between bg-white border rounded-xl px-2 py-1 shadow-md w-fit">
    <span>{{ label }}</span>
    <button 
      @click="toggleSpeaking" 
      class="text-indigo-600 hover:text-indigo-800">
      <component 
        :is="isInstanceSpeaking ? PauseIcon : PlayIcon" 
        class="w-6 h-6" />
    </button>
  </div>
</template>

<script>

import { ref, watch } from "vue"
import PauseIcon from "vue-material-design-icons/Pause.vue"
import PlayIcon from "vue-material-design-icons/Play.vue"
import useTextToSpeech from "@/composables/useTextToSpeech"

export default {
  name: "SpeechButton",
  props: {
    text: {
      type: String,
      default: ""
    },
    label: {
      type: String,
      default: ""
    },
    entity: {
      type: Object,
      default: null
    },
    entities: {
      type: Array,
      default: () => ([])
    },
  },
  setup(props) {
    const {
      isSpeaking,
      createText,
      toggle,
    } = useTextToSpeech()

    const isInstanceSpeaking = ref(false) 

    function toggleSpeaking(event) {
      event.stopPropagation()
      const text = createText(props.text, props.entity, props.entities)
      isInstanceSpeaking.value = true
      toggle(text)
    }

    watch(isSpeaking, () => {
      if (!isSpeaking.value) isInstanceSpeaking.value = false
    }) 

    return {
      isSpeaking,
      isInstanceSpeaking,
      toggle,
      toggleSpeaking,
      createText,
      PlayIcon,
      PauseIcon,
    }
  }
}
</script>
