<template>
  <div class="flex items-center justify-between w-full px-5">
    <Logo />
    <div class="text-lg flex gap-5">
      <span
        v-for="tab in tabs"
        :key="tab.name"
        @click="goTo(tab.name)"
        :class="[$route.name === tab.name ? activeClass : 'cursor-pointer hover:text-indigo-800', 'transition-colors duration-200 ease-in-out']">
        {{ tab.label }}
      </span>
      <Cog
        class="cursor-pointer hover:text-indigo-800 transition-colors duration-200 ease-in-out"
        @click="openConfig=true"/>
    </div>
    <AudioConfigCard 
      v-if="openConfig"
      @close="openConfig=false"/>
  </div>
</template>

<script>
import AudioConfigCard from "@/components/cards/AudioConfigCard.vue"
import Cog from "vue-material-design-icons/Cog.vue"
import Logo from "@/components/ui/Logo.vue"

export default {
  name: "Header",
  components: {
    Logo,
    Cog,
    AudioConfigCard,
  },
  data() {
    return {
      openConfig: false,
      tabs: [
        {
          label: "Dashboard",
          name: "dashboard"
        },
        {
          label: "Rooms",
          name: "rooms"
        },
        {
          label: "About",
          name: "about"
        }
      ]
    }
  },
  computed: {
    activeClass() {
      return "text-indigo-600 cursor-default font-bold"
    }
  },
  methods: {
    goTo(name) {
      this.$router.push({ name })
    }
  }
}
</script>