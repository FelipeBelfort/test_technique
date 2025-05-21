<template>
  <div
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    @click.self="$emit('close')">
    <div class="bg-white rounded-xl p-6 shadow-lg max-w-md w-full">
      <div class="flex flex-row justify-between">
        <h3 class="text-xl font-bold mb-2">Audio Settings</h3>
        <Button
          label="test me"
          @click="saySomething"/>
      </div>

      <div class="flex flex-row gap-2 items-center my-2">
        <p><strong>Rate:</strong></p>
        <input 
          type="range" 
          min="0.1" 
          max="2" 
          step="0.1" 
          v-model="speechConfig.rate"/>
      </div>

      <div class="flex flex-row gap-2 items-center my-2">
        <p><strong>Pitch:</strong></p>
        <input 
          type="range" 
          min="0" 
          max="2" 
          step="0.1" 
          v-model="speechConfig.pitch"/>
      </div>
      
      <div class="flex flex-row gap-2 items-center my-2">
        <p><strong>Language:</strong></p>
        <select
          v-model="speechConfig.lang"
          class="block w-full mt-1 border-gray-300 rounded-md">
          <option 
            v-for="voice in speechConfig.voices" 
            :key="voice.langCode" 
            :value="voice.langCode">{{ voice.langName }}</option>
        </select>
      </div>
      <div class="flex flex-row gap-2 items-center my-2">
        <p><strong>Voice:</strong></p>
        <select
          v-if="speechConfig.voices.find(group => group.langCode === speechConfig.lang)?.options.length"
          v-model="speechConfig.voice"
          class="block w-full mt-1 border-gray-300 rounded-md">
          <option 
            v-for="voice in speechConfig.voices.find(group => group.langCode === speechConfig.lang)?.options" 
            :key="voice.name" 
            :value="voice">{{ voice.name }}</option>
        </select>
      </div>

      <div class="mt-6 flex justify-end gap-2">
        <Button 
          @click="resetValues"
          color="neutral"
          size="small"
          label="Reset"/>
        <Button 
          @click="$emit('close')"
          label="OK"/>
      </div>
    </div>
  </div>
</template>

<script>
import Button from "@/components/buttons/Button.vue"
import useTextToSpeech from "@/composables/useTextToSpeech"

export default {

  name: "AudioConfigCard",
  components: { Button },
  setup() {
    const {
      speak,
      speechConfig,
      getVoicesByLangue,
    } = useTextToSpeech()

    const initialValues = {
      lang: speechConfig.value.lang,
      rate: speechConfig.value.rate,
      pitch: speechConfig.value.pitch,
      voice: speechConfig.value.voice,
    }

    getVoicesByLangue()

    function resetValues() {
      speechConfig.value.lang = initialValues.lang
      speechConfig.value.rate = initialValues.rate
      speechConfig.value.pitch = initialValues.pitch
      speechConfig.value.voice = initialValues.voice
    }

    function saySomething() {
      speak("Hello! I'm Glados to help you with this settings.")
    }

    return {
      resetValues,
      speak,
      speechConfig,
      saySomething,
    }
  }
}
</script>