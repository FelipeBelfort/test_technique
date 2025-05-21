import { ref } from "vue"

const isSpeaking = ref(false)
const speechConfig = ref({
  rate: 1,
  pitch: 0.8,
  volume: 1,
  lang: "en-US",
  voice: null,
  voices: [
    {
      langCode: "en-US",
      langName: "English",
      options: [] 
    },
    {
      langCode: "pt-BR",
      langName: "Português",
      options: [] 
    },
    {
      langCode: "fr-FR",
      langName: "Français",
      options: [] 
    },
  ],
})

let synth = window.speechSynthesis
let utterance = null

async function getVoicesByLangue() {
  const voices = await initVoices()
  for (const lang of speechConfig.value.voices) {
    lang.options = voices.filter(voice => voice.lang === lang.langCode)
  }
}

function initVoices() {
  return new Promise((resolve) => {
    let voices = synth.getVoices()
    if (voices.length) {
      resolve(voices)
    } else {
      synth.onvoiceschanged = () => {
        voices = synth.getVoices()
        resolve(voices)
      }
    }
  })
}

async function speak(text) {
  if (!synth) return

  stop()

  utterance = new SpeechSynthesisUtterance(text)
  const config = speechConfig.value
  utterance.rate = config.rate
  utterance.pitch = config.pitch
  utterance.volume = config.volume
  utterance.lang = config.lang

  if (config.voice) {
    utterance.voice = config.voice
  }

  isSpeaking.value = true
  synth.speak(utterance)

  utterance.onend = () => {
    isSpeaking.value = false
  }
}

function stop() {
  if (synth.speaking) {
    synth.cancel()
    isSpeaking.value = false
  }
}

function toggle(text) {
  if (isSpeaking.value) {
    stop()
  } else {
    speak(text)
  }
}

export default function useTextToSpeech() {

  function describeEntity(entity) {
    return `${entity.name} is ${entity.status}. `
  }

  function describeEntities(entities) {
    if (!entities.length) return "No entities available."

    return entities.map(e => {
      return `${e.name} is ${e.status}`
    }).join(". ") + "."
  }

  function createText(text, entity, entities) {
    if (entity) return describeEntity(entity)

    const describedEntities = describeEntities(entities)
    return text + ". " + describedEntities
  }

  function formatString(room, type, option) {
    return `Entities in the ${room} with the ${type} ${option}. `
  }

  return {
    isSpeaking,
    speechConfig,
    speak,
    stop,
    toggle,
    initVoices,
    createText,
    describeEntity,
    describeEntities,
    getVoicesByLangue,
    formatString,
  }
}
